import threading
import time

from pynput import mouse
from pynput import keyboard

class input_listener():
    def __init__(self, event):
        self.keyboard_listener = keyboard.Listener(on_press = self.keyboard_on_press, on_release = self.keyboard_on_release)
        self.holding_alt = False
        self.event = event

    def button_regularization(self, btn):
        return str(btn).split('.')[-1].replace("'",'')

    def button_unregularization(self, btn):
        if len(btn) > 1:
            if btn in ['left', 'right', 'x1', 'x2', 'middle']:
                return 'Button.' + btn
            else:
                return 'Key.' + btn
        else:
            return btn

    def keyboard_on_press(self, button):
        button = self.button_regularization(button)
        if button == 'alt_l':
            self.holding_alt = True
        elif button == '`' and self.holding_alt:
            self.event()
    def keyboard_on_release(self, button):
        button = self.button_regularization(button)
        if button == 'alt_l':
            self.holding_alt = False

    def start(self):
        self.t = threading.Thread(target=self.run,)
        self.t.setDaemon(True)
        self.t.start()

    def run(self):
        self.keyboard_listener.start()
        self.keyboard_listener.join()

    def join(self):
        self.t.join()

if __name__ == "__main__":
    event = lambda: print('trigger')
    i = input_listener(event)
    i.start()
    i.join()