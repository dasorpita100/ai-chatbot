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
USER_DATA = "/tmp/chrome_audit_profile2"

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
        "--window-size=1280,900",
        "about:blank"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc

async def run_detailed_audit():
    proc = start_chrome()
    try:
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
            print("Failed to connect")
            return

        async with websockets.connect(ws_url) as ws:
            # 1. Dark Mode
            await ws.send(json.dumps({
                "id": 1,
                "method": "Page.navigate",
                "params": {"url": "http://localhost:8501?theme=dark"}
            }))
            await ws.recv()
            await asyncio.sleep(3)

            # Test 1: Open Preferences Expander
            open_expander_script = """
            (() => {
                const summary = document.querySelector('[data-testid="stExpander"] summary');
                if (summary) summary.click();
            })()
            """
            await ws.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {"expression": open_expander_script}
            }))
            await ws.recv()
            await asyncio.sleep(1)

            # Capture Preferences screenshot
            await ws.send(json.dumps({
                "id": 3,
                "method": "Page.captureScreenshot",
                "params": {"format": "png"}
            }))
            shot1 = json.loads(await ws.recv())
            with open("/Users/orpitadas/.gemini/antigravity-ide/brain/f7f0f10a-c601-4764-9c35-30198cfe0bc8/audit_dark_preferences.png", "wb") as f:
                f.write(base64.b64decode(shot1["result"]["data"]))

            # Test 2: Open Sign In Dialog
            open_dialog_script = """
            (() => {
                const btn = document.querySelector('.st-key-hdr_auth_btn button');
                if (btn) btn.click();
            })()
            """
            await ws.send(json.dumps({
                "id": 4,
                "method": "Runtime.evaluate",
                "params": {"expression": open_dialog_script}
            }))
            await ws.recv()
            await asyncio.sleep(1.5)

            # Capture Dialog screenshot
            await ws.send(json.dumps({
                "id": 5,
                "method": "Page.captureScreenshot",
                "params": {"format": "png"}
            }))
            shot2 = json.loads(await ws.recv())
            with open("/Users/orpitadas/.gemini/antigravity-ide/brain/f7f0f10a-c601-4764-9c35-30198cfe0bc8/audit_dark_dialog.png", "wb") as f:
                f.write(base64.b64decode(shot2["result"]["data"]))

            # Check all elements in Dialog for white/light backgrounds
            check_dialog_script = """
            (() => {
                const dialog = document.querySelector('[data-testid="stDialog"]') || document.querySelector('[data-testid="stModal"]');
                if (!dialog) return { error: "dialog not found" };
                const results = [];
                dialog.querySelectorAll('*').forEach(el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    if (rect.width === 0 || rect.height === 0) return;
                    results.push({
                        tag: el.tagName,
                        className: el.className,
                        bg: style.backgroundColor,
                        color: style.color,
                        text: (el.innerText || '').slice(0, 30)
                    });
                });
                return results.filter(r => r.bg !== 'rgba(0, 0, 0, 0)');
            })()
            """
            await ws.send(json.dumps({
                "id": 6,
                "method": "Runtime.evaluate",
                "params": {"expression": check_dialog_script, "returnByValue": True}
            }))
            val_dialog = json.loads(await ws.recv())
            print("Dialog background styles in dark mode:")
            print(json.dumps(val_dialog.get("result", {}).get("result", {}).get("value"), indent=2))

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    asyncio.run(run_detailed_audit())
