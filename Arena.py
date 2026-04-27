from Jeu import Puissance4
from MinMax import Meilleur_coup as Heuristique_AI
from MinMaxNN import Meilleur_coup_NN as Neural_AI

def arena(parties=10, depth_old=3, depth_nn=3):
    print(f"--- DÉBUT DE L'ARÈNE ---")
    print(f"IA Heuristique (Profondeur: {depth_old}) VS IA Réseau de Neurones (Profondeur: {depth_nn})")

    victoires_old = 0
    victoires_nn = 0
    nuls = 0

    for i in range(parties):
        jeu = Puissance4(console=False, j=[
            {"nom": "AncienneIA", "symbole": "x"},
            {"nom": "ReseauIA", "symbole": "+"}
        ])

        # Alterne qui commence
        jeu.Start(j=i%2)
        victoire = 0

        while victoire not in [1, 2]:
            nom_actuel = jeu.Get_name_current_player()

            if nom_actuel == "AncienneIA":
                entree, _ = Heuristique_AI(jeu, depth_old)
            else:
                entree, _ = Neural_AI(jeu, depth_nn)

            victoire = jeu.Play(entree)

        if victoire == 1:
            nuls += 1
        elif victoire == 2:
            vainqueur = jeu.joueurs[jeu.current]["nom"]
            if vainqueur == "AncienneIA":
                victoires_old += 1
            else:
                victoires_nn += 1

        print(f"Partie {i+1}/{parties} terminée. (Score actuel : Old {victoires_old} - {victoires_nn} NN)")

    print("\n=== RÉSULTATS FINAUX ===")
    print(f"Victoires Ancienne IA : {victoires_old}")
    print(f"Victoires Nouveau NN : {victoires_nn}")
    print(f"Matchs Nuls : {nuls}")

    win_rate_nn = (victoires_nn / parties) * 100
    print(f"Précision (Win Rate) du Réseau de Neurones : {win_rate_nn}%")

if __name__ == "__main__":
    # Tu peux changer les profondeurs ici pour tester l'impact
    arena(parties=10, depth_old=3, depth_nn=1)