"""
action.py
---------
Contient la classe Executor.
Rôle : rejouer une liste d'actions enregistrées par Recorder,
       avec ou sans respect des délais entre les actions.

Méthodes publiques :
    action_mouse(liste_actions, liste_delais=None)
    action_keyboard(liste_actions, liste_delais=None)
    action_key_and_mouse(liste_actions, liste_delais=None)

    liste_delais=None  → exécution sans pause entre les actions
    liste_delais=liste → exécution en respectant les délais enregistrés

L'exécution tourne en boucle jusqu'à ce que l'utilisateur appuie sur Échap.
"""

from pynput import mouse, keyboard
from dic_switch import KEY_NAME_TO_KEY
import time


class Executor:

    def __init__(self):
        self.controleur_souris  = mouse.Controller()
        self.controleur_clavier = keyboard.Controller()

        self.boucle_active  = True   # False = l'exécution s'arrête après le tour en cours
        self.index_action   = 0      # position dans la liste d'actions en cours de lecture
        self.delai_median   = None   # délai de substitution utilisé quand index=0 avec délais

        # Listener d'arrêt — recréé dans reset() avant chaque exécution
        self.listener_stop  = keyboard.Listener(on_press=self.callback_stop)

    # -----------------------------------------------------------------------
    # reset
    # Remet à zéro l'état de l'exécuteur et recrée le listener d'arrêt.
    # liste_delais_brute : la liste originale des délais (peut être None)
    #   → si fournie, calcule delai_median = médiane sans le premier délai
    #     (le premier délai est le temps avant la 1ère action, pas entre deux actions)
    # -----------------------------------------------------------------------
    def reset(self, liste_delais_brute=None):
        self.boucle_active = True
        self.index_action  = 0
        self.delai_median  = None
        self.listener_stop = keyboard.Listener(on_press=self.callback_stop)

        if liste_delais_brute:
            # On retire le premier délai (temps d'attente avant la 1ère action)
            # puis on trie pour trouver la médiane — utilisée quand on revient à index=0
            delais_sans_premier = sorted(liste_delais_brute[1:])
            if delais_sans_premier:
                self.delai_median = delais_sans_premier[len(delais_sans_premier) // 2]

    # -----------------------------------------------------------------------
    # callback_stop
    # Callback du listener d'arrêt.
    # Passe boucle_active à False pour sortir de la boucle d'exécution.
    # -----------------------------------------------------------------------
    def callback_stop(self, touche):
        if touche == keyboard.Key.esc:
            print("Arrêt de l'exécution.")
            self.boucle_active = False

    # -----------------------------------------------------------------------
    # appliquer_delai
    # Applique le délai avant l'action courante si liste_delais est fournie.
    # À index=0 (retour au début de la boucle), on utilise delai_median
    # car le délai[0] correspond au temps avant la 1ère action, pas entre actions.
    # -----------------------------------------------------------------------
    def appliquer_delai(self, liste_delais):
        if liste_delais is None:
            return
        if self.index_action == 0 and self.delai_median is not None:
            time.sleep(self.delai_median)
        elif self.index_action > 0:
            time.sleep(liste_delais[self.index_action])

    # -----------------------------------------------------------------------
    # executer_action_souris
    # Rejoue une action souris : click ou scroll.
    # Format attendu :
    #   ['click',  (x, y), 'left'|'right']
    #   ['scroll', (x, y), [dy, dx]]
    # -----------------------------------------------------------------------
    def executer_action_souris(self, action):
        type_action = action[0]
        position    = action[1]

        if type_action == 'click':
            self.controleur_souris.position = position
            bouton = mouse.Button.left if action[2] == 'left' else mouse.Button.right
            self.controleur_souris.click(bouton, 1)

        elif type_action == 'scroll':
            self.controleur_souris.position = position
            self.controleur_souris.scroll(action[2][1], action[2][0])  # (dx, dy)

    # -----------------------------------------------------------------------
    # executer_action_clavier
    # Rejoue une action clavier : appui ou relâchement d'une touche.
    # Format attendu :
    #   ['press',   'char',     caractere]
    #   ['press',   'modifier', nom_touche]
    #   ['release', 'char',     caractere]
    #   ['release', 'modifier', nom_touche]
    # -----------------------------------------------------------------------
    def executer_action_clavier(self, action):
        type_action  = action[0]   # 'press' ou 'release'
        type_touche  = action[1]   # 'char' ou 'modifier'
        valeur       = action[2]   # caractère ou nom de touche spéciale

        # Récupère l'objet pynput correspondant à la touche
        if type_touche == 'modifier':
            touche_pynput = KEY_NAME_TO_KEY.get(valeur)
            if touche_pynput is None:
                return  # touche inconnue, on passe
        else:
            touche_pynput = valeur  # pour les chars, pynput accepte directement la str

        if type_action == 'press':
            self.controleur_clavier.press(touche_pynput)
        elif type_action == 'release':
            self.controleur_clavier.release(touche_pynput)

    # -----------------------------------------------------------------------
    # action_mouse
    # Rejoue en boucle une liste d'actions souris.
    # Appuyez sur Échap pour arrêter.
    # liste_delais=None → sans pause / liste_delais=liste → avec pauses enregistrées
    # -----------------------------------------------------------------------
    def action_mouse(self, liste_actions, liste_delais=None):
        self.reset(liste_delais)
        self.listener_stop.start()

        print("Exécution souris... Appuyez sur Échap pour arrêter.")
        while self.boucle_active:
            self.appliquer_delai(liste_delais)
            self.executer_action_souris(liste_actions[self.index_action])
            self.index_action = (self.index_action + 1) % len(liste_actions)

        self.listener_stop.stop()

    # -----------------------------------------------------------------------
    # action_keyboard
    # Rejoue en boucle une liste d'actions clavier.
    # Appuyez sur Échap pour arrêter.
    # -----------------------------------------------------------------------
    def action_keyboard(self, liste_actions, liste_delais=None):
        self.reset(liste_delais)
        self.listener_stop.start()

        print("Exécution clavier... Appuyez sur Échap pour arrêter.")
        while self.boucle_active:
            self.appliquer_delai(liste_delais)
            self.executer_action_clavier(liste_actions[self.index_action])
            self.index_action = (self.index_action + 1) % len(liste_actions)

        self.listener_stop.stop()

    # -----------------------------------------------------------------------
    # action_key_and_mouse
    # Rejoue en boucle une liste mixte d'actions souris et clavier.
    # Chaque action est routée vers executer_action_souris ou executer_action_clavier
    # selon son type ('click', 'scroll' → souris / 'press', 'release' → clavier).
    # -----------------------------------------------------------------------
    def action_key_and_mouse(self, liste_actions, liste_delais=None):
        self.reset(liste_delais)
        self.listener_stop.start()

        # Types d'actions qui concernent la souris
        TYPES_SOURIS  = {'click', 'scroll'}
        # Types d'actions qui concernent le clavier
        TYPES_CLAVIER = {'press', 'release'}

        print("Exécution clavier + souris... Appuyez sur Échap pour arrêter.")
        while self.boucle_active:
            action = liste_actions[self.index_action]
            self.appliquer_delai(liste_delais)

            if action[0] in TYPES_SOURIS:
                self.executer_action_souris(action)
            elif action[0] in TYPES_CLAVIER:
                self.executer_action_clavier(action)

            self.index_action = (self.index_action + 1) % len(liste_actions)

        self.listener_stop.stop()
