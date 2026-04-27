import torch
import torch.nn as nn
import torch.optim as optim
from copy import deepcopy
import random
from Jeu import Puissance4
from Train_NN import Puissance4Net, grille_to_tensor
from MinMaxNN import Meilleur_coup_NN

# --- PARAMÈTRES AMÉLIORÉS ---
GAMES_PER_ITERATION = 50   # Réduit car la génération sera beaucoup plus lente
ITERATIONS = 15             # Nombre de cycles d'entraînement
EPSILON = 0.1              # Taux d'exploration réduit (10% de hasard) pour éviter les parties absurdes
SEARCH_DEPTH = 2           # LA CLÉ : L'IA calcule 2 coups d'avance pendant l'entraînement !
RECOMPENSE_VICTOIRE = 1000.0
RECOMPENSE_DEFAITE = -1000.0
RECOMPENSE_NUL = 0.0

# --- CHARGEMENT DU MODÈLE ---
model = Puissance4Net()
try:
    # On repart de ton modèle qui a 69% de winrate (le bon !)
    model.load_state_dict(torch.load("modele_p4.pth"))
    print("Modèle initial (69% WR) chargé avec succès.")
except:
    print("Erreur: Modèle non trouvé.")
    exit()

# Learning rate très faible pour ajuster doucement les poids sans "Oubli Catastrophique"
optimizer = optim.Adam(model.parameters(), lr=0.0001)
criterion = nn.MSELoss()

def play_one_game():
    """Joue une partie de haute qualité avec l'algorithme MinMax"""
    jeu = Puissance4(console=False, j=[
        {"nom": "IA_Min", "symbole": "x"}, # Cherche à minimiser le score (joue les x)
        {"nom": "IA_Max", "symbole": "+"}  # Cherche à maximiser le score (joue les +)
    ])
    # Alterne qui commence au hasard
    jeu.Start(j=random.randint(0, 1))

    history = []
    victoire = 0

    while victoire not in [1, 2]:
        current_sy = jeu.joueurs[jeu.current]["symbole"]

        coups_valides = [c for c in range(jeu.L) if jeu.grille[0][c] == 0]

        # --- EXPLORATION vs EXPLOITATION ---
        if random.random() < EPSILON:
            # 10% du temps : Exploration (Coup aléatoire pour découvrir des variantes)
            coup = random.choice(coups_valides)
        else:
            # 90% du temps : Exploitation avec MinMax (Profondeur 2)
            # Si le joueur actuel est "+", il veut maximiser (ia=True)
            # Si le joueur actuel est "x", il veut minimiser (ia=False)
            is_maximizing = (current_sy == "+")

            coup, _ = Meilleur_coup_NN(jeu, n=SEARCH_DEPTH, ia=is_maximizing)
            if coup is None or coup not in coups_valides:
                coup = random.choice(coups_valides) # Sécurité

        # On sauvegarde l'état visuel du plateau APRÈS le coup
        jeu_virtuel = deepcopy(jeu)
        jeu_virtuel.console = False
        jeu_virtuel.Play(coup)

        # Le tenseur est toujours évalué du point de vue global (ia_sy="+", p_sy="x")
        tensor_etat = grille_to_tensor(jeu_virtuel.grille, "+", "x")
        history.append((tensor_etat, current_sy))

        # Jouer le coup pour de vrai
        victoire = jeu.Play(coup)

    # --- FIN DE PARTIE : ATTRIBUTION DES RÉCOMPENSES ---
    X, Y = [], []
    vainqueur_sy = None
    if victoire == 2:
        vainqueur_sy = jeu.joueurs[jeu.current]["symbole"]

    for tensor_etat, joueur_sy in history:
        X.append(tensor_etat.squeeze(0))
        if victoire == 1:
            Y.append([RECOMPENSE_NUL])
        elif joueur_sy == vainqueur_sy:
            Y.append([RECOMPENSE_VICTOIRE])
        else:
            Y.append([RECOMPENSE_DEFAITE])

    return X, Y

# --- BOUCLE PRINCIPALE ---
if __name__ == "__main__":
    print(f"🚀 Début du Self-Play de Qualité Maître (Profondeur = {SEARCH_DEPTH})...")
    print("Attention, cela peut prendre un certain temps.")

    for iteration in range(ITERATIONS):
        print(f"\n--- Itération {iteration+1}/{ITERATIONS} ---")
        all_X, all_Y = [], []

        for i in range(GAMES_PER_ITERATION):
            X, Y = play_one_game()
            all_X.extend(X)
            all_Y.extend(Y)
            if (i+1) % 5 == 0:
                print(f"  > {i+1}/{GAMES_PER_ITERATION} parties générées...")

        tensor_X = torch.stack(all_X)
        tensor_Y = torch.tensor(all_Y, dtype=torch.float32)

        # Entraînement sur les parties générées
        model.train()
        for _ in range(3): # 3 passes sur les données
            optimizer.zero_grad()
            outputs = model(tensor_X)
            loss = criterion(outputs, tensor_Y)
            loss.backward()
            optimizer.step()

        print(f"Loss moyenne (MSE) : {loss.item():.4f}")

    # On sauvegarde sur le même fichier SelfPlay
    torch.save(model.state_dict(), "modele_p4_selfplay.pth")
    print("\n✅ Entraînement Maître terminé ! Modèle 'modele_p4_selfplay.pth' mis à jour.")