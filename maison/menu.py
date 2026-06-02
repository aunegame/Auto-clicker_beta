"""
Ficher personnel non retravaillé
"""

# ---------------------------------------------------------------------------
# Fonctions de menu
# ---------------------------------------------------------------------------

def menu_principal():
    print("\n=== AUTO CLICKER ===")
    print("1 - Souris")
    print("2 - Clavier")
    print("3 - Clavier + Souris")
    print("0 - Quitter")
    return input("Votre choix : ").strip()


def menu_souris():
    print("\n--- Souris ---")
    print("1 - Enregistrer")
    print("2 - Exécuter")
    print("0 - Retour")
    return input("Votre choix : ").strip()


def menu_clavier():
    print("\n--- Clavier ---")
    print("1 - Enregistrer")
    print("2 - Exécuter")
    print("0 - Retour")
    return input("Votre choix : ").strip()


def menu_clavier_souris():
    print("\n--- Clavier + Souris ---")
    print("1 - Enregistrer")
    print("2 - Exécuter")
    print("0 - Retour")
    return input("Votre choix : ").strip()


def menu_exe(choix):
    print(f"Executer {choix}")
    print("1 - Avec pause")
    print("2 - Sans pause")
    print("0 - Retour")
    return input("Votre choix : ").strip()


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------
def choice_menu():
    state = 1
    choix1 = choix2 = choix3 = '0'
    while True:
        if state == 1:
            choix1 = menu_principal()
            state += 1
        elif state == 2:
            if choix1 == '0':
                print("Au revoir")
                break
                # return 0, 0, 0
            elif choix1 == '1':
                choix2 = menu_souris()
                state += 1
            elif choix1 == '2':
                choix2 = menu_clavier()
                state += 1
            elif choix1 == '3':
                choix2 = menu_clavier_souris()
                state += 1
            else:
                print("Erreur de séléction")
                state -= 1
        elif state == 3:
            if choix2 == '0':
                state -= 2
            elif choix2 == '1':
                break
                # return choix1, choix2, 0
            elif choix2 == '2':
                choix3 = menu_exe(DIC_CHOIX[choix1])
                if choix3 == '1' or choix3 == '2':
                    break
                    # return choix1, choix2, choix3
                elif choix3 == '0':
                    state -= 1
                else:
                    print("choix incorrect")
            else:
                print("choix incorrect")
                state -= 1
    return int(choix1), int(choix2), int(choix3)