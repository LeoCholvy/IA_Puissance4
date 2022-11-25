# TODO: Projet XD
# Branche "main": code testé et fonctionnel uniquement, Ne pas entrainer d'IA dans cette branche

from Jeu import Puissance4 as P4
from MinMax import Meilleur_coup as Mc
from colorama import Fore
from colorama import Style

# Test MinMax
# init jeu
JEU = P4(j=[
    {"nom": "Joueur", "symbole": "x"},
    {"nom": "Algo_MinMax","symbole": "+"}
])
JEU.Start()

VICTOIRE = False
while not VICTOIRE:
    nom = JEU.Get_name_current_player()

    if nom == "Joueur":
        JEU.Affiche()
        entree = int(input("Entrez la colonne (0 à 6):\n>>>"))
        VICTOIRE = JEU.Play(entree)
    else:
        entree, score = Mc(JEU, 6)
        if score == 0:
            print(f"Le score du coup '{entree}' {Fore.RED}{score}{Style.RESET_ALL}")
        else:
            print(f"Le score du coup '{entree}' {score}")
        VICTOIRE = JEU.Play(entree) 