import win32gui
import time
import json


if __name__ == '__main__':
    before = time.time()

    while True:

        now = time.time() - before
        windows_frame = {
            "time": now,
            "windows": []
        }

        def callback(hwnd, extra):
            rect = win32gui.GetWindowRect(hwnd)
            x = rect[0]
            y = rect[1]
            w = rect[2] - x
            h = rect[3] - y

            windows_frame["windows"].append({
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

        with open("recorded_file.jsonl", "a") as f:
            f.write(json.dumps(windows_frame) + "\n")

        print("recorded to file")
        time.sleep(1)
