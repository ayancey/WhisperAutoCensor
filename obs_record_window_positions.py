import time
import json
import win32gui
from obswebsocket import obsws, requests  # noqa: E402


# Get all windows with their positions and sizes
def get_window_positions():
    windows = []

    def callback(hwnd, extra):
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        windows.append({
            "text": win32gui.GetWindowText(hwnd),
            "location": {
                "x": x,
                "y": y
            },
            "size": {
                "width": w,
                "height": h
            },
            "active": win32gui.GetForegroundWindow() == hwnd
        })

    win32gui.EnumWindows(callback, None)

    return windows


host = "localhost"
port = 4455
password = ""


ws = obsws(host, port, password)
ws.connect()


recording = None

try:
    while True:
        recording_status = ws.call(requests.GetRecordStatus())

        if recording_status.datain["outputActive"]:
            recording = True
        else:
            if recording is True or recording is None:
                print("Window capture will start when OBS is recording")
            recording = False

        if recording:
            window_pos = get_window_positions()

            with open("window_recording.json", "a") as f:
                f.write(json.dumps({
                    "time": recording_status.datain["outputTimecode"],
                    "windows": get_window_positions()
                }) + "\n")

            print(f"recorded positions at {recording_status.datain['outputTimecode']}")

        time.sleep(1)
except KeyboardInterrupt:
    pass

ws.disconnect()
