import os
import subprocess
import time
import urllib.request
import json
import base64
import asyncio
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

APP_PATH = r"C:\Users\SCI\Desktop\data analyst\ipl-analytics\app.py"
SCREENSHOTS_DIR = r"C:\Users\SCI\Desktop\data analyst\ipl-analytics\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

port = 8512
chrome_port = 9232
user_data_dir = r"C:\temp\chrome_screenshot_profile12"

print(f"Launching Streamlit on port {port}...")
st_proc = subprocess.Popen([
    r"C:\Users\SCI\Desktop\data analyst\ipl-analytics\venv\Scripts\streamlit.exe",
    "run", APP_PATH,
    "--server.headless=true",
    f"--server.port={port}",
    "--browser.gatherUsageStats=false"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

try:
    # 1. Wait for health check
    for attempt in range(40):
        time.sleep(1)
        try:
            with urllib.request.urlopen(f"http://localhost:{port}/healthz", timeout=1) as r:
                if r.status == 200:
                    print(f"Streamlit responding after {attempt+1}s.")
                    break
        except Exception:
            pass

    time.sleep(2)
    print("Launching headless Chrome...")
    chrome_proc = subprocess.Popen([
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--remote-debugging-port={chrome_port}",
        f"--user-data-dir={user_data_dir}",
        "--window-size=1600,1200",
        "about:blank"
    ])

    try:
        time.sleep(3)
        req = urllib.request.urlopen(f"http://localhost:{chrome_port}/json")
        ws_url = json.loads(req.read().decode())[0]["webSocketDebuggerUrl"]
        print("Connected to CDP:", ws_url)

        async def capture_dashboard():
            async with websockets.connect(ws_url, max_size=30*1024*1024) as ws:
                msg_id = 1
                async def cdp(method, params=None):
                    nonlocal msg_id
                    cid = msg_id
                    msg_id += 1
                    await ws.send(json.dumps({"id": cid, "method": method, "params": params or {}}))
                    while True:
                        res = json.loads(await ws.recv())
                        if res.get("id") == cid:
                            return res.get("result", {})

                # Navigate to the Streamlit app URL explicitly
                print(f"Navigating to http://localhost:{port}...")
                await cdp("Page.enable")
                await cdp("Page.navigate", {"url": f"http://localhost:{port}"})

                # Poll until Streamlit tabs appear in the DOM
                print("Polling for Streamlit tabs...")
                find_tabs_js = """
                (() => {
                    const all = Array.from(document.querySelectorAll('*'));
                    const tabCandidates = all.filter(e => {
                        const tc = (e.textContent || '').trim();
                        return tc === '📊 Overview' || tc === '👤 Players' || tc === '🏟️ Teams & Venues';
                    });
                    return tabCandidates.map(t => ({
                        tag: t.tagName,
                        text: (t.textContent || '').trim()
                    }));
                })()
                """
                
                tabs_ready = False
                for s in range(30):
                    await asyncio.sleep(1)
                    res = await cdp("Runtime.evaluate", {"expression": find_tabs_js, "returnByValue": True})
                    matches = res.get("result", {}).get("value", [])
                    if len(matches) >= 3:
                        cleaned = [m['text'].encode('ascii', 'ignore').decode().strip() for m in matches]
                        print(f"Streamlit tabs rendered at {s+1}s: {cleaned}")
                        tabs_ready = True
                        break

                # Wait 5 seconds for Plotly WebGL/SVG charts to render completely
                print("Waiting 5s for Tab 1 charts to finish rendering...")
                await asyncio.sleep(5)

                # 1. Capture Tab 1 (Overview)
                print("Capturing Tab 1: Overview...")
                res1 = await cdp("Page.captureScreenshot", {"format": "png"})
                img1 = base64.b64decode(res1["data"])
                path1 = os.path.join(SCREENSHOTS_DIR, "dashboard_overview.png")
                with open(path1, "wb") as f:
                    f.write(img1)
                print(f"Saved: {path1} ({len(img1):,} bytes)")

                # 2. Click Tab 2 (Players)
                print("Clicking Tab 2 (Players)...")
                click_t2 = """
                (() => {
                    const all = Array.from(document.querySelectorAll('*'));
                    const pTab = all.find(e => (e.textContent || '').trim() === '👤 Players');
                    if (pTab) {
                        pTab.click();
                        // also click parent if button
                        if (pTab.parentElement && pTab.parentElement.tagName === 'BUTTON') {
                            pTab.parentElement.click();
                        }
                        return "Clicked Players tab";
                    }
                    return "Players tab element not found";
                })()
                """
                c2_res = await cdp("Runtime.evaluate", {"expression": click_t2, "returnByValue": True})
                print("Tab 2 click result:", c2_res.get("result", {}).get("value"))
                await asyncio.sleep(5)

                # Capture Tab 2
                print("Capturing Tab 2: Players...")
                res2 = await cdp("Page.captureScreenshot", {"format": "png"})
                img2 = base64.b64decode(res2["data"])
                path2 = os.path.join(SCREENSHOTS_DIR, "dashboard_players.png")
                with open(path2, "wb") as f:
                    f.write(img2)
                print(f"Saved: {path2} ({len(img2):,} bytes)")

                # 3. Click Tab 3 (Teams & Venues)
                print("Clicking Tab 3 (Teams & Venues)...")
                click_t3 = """
                (() => {
                    const all = Array.from(document.querySelectorAll('*'));
                    const tTab = all.find(e => (e.textContent || '').trim() === '🏟️ Teams & Venues');
                    if (tTab) {
                        tTab.click();
                        if (tTab.parentElement && tTab.parentElement.tagName === 'BUTTON') {
                            tTab.parentElement.click();
                        }
                        return "Clicked Teams & Venues tab";
                    }
                    return "Teams tab element not found";
                })()
                """
                c3_res = await cdp("Runtime.evaluate", {"expression": click_t3, "returnByValue": True})
                print("Tab 3 click result:", c3_res.get("result", {}).get("value"))
                await asyncio.sleep(5)

                # Capture Tab 3
                print("Capturing Tab 3: Teams & Venues...")
                res3 = await cdp("Page.captureScreenshot", {"format": "png"})
                img3 = base64.b64decode(res3["data"])
                path3 = os.path.join(SCREENSHOTS_DIR, "dashboard_teams.png")
                with open(path3, "wb") as f:
                    f.write(img3)
                print(f"Saved: {path3} ({len(img3):,} bytes)")

        asyncio.run(capture_dashboard())
        print("All 3 tab screenshots captured successfully!")

    finally:
        chrome_proc.terminate()
        try:
            chrome_proc.wait(timeout=3)
        except Exception:
            chrome_proc.kill()

finally:
    st_proc.terminate()
    try:
        st_proc.wait(timeout=3)
    except Exception:
        st_proc.kill()
    print("Streamlit process terminated.")
