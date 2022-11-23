from random import randint


class Puissance4:
    """Cette classe ne comprend pas d'interface
    start:
        initialise une nouvelle partie (il faut le faire pour la 1ere aussi)
    """
    def __init__(self, console=True, p=4, H=5, L=7, j=None) -> None:
        """
        console: booleen activation affichage console
        p: nombre de pions a aligné pour gagner, par défaut: 4
        H et L: respectivement la hauteur la largeur du jeu, défaut: 5 et 7
        j: liste des joueurs (sous forme de dictionnaires)
            ATTENTION: symbole ne doit pas etre 0"""
        if j == None:
            j = [
                {"nom": "Joueur1", "symbole":"x"},
                {"nom": "Joueur2", "symbole":"o"}
            ]
        self.pow = p
        self.H = H
        self.L = L
        self.joueurs = j
        self.console = console
    def Start(self, j=None):
        """j: indice du joueur qui commence dans la liste"""
        self.n_tours = 0
        self.grille = [[0 for x in range(self.L)] for i in range(self.H)]
        if j != None:
            self.current = j
        else:
            self.current = randint(0, len(self.joueurs)-1)
            if self.console: 
                nom = self.joueurs[self.current]["nom"]
                print(f"Le joueur qui commence est {nom} !")
    def Play(self,entree,j=None):
        """entre: collone où joue le joueur
           j: l'indice du joueurs qui joue dans la liste de joueurs
        ATTENTION: La méthode ne prend pas en charge le changement de joueur qui doit jouer a chaque tour
        si on précise le jour à un certain tour
        Si l'entree n'est pas valide, il ne se passe rien, la fonction revoie -1"""
        if not (isinstance(entree, int) and entree >= 0 and entree < self.L):
            return -1 #l'entree n'est pas valide
        if self.grille[0][entree] != 0:
            return -1

        sy = self.joueurs[self.current]["symbole"]
        for ligne in range(self.H):
            if ligne+1 >= self.H:
                self.grille[ligne][entree] = sy
                lig = ligne
                break
            if self.grille[ligne+1][entree] != 0:
                self.grille[ligne][entree] = sy
                lig = ligne
                break
        victoire = self.Verif(lig,entree)
        if self.console and victoire:
            nom = self.joueurs[self.current]["nom"]
            print(f"{nom} a gagné !")
        self.n_tours += 1
        self.Changement_joueur()
        return victoire #indique si le joueur qui vient de joué a gagné
    def Changement_joueur(self):
        """+1 a current"""
        n_joueurs = len(self.joueurs)
        self.current += 1
        if self.current >= n_joueurs:
            self.current = 0
    def Verif(self,x,y):
        """Fonction qui vérifie si le joueurs de current a gagné"""
        #NOTE: x:pour la hauteur et vers le bas
        #      y:pour la largeur et vers la droite
        #TODO: Optimisation de la fonction et simplification
        pow = self.pow
        sy = self.joueurs[self.current]["symbole"]
        # colonne
        p=0
        for i in range(x-pow-1, x+pow):
            if not(0 <= i and i < self.H):
                continue
            if self.grille[i][y] == sy:
                p+=1
            else:
                p=0
            if p == 4:
                return True
        # ligne
        p=0
        for i in range(y-pow-1, y+pow):
            if not(0 <= i and i < self.L):
                continue
            if self.grille[x][i] == sy:
                p+=1
            else:
                p=0
            if p == 4:
                return True
        # diagonale NE-SO
        i, xf = x-pow+1, x+pow
        j, yf = y-pow+1, y+pow
        while i != xf and j != yf:
            if not(0 <= i and i < self.H):
                i+=1
                j+=1
                continue
            if not(0 <= j and j < self.L):
                i+=1
                j+=1
                continue
            if self.grille[i][j] == sy:
                p+=1
            else:
                p=0
            if p == 4:
                return True
        # diagonale NO-SE
        i, xf = x-pow+1, x+pow
        j, yf = y+pow-1, y-pow
        while i != xf and j != yf:
            if not(0 <= i and i < self.H):
                i+=1
                j+=1
                continue
            if not(0 <= j and j < self.L):
                i+=1
                j+=1
                continue
            if self.grille[i][j] == sy:
                p+=1
            else:
                p=0
            if p == 4:
                return True
            print(self.grille[i][j], i,j)
            i+=1
            j-=1

        return False
    def Affiche(self):
        for i in self.grille[0:-1]:
            for j in i:
                print(j, end="")
            print()
        for j in self.grille[-1]:
            print(j, end="")
        print()


if __name__ == "__main__":
    jeu = Puissance4()
    jeu.Start(j=0)
    # jeu.Play(1)
    # jeu.Play(1)
    # jeu.Play(2)
    # jeu.Play(1)
    # jeu.Play(3)
    # jeu.Play(1)
    # jeu.Play(4)
    # jeu.Play(1)
    # jeu.grille = [
    #     [0,0,0,0,0,0,"x"],
    #     [0,0,0,0,0,"x",0],
    #     [0,0,0,0,"x",0,0],
    #     [0,0,0,"x",0,0,0],
    #     [0,0,0,0,0,0,0]
    # ]
    jeu.grille = [
        [0,0,0,0,0,0,0],
        [0,"x",0,0,0,0,0],
        [0,0,"x",0,0,0,0],
        [0,0,0,"x",0,0,0],
        [0,0,0,0,0,0,0]
    ]
    jeu.Affiche()
    jeu.Play(4)