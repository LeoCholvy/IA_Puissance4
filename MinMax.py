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
                score = 0 - Meilleur_coup(jeu_virtuel, n-1, not ia)[2]
        coups . append ((entree, score))
    # si aucun coup n'est possible, jouer aléatoirement
    # normalement ce n'est pas censé arriver
    if coups == []:
        coups = [(randint(0,n_coups-1), 0)]
    # si les coups ont tous un score de 0
    coups = sorted(coups, key=lambda coup: coup[1], reverse=True)
    if coups[-1][1] == 0 and coups[0][1] == 0:
        coups = [(randint(0,n_coups-1), 0)]
    return coups[0][0] , coups[0][1] , Somme(coups)

def Somme(L):
    """renvoie la somme des scores des coups de L"""
    r = 0
    for i in L:
        r+=i[1]
    return r

def Evaluation(jeu, x, y) -> int:
    """Fonction qui retourne un score pour un coup"""
    pass
    # score pour nombre pions alignés
    # score pour pions suivis
    # score pour empecher un coup0