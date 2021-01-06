import os

from draw_crosshair import draw_crosshair
from input_listener import input_listener

class main():
    def __init__(self):
        self.d = draw_crosshair()
        i = input_listener(self.switch)
        i.start()
        self.d.draw()
        self.show = True
        stop = False
        commed = ['s', 'a', 'c']
        while not stop:
            print('-------------------------')
            print('> 使用 左ALT+` 開關準星 <')
            print('-------------------------')
            print('s [int]          修改準星大小       (預設 48)')
            print('a [int]          修改準星透明度0~99 (預設 0)')
            print('c [int.int.int]  修改準星RGB顏色    (預設 255.0.0)\n')

            print('指令範例:')
            print('c 0.255.0\n')
            modify = input('輸入修改指令:\n')
            comm = modify.split(' ')[0]
            if not comm in commed:
                pass
            elif len(modify.split(' ')) > 1 and self.show:
                arg = modify.split(' ')[1]
                if comm == 's':
                    self.d.modify(fontSize=int(arg))
                elif comm == 'a':
                    a = (100 - int(arg))/100*255
                    self.d.modify(alpha=int(a))
                elif comm == 'c':
                    color = arg.split('.')
                    if color==['255','255','255']:color=[255,255,254]
                    self.d.modify(color=color)
                self.d.close()
                self.d.redraw()
            os.system('cls')

    def switch(self):
        if self.show:
            self.d.close()
        else:
            self.d.redraw()
        self.show = not self.show

if __name__ == "__main__":
    m = main()