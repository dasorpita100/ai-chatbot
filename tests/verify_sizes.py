import asyncio
import base64
import json
import os
import subprocess
import time
import urllib.request
import websockets

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9222
USER_DATA = "/tmp/chrome_verify_profile"

def start_chrome():
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={USER_DATA}",
        f"--remote-debugging-port={PORT}",
        "--window-size=1280,800",
        "about:blank"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc

async def run_inspection():
    proc = start_chrome()
    try:
        # Wait for debugging port
        ws_url = None
        for _ in range(30):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as resp:
                    tabs = json.loads(resp.read().decode())
                    for tab in tabs:
                        if tab.get("type") == "page":
                            ws_url = tab["webSocketDebuggerUrl"]
                            break
                    if ws_url:
                        break
            except Exception:
                await asyncio.sleep(0.5)

        if not ws_url:
            print("Failed to connect to Chrome debugging port")
            return

        async with websockets.connect(ws_url) as ws:
            # Navigate to localhost:8501
            nav_req = {
                "id": 1,
                "method": "Page.navigate",
                "params": {"url": "http://localhost:8501"}
            }
            await ws.send(json.dumps(nav_req))
            await ws.recv()

            # Poll until header buttons are present
            poll_expr = """
            (() => {
                const theme = document.querySelector('.st-key-hdr_theme_btn button');
                const lang = document.querySelector('.st-key-hdr_lang_popover div[data-testid="stPopover"] > button') || document.querySelector('.st-key-hdr_lang_popover button');
                const auth = document.querySelector('.st-key-hdr_auth_btn button') || document.querySelector('.st-key-hdr_user_menu div[data-testid="stPopover"] > button');
                return !!(theme && lang && auth);
            })()
            """
            for _ in range(40):
                await ws.send(json.dumps({
                    "id": 2,
                    "method": "Runtime.evaluate",
                    "params": {"expression": poll_expr, "returnByValue": True}
                }))
                poll_resp = json.loads(await ws.recv())
                if poll_resp.get("result", {}).get("result", {}).get("value") is True:
                    break
                await asyncio.sleep(0.5)

            # Wait an extra 0.5s for styles to settle
            await asyncio.sleep(0.5)

            # Evaluate script to query dimensions
            eval_expr = """
            (() => {
                const results = {};
                const controls = {
                    theme: document.querySelector('.st-key-hdr_theme_btn button'),
                    lang: document.querySelector('.st-key-hdr_lang_popover div[data-testid="stPopover"] > button') || document.querySelector('.st-key-hdr_lang_popover button'),
                    auth: document.querySelector('.st-key-hdr_auth_btn button') || document.querySelector('.st-key-hdr_user_menu div[data-testid="stPopover"] > button')
                };

                for (const [key, el] of Object.entries(controls)) {
                    if (!el) {
                        results[key] = { error: "Element not found" };
                        continue;
                    }
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    results[key] = {
                        text: el.innerText.trim(),
                        className: el.className,
                        hasHeaderControlClass: el.classList.contains('header-control'),
                        rect: {
                            width: rect.width,
                            height: rect.height,
                            top: rect.top,
                            left: rect.left
                        },
                        computed: {
                            width: style.width,
                            height: style.height,
                            minWidth: style.minWidth,
                            minHeight: style.minHeight,
                            maxWidth: style.maxWidth,
                            maxHeight: style.maxHeight,
                            padding: style.padding,
                            margin: style.margin,
                            borderWidth: style.borderWidth,
                            borderStyle: style.borderStyle,
                            borderRadius: style.borderRadius,
                            boxSizing: style.boxSizing,
                            display: style.display,
                            alignItems: style.alignItems,
                            justifyContent: style.justifyContent
                        }
                    };
                }
                return results;
            })()
            """
            req = {
                "id": 3,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": eval_expr,
                    "returnByValue": True
                }
            }
            await ws.send(json.dumps(req))
            resp = json.loads(await ws.recv())
            val = resp.get("result", {}).get("result", {}).get("value", {})
            print("=== BUTTON DIMENSIONS AND COMPUTED STYLES ===")
            print(json.dumps(val, indent=2))

            # Test click on Theme Toggle -> Switches to Light Mode
            print("\n--- Clicking Theme Toggle Button to switch to Light Mode ---")
            await ws.send(json.dumps({
                "id": 5,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.querySelector('.st-key-hdr_theme_btn button').click()"}
            }))
            await ws.recv()
            await asyncio.sleep(2)

            # Re-evaluate dimensions in Light Mode
            req_light = {
                "id": 6,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": eval_expr,
                    "returnByValue": True
                }
            }
            await ws.send(json.dumps(req_light))
            resp_light = json.loads(await ws.recv())
            val_light = resp_light.get("result", {}).get("result", {}).get("value", {})
            print("=== BUTTON DIMENSIONS AND COMPUTED STYLES IN LIGHT MODE ===")
            print(json.dumps(val_light, indent=2))

            # Take Light Mode screenshot
            await ws.send(json.dumps({
                "id": 7,
                "method": "Page.captureScreenshot",
                "params": {"format": "png"}
            }))
            shot_light_resp = json.loads(await ws.recv())
            img_light_data = base64.b64decode(shot_light_resp["result"]["data"])
            shot_light_path = "/Users/orpitadas/.gemini/antigravity-ide/brain/f7f0f10a-c601-4764-9c35-30198cfe0bc8/chrome_verified_screenshot_light.png"
            with open(shot_light_path, "wb") as f:
                f.write(img_light_data)
            print(f"Light Mode Screenshot written to {shot_light_path}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    asyncio.run(run_inspection())
