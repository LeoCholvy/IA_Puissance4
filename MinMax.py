from copy import deepcopy
from random import randint

# coef: -1 si c'est le coup de l'adversaire
#        1 si c'est le coup de l'IA
def Meilleur_coup(jeu:object,n:int,ia=True):
    pass


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