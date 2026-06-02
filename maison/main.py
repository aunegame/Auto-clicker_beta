"""
Ficher personnel non retravaillé
"""

from menu import choice_menu
from recorder import Recorder
from action import Executor


# Variables usuels
recorder_module = Recorder()
action_module = Executor() # todo : Déja rempli
recorded_mode, ch1, ch2 = 0, 0, 0
recorded_list = []
pause_list = []
last_record = 0
FONCTIONS_SWITCH = {
    1: {1: recorder_module.r_mouse,                 # TODO: record_mouse()
        2: action_module.action_mouse},           # TODO: execute_mouse()

    2: {1: recorder_module.r_keyboard,              # TODO: record_keyboard()
        2: action_module.action_keyboard},          # TODO: execute_keyboard()

    3: {1: recorder_module.r_key_and_mouse,         # TODO: record_mouse_and_keyboard()
        2: action_module.action_key_and_mousse}   # TODO: execute_mouse_and_keyboard()
}

if __name__ == '__main__':
    while True:
        ch1, ch2, ch3 = choice_menu()
        if ch2 == 1:
            last_record = ch1
            recorded_list, pause_list = FONCTIONS_SWITCH[ch1][ch2]()
        elif ch2 == 2:
            if ch1 != last_record:
                print("La liste n'es pas enregisté")
                input("press entrer pour enregistrer")
                last_record = ch1
                recorded_list, pause_list = FONCTIONS_SWITCH[ch1][ch2]()
            if ch3 == 1:
                FONCTIONS_SWITCH[ch1][ch2](recorded_list, pause_list)
            elif ch3 == 2:
                FONCTIONS_SWITCH[ch1][ch2](recorded_list)
            else:
                print("Error")