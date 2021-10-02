import os

from draw_crosshair import draw_crosshair
from input_listener import input_listener

class main():
    def __init__(self):
        os.system('cls')
        self.d = draw_crosshair()
        self.i = input_listener(self.switch)
        self.i.start()
        self.d.draw()
        self.show = True
        stop = False
        commed = ['s', 'a', 'c']
        while not stop:
            print(' https://github.com/shounen51/crosshair')
            print(' -------------------------------')
            print(' > 使用 [左ALT] + [`] 開關準星 <')
            print(' -------------------------------')
            print('圓形版本不可調整參數')
            self.i.join()

    def switch(self):
        if self.show:
            self.d.close()
        else:
            self.d.redraw()
        self.show = not self.show

if __name__ == "__main__":
    m = main()