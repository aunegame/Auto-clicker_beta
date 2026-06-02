"""
main.py
-------
Point d'entrée de l'auto clicker.
Orchestre le menu, l'enregistrement et l'exécution.

Flux principal :
    1. choice_menu()  → l'utilisateur choisit ce qu'il veut faire
    2. Si action=Enregistrer → on enregistre et on stocke le résultat
    3. Si action=Exécuter    → on rejoue ce qui a été enregistré
                               (avec ou sans délais selon choix_option)
"""

from menu     import choice_menu
from recorder import Recorder
from action   import Executor


# ---------------------------------------------------------------------------
# Initialisation des modules
# ---------------------------------------------------------------------------

module_enregistrement = Recorder()   # gère l'écoute et le stockage des actions
module_execution      = Executor()   # gère le rejeu des actions enregistrées


# ---------------------------------------------------------------------------
# Variables de session
# ---------------------------------------------------------------------------

liste_actions_enregistrees = []   # actions enregistrées lors du dernier enregistrement
liste_delais_enregistres   = []   # délais enregistrés lors du dernier enregistrement
derniere_categorie         = 0    # catégorie du dernier enregistrement (1, 2 ou 3)
                                  # permet de détecter si on essaie d'exécuter
                                  # une liste enregistrée dans une autre catégorie


# ---------------------------------------------------------------------------
# Dictionnaire de routage des fonctions d'enregistrement
#   clé : categorie (1=Souris, 2=Clavier, 3=Clavier+Souris)
#   valeur : méthode à appeler sur module_enregistrement
# ---------------------------------------------------------------------------

SWITCH_ENREGISTREMENT = {
    1: module_enregistrement.r_mouse,
    2: module_enregistrement.r_keyboard,
    3: module_enregistrement.r_key_and_mouse,
}


# ---------------------------------------------------------------------------
# Dictionnaire de routage des fonctions d'exécution
#   clé : categorie (1=Souris, 2=Clavier, 3=Clavier+Souris)
#   valeur : méthode à appeler sur module_execution
# ---------------------------------------------------------------------------

SWITCH_EXECUTION = {
    1: module_execution.action_mouse,
    2: module_execution.action_keyboard,
    3: module_execution.action_key_and_mouse,
}


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    while True:
        choix_categorie, choix_action, choix_option = choice_menu()

        # Quitter
        if choix_categorie == 0:
            break

        # --- Action = Enregistrer ---
        if choix_action == 1:
            derniere_categorie = choix_categorie
            liste_actions_enregistrees, liste_delais_enregistres = (
                SWITCH_ENREGISTREMENT[choix_categorie]()
            )

        # --- Action = Exécuter ---
        elif choix_action == 2:

            # Vérification : la liste enregistrée correspond-elle à la catégorie choisie ?
            if choix_categorie != derniere_categorie:
                print("Aucun enregistrement disponible pour cette catégorie.")
                print("Lancement de l'enregistrement...")
                derniere_categorie = choix_categorie
                liste_actions_enregistrees, liste_delais_enregistres = (
                    SWITCH_ENREGISTREMENT[choix_categorie]()
                )

            # Exécution avec délais (option 1)
            if choix_option == 1:
                SWITCH_EXECUTION[choix_categorie](
                    liste_actions_enregistrees,
                    liste_delais_enregistres
                )

            # Exécution sans délais (option 2)
            elif choix_option == 2:
                SWITCH_EXECUTION[choix_categorie](
                    liste_actions_enregistrees
                )

            else:
                print("Erreur : option d'exécution invalide.")
