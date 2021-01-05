import threading

import win32api, win32con, win32gui, win32ui

class draw_crosshair():
    def __init__(self):
        self.fontSize = 48
        self.color = win32api.RGB(0,255,0)
        self.text = '＋'

    def join(self):
        self.t.join()

    def create(self):
        self.t = threading.Thread(target=self.run, )
        self.t.setDaemon(True)
        self.t.start()

    def close(self):
        win32gui.SendMessage(self.hWindow, win32con.WM_DESTROY, 0, 0)

    def run(self):
        hInstance = win32api.GetModuleHandle()
        className = 'MyWindowClassName'

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633576(v=vs.85).aspx
        # win32gui does not support WNDCLASSEX.
        wndClass                = win32gui.WNDCLASS()
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ff729176(v=vs.85).aspx
        wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = hInstance
        wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = className
        # win32gui does not support RegisterClassEx
        wndClassAtom = win32gui.RegisterClass(wndClass)

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # Consider using: WS_EX_COMPOSITED, WS_EX_LAYERED, WS_EX_NOACTIVATE, WS_EX_TOOLWINDOW, WS_EX_TOPMOST, WS_EX_TRANSPARENT
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms632600(v=vs.85).aspx
        # Consider using: WS_DISABLED, WS_POPUP, WS_VISIBLE
        style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms632680(v=vs.85).aspx
        self.hWindow = win32gui.CreateWindowEx(
            exStyle,
            wndClassAtom,
            None, # WindowName
            style,
            0, # x
            0, # y
            win32api.GetSystemMetrics(win32con.SM_CXSCREEN), # width
            win32api.GetSystemMetrics(win32con.SM_CYSCREEN), # height
            None, # hWndParent
            None, # hMenu
            hInstance,
            None # lpParam
        )

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633540(v=vs.85).aspx
        win32gui.SetLayeredWindowAttributes(self.hWindow, 0x00ffffff, 180, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)

        # https://msdn.microsoft.com/en-us/library/windows/desktop/dd145167(v=vs.85).aspx
        #win32gui.UpdateWindow(self.hWindow)

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx
        win32gui.SetWindowPos(self.hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
            win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx
        # win32gui.ShowWindow(self.hWindow, win32con.SW_SHOW)

        win32gui.PumpMessages()
    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            hdc, paintStruct = win32gui.BeginPaint(hWnd)

            dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
            fontSize = self.fontSize
            win32gui.SetTextColor(hdc,self.color)
            # https://msdn.microsoft.com/en-us/library/windows/desktop/dd145037(v=vs.85).aspx
            lf = win32gui.LOGFONT()
            # lf.lfFaceName = "微軟正黑體"
            lf.lfHeight = int(round(dpiScale * fontSize))
            lf.lfWeight = 700
            # Use nonantialiased to remove the white edges around the text.
            lf.lfQuality = win32con.NONANTIALIASED_QUALITY
            hf = win32gui.CreateFontIndirect(lf)
            win32gui.SelectObject(hdc, hf)

            rect = win32gui.GetClientRect(hWnd)
            # https://msdn.microsoft.com/en-us/library/windows/desktop/dd162498(v=vs.85).aspx
            win32gui.DrawText(
                hdc,
                self.text,
                -1,
                rect,
                win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER
            )
            win32gui.EndPaint(hWnd, paintStruct)
            return 0

        elif message == win32con.WM_DESTROY:
            print('Closing the window.')
            win32gui.PostQuitMessage(0)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

if __name__ == "__main__":
    d = draw_crosshair()
    d.create()
    d.join()