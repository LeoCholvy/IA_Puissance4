from copy import deepcopy
import math
from random import randint

# coef: -1 si c'est le coup de l'adversaire
#        1 si c'est le coup de l'IA
def Meilleur_coup(jeu:object,n:int,ia=True, issue = 3):
    """ia est min car la fonction est inversée
    je sais pas pourquoi ca marche"""
    # pour chaque colonne
    n_coups = jeu.L
    if n == 0 or issue in [1,2] :
        if issue == 2:
            #TODO
            if not ia:
                # FIXME support sy change
                return (None, Eval(jeu, "+", "x") + n * 100000)
            else:
                return (None, Eval(jeu, "+", "x") - n * 100000)
        if issue == 1:
            return (None, 0)
        else: #TODO
            return (None, Eval(jeu, "+", "x"))
    
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
            new_score = Meilleur_coup(jeu_virtuel, n-1, not ia,new_issue)[1]
            if new_score > value:
                value = new_score
                coup = [entree]
            elif new_score == value:
                coup.append(entree)
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
            new_score = Meilleur_coup(jeu_virtuel, n-1, not ia,new_issue)[1]
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


def Eval(jeu, ia_sy, p_sy):
    return Evaluation(jeu,ia_sy, p_sy) - Evaluation(jeu, p_sy, ia_sy)

def Evaluation(jeu, g_sy, b_sy) -> int:
    """Fonction qui retourne un score pour un coup"""
    h_max = jeu.hauteur_max
    grille = jeu.grille
    wp = [] # (coord, missing)
    score = 0
    # TODO: une bonne partie des coord est inutile 
    for x in range(h_max, jeu.H):
        for y in range(jeu.L):
            directions = [
                [(x,y), (x,y+1), (x,y+2), (x,y+3)],
                [(x,y), (x+1,y), (x+2,y), (x+3,y)],
                [(x,y), (x+1,y+1), (x+2,y+2), (x+3,y+3)],
                [(x,y), (x+1,y-3), (x+2,y-3), (x+3,y-3)]
            ]
            for dir in directions:
                n = 0
                for i,j in dir:
                    if not(0 <= i and i < jeu.H and 0 <= j and j < jeu.L):
                        n = -1
                        break
                    jeton = grille[i][j]
                    if jeton == b_sy:
                        n = -1
                        break
                    if jeton == g_sy:
                        n += 1
                        continue
                    if jeton == 0:
                        coord = (i,j)
                if n == -1:
                    continue
                elif n == 4:
                    score += 10000000
                elif n == 3:
                    score += 10000
                    if Under_wp(coord, wp):
                        score += 100000
                    if not coord in wp:
                        score += 50000
                        wp.append (coord)
                elif n == 2:
                    score += 100
                elif n == 1:
                    score += 1
    return score

def Under_wp(coord, wp):
    on = (coord[0]-1, coord[1])
    for i in wp:
        if i == on:
            return True
        if i[0] == coord[0]:
            return False
    return False
                
            


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