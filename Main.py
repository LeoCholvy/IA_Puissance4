# TODO: Projet XD
# Branche "main": code testé et fonctionnel uniquement, Ne pas entrainer d'IA dans cette branche

from Jeu import Puissance4 as P4
from MinMax import Meilleur_coup
from colorama import Fore
from colorama import Style

# Test MinMax
# init jeu
JEU = P4(j=[
    {"nom": "Joueur", "symbole": "x"},
    {"nom": "Algo_MinMax","symbole": "+"}
])
JEU.Start(j=0)

VICTOIRE = False
while not VICTOIRE in [1,2]:
    nom = JEU.Get_name_current_player()

    if nom == "Joueur":
        JEU.Affiche()
        try:
            entree = int(input("Entrez la colonne (0 à 6):\n>>>"))
        except:
            continue
        VICTOIRE = JEU.Play(entree)
    else:
        entree, score = Meilleur_coup(JEU,6)
        print(f"L'ia joue {entree}, ce coup a un score de {score}")
        VICTOIRE = JEU.Play(entree) 
JEU.Affiche()