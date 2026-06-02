"""
recorder.py
-----------
Contient la classe Recorder.
Rôle : écouter les actions souris et/ou clavier via pynput
       et les stocker dans deux listes :
           - self.liste_actions   : liste des actions enregistrées
           - self.liste_delais    : liste des durées entre chaque action (en secondes)

Chaque action est une liste de la forme :
    ['click',    (x, y),        'left'|'right']
    ['scroll',   (x, y),        [dy, dx]]
    ['press',    'char',        caractere]      ← touche normale
    ['press',    'modifier',    nom_touche]     ← touche spéciale (Ctrl, Shift...)
    ['release',  'char',        caractere]
    ['release',  'modifier',    nom_touche]

Méthodes publiques :
    r_mouse()           → enregistre uniquement la souris
    r_keyboard()        → enregistre uniquement le clavier
    r_key_and_mouse()   → enregistre souris + clavier simultanément
    Chacune retourne (liste_actions, liste_delais)
"""

from pynput import mouse, keyboard
from dic_switch import VK_TO_CHAR
import time


class Recorder:

    def __init__(self):
        self.liste_actions = []     # actions enregistrées
        self.liste_delais  = []     # délais entre chaque action
        self.temps_debut   = 0.0    # horodatage du début de l'intervalle en cours
        self.temps_fin     = 0.0    # horodatage de la fin de l'intervalle en cours

        # Contrôleurs (non utilisés en enregistrement, réservés à une future extension)
        self.controleur_souris   = mouse.Controller()
        self.controleur_clavier  = keyboard.Controller()

        # Listeners — recréés à chaque enregistrement dans reset()
        self.listener_souris   = mouse.Listener(
            on_click=self.callback_click,
            on_scroll=self.callback_scroll
        )
        self.listener_clavier  = keyboard.Listener(
            on_press=self.callback_appui_touche,
            on_release=self.callback_relache_touche
        )

    # -----------------------------------------------------------------------
    # reset
    # Remet à zéro les listes et recrée les listeners.
    # Appelé au début de chaque enregistrement pour repartir d'un état propre.
    # Les listeners pynput ne peuvent pas être redémarrés après un stop(),
    # il faut obligatoirement en créer de nouveaux.
    # -----------------------------------------------------------------------
    def reset(self):
        self.liste_actions = []
        self.liste_delais  = []
        self.temps_debut   = 0.0
        self.temps_fin     = 0.0
        self.listener_souris  = mouse.Listener(
            on_click=self.callback_click,
            on_scroll=self.callback_scroll
        )
        self.listener_clavier = keyboard.Listener(
            on_press=self.callback_appui_touche,
            on_release=self.callback_relache_touche
        )

    # -----------------------------------------------------------------------
    # enregistrer_delai
    # Calcule le délai depuis la dernière action et l'ajoute à liste_delais.
    # Appelé à la fin de chaque callback d'action.
    # -----------------------------------------------------------------------
    def enregistrer_delai(self):
        self.temps_fin = time.perf_counter()
        self.liste_delais.append(self.temps_fin - self.temps_debut)
        self.temps_debut = time.perf_counter()

    # -----------------------------------------------------------------------
    # callback_click
    # Appelé par listener_souris à chaque click souris.
    # On n'enregistre que les appuis (pressed=True), pas les relâchements.
    # -----------------------------------------------------------------------
    def callback_click(self, pos_x, pos_y, bouton, est_appuye):
        if est_appuye:
            self.liste_actions.append(['click', (pos_x, pos_y), bouton.name])
            self.enregistrer_delai()

    # -----------------------------------------------------------------------
    # callback_scroll
    # Appelé par listener_souris à chaque mouvement de molette.
    # Logique de regroupement : si le scroll précédent est dans la même zone
    # (±50px) et dans le même sens, on l'additionne au lieu d'en créer un nouveau.
    # Cela évite des dizaines d'entrées pour un seul geste de défilement.
    # -----------------------------------------------------------------------
    def callback_scroll(self, pos_x, pos_y, delta_x, delta_y):
        dernier = self.liste_actions[-1] if self.liste_actions else None
        meme_zone = (
            dernier
            and dernier[0] == 'scroll'
            and dernier[1][0] - 50 < pos_x < dernier[1][0] + 50
            and dernier[1][1] - 50 < pos_y < dernier[1][1] + 50
        )

        if meme_zone:
            # Regroupement vertical
            if delta_y != 0:
                meme_sens_y = (delta_y < 0) == (dernier[2][0] < 0)
                if meme_sens_y:
                    dernier[2][0] += delta_y
                    return  # on regroupe, pas de nouvelle entrée
            # Regroupement horizontal
            elif delta_x != 0:
                meme_sens_x = (delta_x < 0) == (dernier[2][1] < 0)
                if meme_sens_x:
                    dernier[2][1] += delta_x
                    return  # on regroupe, pas de nouvelle entrée

        # Nouveau scroll (zone différente, sens différent, ou premier scroll)
        self.liste_actions.append(['scroll', (pos_x, pos_y), [delta_y, delta_x]])
        self.enregistrer_delai()

    # -----------------------------------------------------------------------
    # callback_appui_touche
    # Appelé par listener_clavier à chaque appui de touche.
    # Distingue deux types :
    #   - 'char'     : touche normale avec un caractère (a, b, 1, é...)
    #   - 'modifier' : touche spéciale (Ctrl, Shift, F1, Entrée...)
    # On évite les répétitions : si la même touche est déjà en cours d'appui
    # (pas encore relâchée), on ne la réenregistre pas.
    # -----------------------------------------------------------------------
    def callback_appui_touche(self, touche):
        derniere_action = self.liste_actions[-1] if self.liste_actions else None

        if hasattr(touche, 'char') and touche.char is not None:
            # Touche normale → on récupère le caractère via VK_TO_CHAR
            # (évite les caractères de contrôle \x03 etc. quand Ctrl est actif)
            caractere = VK_TO_CHAR.get(touche.vk, chr(touche.vk).lower())
            nouvelle_action = ['press', 'char', caractere]

            # On vérifie que ce n'est pas une répétition de la touche encore enfoncée
            deja_enfoncee = (
                derniere_action
                and derniere_action[0] == 'press'
                and derniere_action[2] == caractere
            )
            if not deja_enfoncee:
                self.liste_actions.append(nouvelle_action)
                self.enregistrer_delai()

        elif hasattr(touche, 'name'):
            # Touche spéciale (modificateur, navigation, fonction...)
            nouvelle_action = ['press', 'modifier', touche.name]

            deja_enfoncee = (
                derniere_action
                and derniere_action[0] == 'press'
                and derniere_action[2] == touche.name
            )
            if not deja_enfoncee:
                self.liste_actions.append(nouvelle_action)
                self.enregistrer_delai()

    # -----------------------------------------------------------------------
    # callback_relache_touche
    # Appelé par listener_clavier à chaque relâchement de touche.
    # Enregistre un 'release' pour permettre à l'exécuteur de relâcher
    # les modificateurs au bon moment (ex: relâcher Ctrl après Ctrl+C).
    # -----------------------------------------------------------------------
    def callback_relache_touche(self, touche):
        if hasattr(touche, 'char') and touche.char is not None:
            caractere = VK_TO_CHAR.get(touche.vk, chr(touche.vk).lower())
            self.liste_actions.append(['release', 'char', caractere])
        elif hasattr(touche, 'name'):
            self.liste_actions.append(['release', 'modifier', touche.name])
        self.enregistrer_delai()

    # -----------------------------------------------------------------------
    # stopper_listener
    # Callback utilisé par le listener de pause.
    # Retourne False sur Échap pour débloquer le stopper_var.join().
    # -----------------------------------------------------------------------
    def stopper_listener(self, touche):
        if touche == keyboard.Key.esc:
            return False

    # -----------------------------------------------------------------------
    # r_mouse
    # Lance l'enregistrement de la souris uniquement.
    # L'enregistrement s'arrête quand l'utilisateur appuie sur Échap.
    # Retourne (liste_actions, liste_delais).
    # -----------------------------------------------------------------------
    def r_mouse(self):
        self.reset()
        self.temps_debut = time.perf_counter()
        self.listener_souris.start()

        print("Enregistrement souris... Appuyez sur Échap pour arrêter.")
        with keyboard.Listener(on_press=self.stopper_listener) as stopper_var:
            stopper_var.join()

        self.listener_souris.stop()
        return self.liste_actions, self.liste_delais

    # -----------------------------------------------------------------------
    # r_keyboard
    # Lance l'enregistrement du clavier uniquement.
    # L'enregistrement s'arrête quand l'utilisateur appuie sur Échap.
    # Retourne (liste_actions, liste_delais).
    # -----------------------------------------------------------------------
    def r_keyboard(self):
        self.reset()
        self.temps_debut = time.perf_counter()
        self.listener_clavier.start()

        print("Enregistrement clavier... Appuyez sur Échap pour arrêter.")
        with keyboard.Listener(on_press=self.stopper_listener) as stopper_var:
            stopper_var.join()

        self.listener_clavier.stop()
        return self.liste_actions, self.liste_delais

    # -----------------------------------------------------------------------
    # r_key_and_mouse
    # Lance l'enregistrement du clavier ET de la souris simultanément.
    # L'enregistrement s'arrête quand l'utilisateur appuie sur Échap.
    # Retourne (liste_actions, liste_delais).
    # -----------------------------------------------------------------------
    def r_key_and_mouse(self):
        self.reset()
        self.temps_debut = time.perf_counter()
        self.listener_clavier.start()
        self.listener_souris.start()

        print("Enregistrement clavier + souris... Appuyez sur Échap pour arrêter.")
        with keyboard.Listener(on_press=self.stopper_listener) as stopper_var:
            stopper_var.join()

        self.listener_clavier.stop()
        self.listener_souris.stop()
        return self.liste_actions, self.liste_delais
