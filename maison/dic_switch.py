"""
Ficher personnel non retravaillé
"""

from pynput import keyboard


VK_TO_CHAR = {
    # Lettres
    65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e',
    70: 'f', 71: 'g', 72: 'h', 73: 'i', 74: 'j',
    75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o',
    80: 'p', 81: 'q', 82: 'r', 83: 's', 84: 't',
    85: 'u', 86: 'v', 87: 'w', 88: 'x', 89: 'y',
    90: 'z',

    # Chiffres (AZERTY)
    48: 'à', 49: '&', 50: 'é', 51: '"', 52: "'",
    53: '(', 54: '-', 55: 'è', 56: '_', 57: 'ç',

    # Pavé numérique
    96: '0', 97: '1', 98: '2', 99: '3', 100: '4',
    101: '5', 102: '6', 103: '7', 104: '8', 105: '9',
    106: '*', 107: '+', 109: '-', 110: '.', 111: '/',

    # Caractères spéciaux AZERTY français
    186: '$', 187: '=', 188: ',', 189: '-', 190: ';',
    191: ':', 192: 'ù', 219: ')', 220: '*', 221: '^',
    222: '²', 223: '!', 226: '<',

    # Caractères spéciaux QWERTY (pour référence)
    # 186: ';', 187: '=', 188: ',', 189: '-', 190: '.',
    # 191: '/', 192: '`', 219: '[', 220: '\\', 221: ']',
    # 222: "'",
}

KEY_NAME_TO_KEY = {
    # Modificateurs
    'shift':    keyboard.Key.shift,
    'shift_l':  keyboard.Key.shift_l,
    'shift_r':  keyboard.Key.shift_r,
    'ctrl_l':   keyboard.Key.ctrl_l,
    'ctrl_r':   keyboard.Key.ctrl_r,
    'alt_l':    keyboard.Key.alt_l,
    'alt_r':    keyboard.Key.alt_r,
    'alt_gr':   keyboard.Key.alt_gr,
    'cmd':      keyboard.Key.cmd,
    'cmd_r':    keyboard.Key.cmd_r,

    # Navigation
    'up':        keyboard.Key.up,
    'down':      keyboard.Key.down,
    'left':      keyboard.Key.left,
    'right':     keyboard.Key.right,
    'home':      keyboard.Key.home,
    'end':       keyboard.Key.end,
    'page_up':   keyboard.Key.page_up,
    'page_down': keyboard.Key.page_down,
    'insert':    keyboard.Key.insert,
    'delete':    keyboard.Key.delete,

    # Touches de contrôle
    'backspace': keyboard.Key.backspace,
    'tab':       keyboard.Key.tab,
    'enter':     keyboard.Key.enter,
    'esc':       keyboard.Key.esc,
    'space':     keyboard.Key.space,
    'caps_lock': keyboard.Key.caps_lock,

    # Touches de fonction
    'f1':  keyboard.Key.f1,  'f2':  keyboard.Key.f2,
    'f3':  keyboard.Key.f3,  'f4':  keyboard.Key.f4,
    'f5':  keyboard.Key.f5,  'f6':  keyboard.Key.f6,
    'f7':  keyboard.Key.f7,  'f8':  keyboard.Key.f8,
    'f9':  keyboard.Key.f9,  'f10': keyboard.Key.f10,
    'f11': keyboard.Key.f11, 'f12': keyboard.Key.f12,

    # Média
    'media_play_pause': keyboard.Key.media_play_pause,
    'media_next':       keyboard.Key.media_next,
    'media_previous':   keyboard.Key.media_previous,
    'media_volume_up':  keyboard.Key.media_volume_up,
    'media_volume_down':keyboard.Key.media_volume_down,
    'media_volume_mute':keyboard.Key.media_volume_mute,
}

