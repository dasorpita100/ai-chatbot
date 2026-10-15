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
USER_DATA = "/tmp/chrome_audit_profile"

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

async def run_audit():
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
            print("Failed to connect to Chrome debugging port")
            return

        async with websockets.connect(ws_url) as ws:
            # 1. Audit Dark Mode
            nav_req = {
                "id": 1,
                "method": "Page.navigate",
                "params": {"url": "http://localhost:8501?theme=dark"}
            }
            await ws.send(json.dumps(nav_req))
            await ws.recv()

            # Wait for render
            await asyncio.sleep(3.5)

            # Evaluate DOM in Dark Mode to find all white/light blocks and contrast issues
            eval_expr = """
            (() => {
                const issues = [];
                const allElements = document.querySelectorAll('*');
                
                function parseRgb(colorStr) {
                    const match = colorStr.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
                    if (!match) return null;
                    return { r: parseInt(match[1]), g: parseInt(match[2]), b: parseInt(match[3]) };
                }
                
                function luminance(r, g, b) {
                    const a = [r, g, b].map(v => {
                        v /= 255;
                        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
                    });
                    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
                }

                allElements.forEach(el => {
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    if (rect.width === 0 || rect.height === 0 || style.display === 'none' || style.visibility === 'hidden') return;
                    
                    const bg = style.backgroundColor;
                    const fg = style.color;
                    const rgbBg = parseRgb(bg);
                    const rgbFg = parseRgb(fg);
                    
                    // Check for unintended white or very light background in dark mode
                    if (rgbBg && rgbBg.r > 230 && rgbBg.g > 230 && rgbBg.b > 230) {
                        // Skip if intentionally transparent or 0 opacity
                        if (!bg.includes('rgba') || !bg.includes(', 0)')) {
                            // Find selector/identification
                            let sel = el.tagName.toLowerCase();
                            if (el.id) sel += '#' + el.id;
                            if (el.className && typeof el.className === 'string') {
                                sel += '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.');
                            }
                            const testId = el.getAttribute('data-testid');
                            if (testId) sel += `[data-testid="${testId}"]`;
                            
                            issues.push({
                                type: 'light-background-in-dark-mode',
                                selector: sel,
                                textSample: (el.innerText || '').slice(0, 40).replace(/\\n/g, ' '),
                                rect: { width: Math.round(rect.width), height: Math.round(rect.height), top: Math.round(rect.top), left: Math.round(rect.left) },
                                bg: bg,
                                fg: fg
                            });
                        }
                    }
                });
                
                return {
                    totalChecked: allElements.length,
                    themeModeText: document.querySelector('.st-key-hdr_theme_btn button')?.innerText || 'not found',
                    issues: issues.slice(0, 50)
                };
            })()
            """
            await ws.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {"expression": eval_expr, "returnByValue": True}
            }))
            resp = json.loads(await ws.recv())
            val = resp.get("result", {}).get("result", {}).get("value", {})
            print("=== DARK MODE AUDIT RESULTS ===")
            print(json.dumps(val, indent=2))

            # Capture Dark Mode Screenshot
            await ws.send(json.dumps({
                "id": 3,
                "method": "Page.captureScreenshot",
                "params": {"format": "png"}
            }))
            shot_resp = json.loads(await ws.recv())
            img_data = base64.b64decode(shot_resp["result"]["data"])
            shot_path = "/Users/orpitadas/.gemini/antigravity-ide/brain/f7f0f10a-c601-4764-9c35-30198cfe0bc8/dark_mode_audit_full.png"
            with open(shot_path, "wb") as f:
                f.write(img_data)
            print(f"Dark mode screenshot written to {shot_path}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

if __name__ == "__main__":
    asyncio.run(run_audit())
