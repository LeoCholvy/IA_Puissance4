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
                break
            if self.grille[ligne+1][entree] != 0:
                self.grille[ligne][entree] = sy
                break
        victoire = self.Verif()
        self.n_tours += 1
        self.Changement_joueur()

        return victoire #indique si le joueur qui vient de joué a gagné
    def Changement_joueur(self):
        """+1 a current"""
        n_joueurs = len(self.joueurs)
        self.current += 1
        if self.current >= n_joueurs:
            self.current = 0
    def Verif(self):
        """Fonction qui vérifie si le joueurs de current a gagné"""
        #TODO: verif victoire
        return False
    def Affiche(self):
        for i in self.grille[0:-1]:
            for j in i:
                print(j, end="")
            print()
        for j in self.grille[-1]:
            print(j, end="")


if __name__ == "__main__":
    jeu = Puissance4()
    jeu.Start(j=0)
    jeu.Play(1)
    jeu.Play(2)
    jeu.Play(1)
    jeu.Play(2)
    jeu.Play(1)
    jeu.Play(2)
    jeu.Play(1)
    jeu.Affiche()