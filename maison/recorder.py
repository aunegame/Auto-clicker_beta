"""
Ficher personnel non retravaillé
"""

from pynput import mouse
from pynput import keyboard
from dic_switch import VK_TO_CHAR
import time


class Recorder:
    def __init__(self):
        # Définition des variables
        self.record = []
        self.time_between = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def reset(self):
        self.record = []
        self.time_between = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def time_count(self):
        self.end_time = time.perf_counter()
        self.time_between.append(self.end_time - self.start_time)
        self.start_time = time.perf_counter()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.record.append(['click', (x, y), button.name])
            self.time_count()

    def on_scroll(self, x, y, dx, dy):  # Effectuer verifications du scroll au pad (CF: Brouillon)
        if self.record and self.record[-1][0] == 'scroll':
            oX, oY = self.record[-1][1]
            if oX-50 < x < oX+50 and oY-50 < y < oY+50:
                if dy != 0:
                    if dy < 0 and self.record[-1][2][0] < 0:
                        self.record[-1][2][0] += dy
                    elif dy > 0 and self.record[-1][2][0] > 0:
                        self.record[-1][2][0] += dy
                    else:
                        self.record.append(['scroll', (x, y), [dy, dx]])
                        self.time_count()
                elif dx != 0:
                    if dx < 0 and self.record[-1][3][1] < 0:
                        self.record[-1][3][1] += dx
                    elif dx > 0 and self.record[-1][3][1] > 0:
                        self.record[-1][3][1] += dx
                    else:
                        self.record.append(['scroll', (x, y), [dy, dx]])
                        self.time_count()
                else:
                    self.record.append(['scroll', (x, y), [dy, dx]])
                    self.time_count()
            else:
                self.record.append(['scroll', (x, y), [dy, dx]])
                self.time_count()
        else:
            self.record.append(['scroll', (x, y), [dy, dx]])
            self.time_count()
        # print(self.record)

    def on_press(self, key):
        if self.record:
            if hasattr(key, 'char'):
                char = VK_TO_CHAR.get(key.vk, chr(key.vk).lower())
                if char != self.record[-1][1] or (self.record[-1] == ['release', 'char', char]):
                    self.record.append(['press', 'char', char])
                    self.time_count()
            elif hasattr(key, 'name'):
                if key.name != self.record[-1][1] or (self.record[-1] == ['release', 'modifier', key.name]):
                    self.record.append(['press', 'modifier', key.name])
                    self.time_count()
        else:
            if hasattr(key, 'char'):
                char = VK_TO_CHAR.get(key.vk, chr(key.vk).lower())
                self.record.append(['press', 'char', char])
                self.time_count()
            else:
                self.record.append(['press', 'modifier', key.name])
                self.time_count()

    def on_release(self, key):
        if hasattr(key, 'char'):
            char = VK_TO_CHAR.get(key.vk, chr(key.vk).lower())
            self.record.append(['release', 'char', char])
            self.time_count()
        else:
            self.record.append(['release', 'modifier', key.name])
            self.time_count()

    def stopper(self, key):
        if key == keyboard.Key.esc:
            return False

    def r_mouse(self):
        self.reset()
        # Activation du listener souris
        self.start_time = time.perf_counter()
        self.mouse_listener.start()
        # Temporisation avec listener clavier
        print("Recording mouse... \nPress esc to continue:")
        with keyboard.Listener(on_press=self.stopper) as stopper_var:
            stopper_var.join()
        self.mouse_listener.stop()
        return self.record, self.time_between

    def r_keyboard(self):
        self.reset()
        # Activation du listener keyboard
        self.start_time = time.perf_counter()
        self.keyboard_listener.start()
        # Temporisation avec le clavier
        print("Recording keyboard... \nPress esc to continue:")
        with keyboard.Listener(on_press=self.stopper) as stopper_var:
            stopper_var.join()
        self.keyboard_listener.stop()
        return self.record, self.time_between

    def r_key_and_mouse(self):
        self.reset()
        # Activation des listeners
        self.start_time = time.perf_counter()
        self.keyboard_listener.start()
        self.mouse_listener.start()
        # Temporisation avec le clavier
        print("Recording both... \npress esc to continue")
        with keyboard.Listener(on_press=self.stopper) as stopper_var:
            stopper_var.join()
        self.keyboard_listener.stop()
        return self.record, self.time_between

ecoute = Recorder()

print(ecoute.r_key_and_mouse())