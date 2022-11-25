# TODO: Projet XD
# Branche "main": code testé et fonctionnel uniquement, Ne pas entrainer d'IA dans cette branche

from Jeu import Puissance4 as P4

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
        JEU.Play(1)