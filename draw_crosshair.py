import threading

import win32api, win32con, win32gui, win32ui

class draw_crosshair():
    def __init__(self):
        self.fontSize = 36
        self.alpha = 255
        self.color = win32api.RGB(255,255,254)
        self.color_edge = win32api.RGB(0,0,0)
        self.text = '．'
        self.DRAWING = False

    def join(self):
        self.t.join()

    def draw(self):
        self.t = threading.Thread(target=self.first_run, )
        self.t.setDaemon(True)
        self.t.start()

    def modify(self, fontSize=None, alpha=None, color=None):
        if fontSize:
            try:
                self.fontSize = int(fontSize)
            except:
                print('try use int')
        if alpha:
            try:
                self.alpha = int(alpha)
            except:
                print('try use int')
        if color:
            try:
                self.color = win32api.RGB(int(color[0]), int(color[1]), int(color[2]))
            except:
                print('try use (R,G,B)')

    def redraw(self):
        self.t = threading.Thread(target=self.run, )
        self.t.setDaemon(True)
        self.t.start()

    def close(self):
        win32gui.SendMessage(self.hWindow, win32con.WM_DESTROY, 0, 0)
        self.DRAWING = False

    def register(self):
        self.hInstance = win32api.GetModuleHandle()
        className = 'MyWindowClassName'

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633576(v=vs.85).aspx
        # win32gui does not support WNDCLASSEX.
        wndClass                = win32gui.WNDCLASS()
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ff729176(v=vs.85).aspx
        wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc    = self.wndProc
        wndClass.hInstance      = self.hInstance
        wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = className
        # win32gui does not support RegisterClassEx
        self.wndClassAtom = win32gui.RegisterClass(wndClass)
        
        self.hInstance_edge = win32api.GetModuleHandle()
        className = 'MyWindowClassName_edge'

        wndClass_edge                = win32gui.WNDCLASS()
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ff729176(v=vs.85).aspx
        wndClass_edge.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass_edge.lpfnWndProc    = self.wndProc_edge
        wndClass_edge.hInstance      = self.hInstance_edge
        wndClass_edge.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass_edge.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass_edge.lpszClassName  = className
        self.wndClassAtom_edge = win32gui.RegisterClass(wndClass_edge)

    def create_window(self):
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
        # Consider using: WS_EX_COMPOSITED, WS_EX_LAYERED, WS_EX_NOACTIVATE, WS_EX_TOOLWINDOW, WS_EX_TOPMOST, WS_EX_TRANSPARENT
        # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms632600(v=vs.85).aspx
        # Consider using: WS_DISABLED, WS_POPUP, WS_VISIBLE
        style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms632680(v=vs.85).aspx
        self.hWindow_edge = win32gui.CreateWindowEx(
            exStyle,
            self.wndClassAtom_edge,
            None, # WindowName
            style,
            1   , # x
            -3, # y
            win32api.GetSystemMetrics(win32con.SM_CXSCREEN), # width
            win32api.GetSystemMetrics(win32con.SM_CYSCREEN), # height
            None, # hWndParent
            None, # hMenu
            self.hInstance_edge,
            None # lpParam
        )
        self.hWindow = win32gui.CreateWindowEx(
            exStyle,
            self.wndClassAtom,
            None, # WindowName
            style,
            0, # x
            -3, # y
            win32api.GetSystemMetrics(win32con.SM_CXSCREEN), # width
            win32api.GetSystemMetrics(win32con.SM_CYSCREEN), # height
            None, # hWndParent
            None, # hMenu
            self.hInstance,
            None # lpParam
        )

    def show_window(self):
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633540(v=vs.85).aspx
        win32gui.SetLayeredWindowAttributes(self.hWindow_edge, 0x00ffffff, self.alpha, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.SetLayeredWindowAttributes(self.hWindow, 0x00ffffff, self.alpha, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)

        # https://msdn.microsoft.com/en-us/library/windows/desktop/dd145167(v=vs.85).aspx
        #win32gui.UpdateWindow(self.hWindow)

        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx
        win32gui.SetWindowPos(self.hWindow_edge, win32con.HWND_TOPMOST, 0, 0, 0, 0,
            win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        win32gui.SetWindowPos(self.hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
            win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        # https://msdn.microsoft.com/en-us/library/windows/desktop/ms633548(v=vs.85).aspx
        # win32gui.ShowWindow(self.hWindow, win32con.SW_SHOW)
        self.DRAWING = True
        win32gui.PumpMessages()

    def first_run(self):
        self.register()
        self.create_window()
        self.show_window()

    def run(self):
        self.create_window()
        self.show_window()

    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            hdc, paintStruct = win32gui.BeginPaint(hWnd)

            dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
            fontSize = self.fontSize
            win32gui.SetTextColor(hdc,self.color)
            # https://msdn.microsoft.com/en-us/library/windows/desktop/dd145037(v=vs.85).aspx
            lf = win32gui.LOGFONT()
            lf.lfFaceName = "微軟正黑體"
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
            # print('Closing the window.')
            win32gui.PostQuitMessage(0)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    def wndProc_edge(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            hdc, paintStruct = win32gui.BeginPaint(hWnd)

            dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
            fontSize = self.fontSize + 12
            win32gui.SetTextColor(hdc,self.color_edge)
            # https://msdn.microsoft.com/en-us/library/windows/desktop/dd145037(v=vs.85).aspx
            lf = win32gui.LOGFONT()
            lf.lfFaceName = "微軟正黑體"
            lf.lfHeight = int(round(dpiScale * fontSize))
            lf.lfWeight = 700
            # Use nonantialiased to remove the white edges around the text.
            lf.lfQuality = win32con.NONANTIALIASED_QUALITY
            hf = win32gui.CreateFontIndirect(lf)
            win32gui.SelectObject(hdc, hf)

            rect = win32gui.GetClientRect(hWnd)
            # https://msdn.microsoft.com/en-us/library/windows/desktop/dd162498(v=vs.85).aspx
            win32gui.DrawTextW(
                hdc,
                self.text,
                -1,
                rect,
                win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER
            )
            win32gui.EndPaint(hWnd, paintStruct)
            return 0

        elif message == win32con.WM_DESTROY:
            # print('Closing the window.')
            win32gui.PostQuitMessage(0)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
if __name__ == "__main__":
    import time
    d = draw_crosshair()
    time.sleep(1)
    # d.modify(fontSize=52, alpha=255, color=(255,255,254))
    d.draw()
    # d.redraw()
    d.join()