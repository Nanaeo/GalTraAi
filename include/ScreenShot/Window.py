import time
import tkinter as tk
import mss
import win32gui

WindowHwnd = 0
monitor = {"left": 0, "top": 0, "width": 0, "height": 0}
sct = mss.mss()


class WinSC:
    def getUserInput(MsgTitle):
        result = {"input": ""}

        def submit():
            result['input'] = entry.get()
            root.destroy()

        root = tk.Tk()
        root.title('输入数据')
        root.geometry('300x200')  # 设置窗口大小为300x200像素

        # 计算居中位置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 300
        window_height = 200
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # 设置窗口位置
        root.geometry("+{}+{}".format(position_right, position_top))

        tk.Label(root, text="请输入数据").pack()
        entry = tk.Entry(root)
        entry.pack()
        tk.Button(root, text="提交", command=submit).pack()
        root.mainloop()

        return result['input']

    def GetGameImgInit(self):
        global WindowHwnd, monitor
        WindowHwnd = int(getUserInput("请输入窗口句柄:"))
        try:
            # 获取窗口标题
            window_title = win32gui.GetWindowText(WindowHwnd)
            if not window_title:
                raise ValueError(f"没有找到窗口: {WindowHwnd}")
            print("窗口找到,标题为： " + window_title)
        except Exception:
            raise ValueError(f"没有找到窗口: {WindowHwnd}")
        left, top, right, bottom = win32gui.GetWindowRect(WindowHwnd)
        width = right - left
        height = bottom - top
        monitor = {"left": left, "top": top, "width": width, "height": height}

    def GetGameImg(self):
        global sct
        screenshot = sct.grab(monitor)
        return screenshot
        # return Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)

    def CheckLoop(self):
        global monitor, WindowHwnd
        try:
            # 获取窗口标题
            window_title = win32gui.GetWindowText(WindowHwnd)
            if not window_title:
                raise ValueError(f"没有找到窗口: {WindowHwnd}")
        except Exception:
            raise ValueError(f"没有找到窗口: {WindowHwnd}")
        left, top, right, bottom = win32gui.GetWindowRect(WindowHwnd)
        width = right - left
        height = bottom - top
        monitor = {"left": left, "top": top, "width": width, "height": height}

    def WaitWindow(self, window_title):
        global WindowHwnd
        while True:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd != 0:
                print(f"找到窗口: {window_title}")
                break
            else:
                print("等待窗口出现...")
                time.sleep(1)  # 每秒检查一次
        WindowHwnd = hwnd
