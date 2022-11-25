from copy import deepcopy

# coef: -1 si c'est le coup de l'adversaire
#        1 si c'est le coup de l'IA
def Meilleur_coup(jeu:object,n:int,coef:int):
    # pour chaque colonne
    max = (None, 0)
    # (entree, score)
    for entree in range (pow):
        pow=jeu.pow
        pos = jeu.Get_position(entree)
        if pos == -1:
            continue


        # # verif si le coup est possible
        # pow = jeu.Get_position(entree)
        # if pow == -1:
        #     # le coup n'est pas valide
        #     continue
        # # fin réccursif
        # if n == 0:
        #     score = Evaluation(jeu, entree)
        # # score du coup
        # else:
        #     jeu_virtuel = deepcopy(jeu)
        #     jeu_virtuel.Play(entree)
        #     # prendre en charge les fin de partie
        #     score = Meilleur_coup(jeu_virtuel) + Evaluation(jeu, entree)
        # if max < score:
        #     # FIXME: score avec le coef
        #     max = (entree, score)
        #     continue
    return max
    # TODO: si max = (None,x) aucun coup n'est possible, prendre en charge cette possibilité (score match nul)

def Evaluation(jeu, x, y) -> int:
    """Fonction qui retourne un score pour un coup"""
    pass
    # score pour nombre pions alignés
    # score pour pions suivis
    # score pour match nul ?
    # score pour victoire