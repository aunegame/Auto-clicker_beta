"""
menu.py
-------
Gestion de la navigation dans les menus console de l'auto clicker.

Fonction publique :
    choice_menu() → retourne (categorie, action, option)
        categorie : 1=Souris  2=Clavier  3=Clavier+Souris
        action    : 1=Enregistrer  2=Exécuter
        option    : 1=Avec pause   2=Sans pause   0=non applicable (si action=Enregistrer)
"""


# ---------------------------------------------------------------------------
# Fonctions d'affichage des menus
# Chaque fonction affiche son menu et retourne le choix saisi (str).
# ---------------------------------------------------------------------------

def afficher_menu_principal():
    print("\n=== AUTO CLICKER ===")
    print("1 - Souris")
    print("2 - Clavier")
    print("3 - Clavier + Souris")
    print("0 - Quitter")
    return input("Votre choix : ").strip()


def afficher_menu_souris():
    print("\n--- Souris ---")
    print("1 - Enregistrer")
    print("2 - Exécuter")
    print("0 - Retour")
    return input("Votre choix : ").strip()


def afficher_menu_clavier():
    print("\n--- Clavier ---")
    print("1 - Enregistrer")
    print("2 - Exécuter")
    print("0 - Retour")
    return input("Votre choix : ").strip()


def afficher_menu_clavier_souris():
    print("\n--- Clavier + Souris ---")
    print("1 - Enregistrer")
    print("2 - Exécuter")
    print("0 - Retour")
    return input("Votre choix : ").strip()


def afficher_menu_execution(label_categorie):
    """
    Menu de choix du mode d'exécution.
    label_categorie : str affiché dans le titre (ex: 'Souris', 'Clavier'...)
    """
    print(f"\n--- Exécuter {label_categorie} ---")
    print("1 - Avec pause")
    print("2 - Sans pause")
    print("0 - Retour")
    return input("Votre choix : ").strip()


# ---------------------------------------------------------------------------
# Dictionnaires de routage
#   SWITCH_MENU_CATEGORIE : choix principal → fonction d'affichage du sous-menu
#   SWITCH_LABEL_CATEGORIE: choix principal → label lisible (pour afficher_menu_execution)
# ---------------------------------------------------------------------------

SWITCH_MENU_CATEGORIE = {
    '1': afficher_menu_souris,
    '2': afficher_menu_clavier,
    '3': afficher_menu_clavier_souris,
}

SWITCH_LABEL_CATEGORIE = {
    '1': 'Souris',
    '2': 'Clavier',
    '3': 'Clavier + Souris',
}


# ---------------------------------------------------------------------------
# choice_menu
# Boucle de navigation principale.
# Retourne (categorie, action, option) sous forme d'entiers.
#   categorie : 1=Souris  2=Clavier  3=Clavier+Souris
#   action    : 1=Enregistrer  2=Exécuter
#   option    : 1=Avec pause   2=Sans pause   0=non applicable
# ---------------------------------------------------------------------------

def choice_menu():

    # --- Niveau 1 : menu principal ---
    while True:
        choix_categorie = afficher_menu_principal()

        if choix_categorie == '0':
            print("Au revoir !")
            return 0, 0, 0

        if choix_categorie not in SWITCH_MENU_CATEGORIE:
            print("Choix invalide.")
            continue
        break  # choix valide, on descend au niveau 2

    # --- Niveau 2 : Enregistrer ou Exécuter ---
    while True:
        choix_action = SWITCH_MENU_CATEGORIE[choix_categorie]()

        if choix_action == '0':
            # Retour → on relance depuis le niveau 1
            return choice_menu()

        if choix_action == '1':
            # Enregistrer → pas de niveau 3
            return int(choix_categorie), int(choix_action), 0

        if choix_action == '2':
            # Exécuter → on descend au niveau 3
            break

        print("Choix invalide.")

    # --- Niveau 3 : Avec pause ou Sans pause ---
    while True:
        label = SWITCH_LABEL_CATEGORIE[choix_categorie]
        choix_option = afficher_menu_execution(label)

        if choix_option == '0':
            # Retour → on relance depuis le niveau 1
            return choice_menu()

        if choix_option in ('1', '2'):
            return int(choix_categorie), int(choix_action), int(choix_option)

        print("Choix invalide.")
