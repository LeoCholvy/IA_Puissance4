import torch
from copy import deepcopy
import math
from random import randint
from Train_NN import Puissance4Net, grille_to_tensor

# Chargement global du modèle pour éviter de le recharger à chaque noeud
MODELE_NN = Puissance4Net()
try:
    MODELE_NN.load_state_dict(torch.load("modele_p4.pth"))
    MODELE_NN.eval() # Mode inférence
except FileNotFoundError:
    print("ATTENTION : Modèle non trouvé. Lancez Train_NN.py en premier.")

def Eval_NN(jeu, ia_sy, p_sy):
    """Nouvelle fonction d'évaluation utilisant le réseau de neurones"""
    tensor = grille_to_tensor(jeu.grille, ia_sy, p_sy)
    with torch.no_grad():
        score = MODELE_NN(tensor).item()
    return score

def Meilleur_coup_NN(jeu:object, n:int, ia=True, issue=3):
    ia_sy, p_sy = "+", "x"
    n_coups = jeu.L

    if n == 0 or issue in [1,2]:
        if issue == 2:
            if not ia: return (None, Eval_NN(jeu, ia_sy, p_sy) + n * 10000000000)
            else: return (None, Eval_NN(jeu, ia_sy, p_sy) - n * 10000000000)
        if issue == 1:
            return (None, 0)
        else:
            return (None, Eval_NN(jeu, ia_sy, p_sy))

    # Algorithme MinMax identique, mais appelle Meilleur_coup_NN récursivement
    if ia:
        value = -math.inf
        coups_possibles = []
        coup = []
        for entree in range(n_coups):
            jeu_virtuel = deepcopy(jeu)
            jeu_virtuel.console = False
            new_issue = jeu_virtuel.Play(entree)
            if new_issue == -1: continue
            coups_possibles.append(entree)
            new_score = Meilleur_coup_NN(jeu_virtuel, n-1, not ia, new_issue)[1]
            if new_score > value:
                value = new_score
                coup = [entree]
            elif new_score == value:
                coup.append(entree)
        if not coup: coup = [coups_possibles[randint(0, len(coups_possibles)-1)]]
        return coup[randint(0,len(coup)-1)], value
    else:
        value = math.inf
        coups_possibles = []
        coup = []
        for entree in range(n_coups):
            jeu_virtuel = deepcopy(jeu)
            jeu_virtuel.console = False
            new_issue = jeu_virtuel.Play(entree)
            if new_issue == -1: continue
            coups_possibles.append(entree)
            new_score = Meilleur_coup_NN(jeu_virtuel, n-1, not ia, new_issue)[1]
            if new_score < value:
                value = new_score
                coup = [entree]
            if new_score == value:
                coup.append(entree)
        if not coup: coup = [coups_possibles[randint(0, len(coups_possibles)-1)]]
        return coup[randint(0,len(coup)-1)], value