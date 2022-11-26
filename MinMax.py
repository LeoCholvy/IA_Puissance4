from copy import deepcopy
from random import randint

# ia: si c'est l'ia qui joue ou non
# ici: si True le score pour une victoire et positif
#      si False, il est negatif
def Meilleur_coup(jeu:object,n:int, ia = True):
    # pour chaque colonne
    coups = []
    n_coups = jeu.L
    # (entree, score)
    for entree in range (n_coups):
        jeu_virtuel = deepcopy(jeu)
        jeu_virtuel.console = False
        issue = jeu_virtuel.Play(entree)
        # si le coup n'est pas valide
        if issue == -1:
            continue
        # si le coup donne match nul
        elif issue == 1:
            score = 0
        # si le coup donne une victoire
        elif issue == 2:
            score = n * 1000

        # score du coup en fonction des coups possibles ensuite
        elif issue == 0:
            # remplacer 0 par le score du coup avec la fonction d'évaluation
            if n == 0:
                score = 0
            else:
                # score du coup
                pass
    return # entree meilleur coup + min max
def Evaluation(jeu, x, y) -> int:
    """Fonction qui retourne un score pour un coup"""
    pass
    # score pour nombre pions alignés
    # score pour pions suivis
    # score pour empecher un coup0