from copy import deepcopy
from random import randint

# ia: si c'est l'ia qui joue ou non
# ici: si True le score pour une victoire et positif
#      si False, il est negatif
def Meilleur_coup(jeu:object,n:int):
    # pour chaque colonne
    max = (None, 0)
    pow = jeu.pow
    # (entree, score)
    for entree in range (pow):
        pow=jeu.pow
        pos = jeu.Get_position(entree)
        # si le coup n'est pas valide
        if pos == -1:
            continue
        # si le coup donne match nul
        jeu_virtuel = deepcopy(jeu)
        jeu_virtuel.console = False
        issue = jeu_virtuel.Play(entree)
        if issue == 1:
            score = 0
            continue    
        # si le coup donne une victoire
        elif issue == 2:
            score = n * 1000

        # score du coup en fonction des coups possibles ensuite
        elif issue == 0:
            # remplacer 0 par le score du coup avec la fonction d'évaluation
            if n == 0:
                score = 0
            else:
                score = 0 - Meilleur_coup(jeu_virtuel, n-1)[1]

        # meilleur coup
        if max[1] < score:
            max = (entree, score)
    if max[0] == None:
        max = (randint(0,pow), 0)
    return max

def Evaluation(jeu, x, y) -> int:
    """Fonction qui retourne un score pour un coup"""
    pass
    # score pour nombre pions alignés
    # score pour pions suivis
    # score pour empecher un coup