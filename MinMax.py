from copy import deepcopy
import math
from random import randint

# coef: -1 si c'est le coup de l'adversaire
#        1 si c'est le coup de l'IA
def Meilleur_coup(jeu:object,n:int,ia=True, val = 0, issue = 3):
    """ia est min car la fonction est inversée
    je sais pas pourquoi ca marche"""
    # pour chaque colonne
    n_coups = jeu.L
    if n == 0 or issue in [1,2] :
        if issue == 2:
            if not ia:
                return (None, val + n * 100000)
            else:
                return (None, val - n * 100000)
        if issue == 1:
            return (None, 0)
        else:
            return (None, val)
    
    # max
    if ia:
        value = -math.inf
        coups_possibles = []
        coup = []
        for entree in range(n_coups):
            jeu_virtuel = deepcopy(jeu)
            jeu_virtuel.console = False
            new_issue = jeu_virtuel.Play(entree)
            if new_issue == -1:
                continue
            coups_possibles.append(entree)
            new_score = Meilleur_coup(jeu_virtuel, n-1, not ia, val+Evaluation(jeu_virtuel,n,entree),new_issue)[1]
            if new_score > value:
                value = new_score
                coup = [entree]
            elif new_score == value:
                coup.append(entree)
        if n == 5:
            print(coup, value)
            print(jeu_virtuel.missing)
        if coup == []:
            coup = coups_possibles[randint(0,len(coups_possibles)-1)]
        else:
            coup = coup[randint(0,len(coup)-1)]
        return coup, value
    # min
    else:
        value = math.inf
        coups_possibles = []
        coup = []
        for entree in range(n_coups):
            jeu_virtuel = deepcopy(jeu)
            jeu_virtuel.console = False
            new_issue = jeu_virtuel.Play(entree)
            if new_issue == -1:
                continue
            coups_possibles.append(entree)
            new_score = Meilleur_coup(jeu_virtuel, n-1, not ia, val-Evaluation(jeu_virtuel,n,entree),new_issue)[1]
            if new_score < value:
                value = new_score
                coup = [entree]
            if new_score == value:
                coup.append(entree)
        if coup == []:
            coup = coups_possibles[randint(0,len(coups_possibles)-1)]
        else:
            coup = coup[randint(0,len(coup)-1)]
        return coup, value
        

def Evaluation(jeu,n,y) -> int:
    """Fonction qui retourne un score pour un coup"""
    alignes = jeu.a
    missing = jeu.missing
    score = 0
    if y == 3:
        score += n
    # elif y in [2,4]:
    #     score += n
    for i in alignes:
        score += i*n
    for i in missing:
        # if i == 2:
        #     score += 10*n
        if i == 1:
            score += 100*n
    return score


# function minimax(node, depth, maximizingPlayer) is
#     if depth = 0 or node is a terminal node then
#         return the heuristic value of node
#     if maximizingPlayer then
#         value := −∞
#         for each child of node do
#             value := max(value, minimax(child, depth − 1, FALSE))
#     else (* minimizing player *)
#         value := +∞
#         for each child of node do
#             value := min(value, minimax(child, depth − 1, TRUE))
#     return value