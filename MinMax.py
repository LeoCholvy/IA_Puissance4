from copy import deepcopy
from random import randint

# ia: si c'est l'ia qui joue ou non
# ici: si True le score pour une victoire et positif
#      si False, il est negatif
def Meilleur_coup(jeu:object,n:int, ia = True, val=0):
    # pour chaque colonne
    coups = []
    n_coups = jeu.L
    minmax = []
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
            if ia:
                score = val + n * 1000
            else:    
                score = val - n * 1000

        # score du coup en fonction des coups possibles ensuite
        elif issue == 0:
            # remplacer 0 par le score du coup avec la fonction d'évaluation
            if n == 0:
                score = val
            else:
                # score du coup
                eval = Evaluation(jeu_virtuel,n)
                if not ia:
                    eval = -eval
                e, score = Meilleur_coup(jeu_virtuel,n-1,not ia,val+eval)
        minmax . append((entree,score))
        if score == 0: print(entree,score,n, ia, val)
    if n==3:
        print(minmax)
    #max
    # if ia:
    #     minmax = sorted(minmax,key=lambda coup: coup[1], reverse=True)
    #     max = minmax[0][1]
    #     minmax = list(filter(lambda coup: coup[1] == max, minmax))
    # #min
    # else:
    minmax = sorted(minmax,key=lambda coup: coup[1], reverse=True)
    min = minmax[0][1]
    minmax = list(filter(lambda coup: coup[1] == min, minmax))
    # si aucun coups possibles
    if minmax == []:
        # print('wtf --------------------------------')
        return (randint(2,4),0)
    return minmax[randint(0,len(minmax)-1)]
def Evaluation(jeu,n) -> int:
    """Fonction qui retourne un score pour un coup"""
    alignes = jeu.a
    score = 0
    for i in alignes:
        score += i
    return score*10*n