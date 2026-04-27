import torch
import torch.nn as nn
import torch.optim as optim
from random import choice
from copy import deepcopy
from Jeu import Puissance4
from MinMax import Eval
import numpy as np

# --- ARCHITECTURE DU RÉSEAU DE NEURONES ---
class Puissance4Net(nn.Module):
    def __init__(self):
        super(Puissance4Net, self).__init__()
        # Le plateau fait 6x7. On utilise des convolutions pour repérer les alignements.
        self.conv1 = nn.Conv2d(1, 16, kernel_size=4, padding=2)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.flatten = nn.Flatten()
        # Entrée dense : 32 canaux * 7 * 8 (à cause du padding) -> 1792
        self.fc1 = nn.Linear(1792, 128)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, 1) # Sortie : 1 seul score (float)

    def forward(self, x):
        x = self.relu1(self.conv1(x))
        x = self.relu2(self.conv2(x))
        x = self.flatten(x)
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return x

# --- UTILITAIRES DE CONVERSION ---
def grille_to_tensor(grille, ia_sy, p_sy):
    """Convertit la grille 2D de strings en Tensor PyTorch"""
    mat = np.zeros((6, 7), dtype=np.float32)
    for i in range(6):
        for j in range(7):
            if grille[i][j] == ia_sy:
                mat[i][j] = 1.0
            elif grille[i][j] == p_sy:
                mat[i][j] = -1.0
    # Reshape pour PyTorch: (Batch, Channels, Height, Width) -> (1, 1, 6, 7)
    return torch.tensor(mat).unsqueeze(0).unsqueeze(0)

# --- GÉNÉRATION DE DONNÉES ---
def generate_data(num_samples=5000):
    print(f"Génération de {num_samples} plateaux pour l'entraînement...")
    X, Y = [], []
    ia_sy, p_sy = "+", "x"

    for _ in range(num_samples):
        jeu = Puissance4(console=False, j=[{"nom": "Joueur", "symbole": p_sy}, {"nom": "IA", "symbole": ia_sy}])
        jeu.Start()
        # Jouer un nombre aléatoire de coups pour avoir des plateaux variés
        n_coups = np.random.randint(5, 35)
        for _ in range(n_coups):
            coups_valides = [c for c in range(jeu.L) if jeu.grille[0][c] == 0]
            if not coups_valides: break
            jeu.Play(choice(coups_valides))

        score = Eval(jeu, ia_sy, p_sy)
        X.append(grille_to_tensor(jeu.grille, ia_sy, p_sy).squeeze(0)) # Garde (1, 6, 7)
        Y.append([float(score)])

    return torch.stack(X), torch.tensor(Y, dtype=torch.float32)

if __name__ == "__main__":
    X, Y = generate_data(10000) # Tu peux augmenter ce nombre pour plus de précision

    model = Puissance4Net()
    criterion = nn.MSELoss() # Erreur Quadratique Moyenne
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # --- ENTRAÎNEMENT ---
    epochs = 50
    batch_size = 64
    print("Début de l'entraînement du réseau...")
    for epoch in range(epochs):
        permutation = torch.randperm(X.size()[0])
        epoch_loss = 0
        for i in range(0, X.size()[0], batch_size):
            indices = permutation[i:i+batch_size]
            batch_x, batch_y = X[indices], Y[indices]

            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        if (epoch+1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} - Loss (MSE) : {epoch_loss/len(X):.4f}")

    print("Entraînement terminé. Sauvegarde du modèle dans 'modele_p4.pth'")
    torch.save(model.state_dict(), "modele_p4.pth")