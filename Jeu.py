from copy import copy
from random import randint
from colorama import Fore
from colorama import Style


class Puissance4:
    """Cette classe ne comprend pas d'interface
    start:
        initialise une nouvelle partie (il faut le faire pour la 1ere aussi)
    """
    def __init__(self, console=True, p=4, H=6, L=7, j=None) -> None:
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
        self.hauteur_max = self.H-1
        if j != None:
            self.current = j
        else:
            self.current = randint(0, len(self.joueurs)-1)
            if self.console: 
                nom = self.joueurs[self.current]["nom"]
                print(f"Le joueur qui commence est {nom} !")
                return {"index": self.current, "nom": nom}
    def Play(self,entree: int,j=None):
        """entre: collone où joue le joueur
           j: l'indice du joueurs qui joue dans la liste de joueurs
        ATTENTION: La méthode ne prend pas en charge le changement de joueur qui doit jouer a chaque tour
        si on précise le jour à un certain tour
        Si l'entree n'est pas valide, il ne se passe rien, la fonction revoie -1
        elle retourne 0 si si la partie peut continuer
                      1 si il y a match nul
                      2 si il y a victoire"""
        if not (isinstance(entree, int) and entree >= 0 and entree < self.L):
            return -1 #l'entree n'est pas valide
        if self.grille[0][entree] != 0:
            return -1
        #TODO: opti indique la hauteur max jouée (ne pas verifier si la ligne n'as pas de )
        sy = self.joueurs[self.current]["symbole"]
        for ligne in range(self.hauteur_max ,self.H):
            if ligne+1 >= self.H:
                self.grille[ligne][entree] = sy
                lig = ligne
                break
            if self.grille[ligne+1][entree] != 0:
                self.grille[ligne][entree] = sy
                lig = ligne
                break
        if self.hauteur_max >= lig:
            self.hauteur_max = ligne-1
        # verif match nul
        if self.Match_nul():
            if self.console:
                nom = self.joueurs[self.current]["nom"]
                print("Egalité ! bandes de ng")
            return 1 # match nul
        #verif victoire
        victoire = self.Verif(lig,entree)
        if victoire:
            if self.console:
                nom = self.joueurs[self.current]["nom"]
                print(f"{nom} a gagné !")
            return 2
        self.n_tours += 1
        self.Changement_joueur()
        return 0 #la partie peut continuer
    def Changement_joueur(self):
        """+1 a current"""
        n_joueurs = len(self.joueurs)
        self.current += 1
        if self.current >= n_joueurs:
            self.current = 0
    def Match_nul(self) -> bool:
        for x in self.grille:
            for y in x:
                if y == 0:
                    return False
        return True
    def Verif(self,x,y):
        pow = self.pow
        sy = self.joueurs[self.current]["symbole"]
        
        self.a=[]
        colonne = self.Aligne([(i,y) for i in range(x-pow-1, x+pow)],sy,pow)
        ligne = self.Aligne([(x,i) for i in range(y-pow-1, y+pow)],sy,pow)
        lx = [i for i in range(x-pow+1, x+pow)]
        diag1 = self.Aligne(self.Coord_Fusion(lx,[i for i in range(y-pow+1, y+pow)]),sy,pow)
        diag2 = self.Aligne(self.Coord_Fusion(lx,[i for i in range(y+pow-1, y-pow,-1)]),sy,pow)

        return colonne or ligne or diag1 or diag2
    def Coord_Fusion(self,l1,l2):
        L = []
        for i in range(len(l1)):
            L.append((l1[i],l2[i]))
        return L
    def Aligne(self,coord,sy,pow):
        """Fonction qui prend en argument une liste de coordonnés
        Elle indique si assez de "pions" se suivent"""
        p=0
        a=0
        vic=False
        for i,j in coord:
            if not(0 <= i and i < self.H and 0 <= j and j < self.L):
                i+=1
                j+=1
                continue
            if self.grille[i][j] == sy:
                p+=1
                a+=1
            else:
                p=0
            if p == pow:
                vic = True
        self.a.append(a)
        return vic
    def Affiche(self):
        joueurs = [x["symbole"] for x in self.joueurs]
        for i in self.grille:
            for j in i:
                if j == joueurs[0]:
                    print(f"{Fore.BLUE}{j}{Style.RESET_ALL}",end=" ")
                elif j == joueurs[1]:
                    print(f"{Fore.RED}{j}{Style.RESET_ALL}",end=" ")
                else:
                    print(f"{j} ", end="")
            print()
    def Get_grille(self):
        return self.grille
    def Get_position(self, entree, grille = None):
        if grille == None:
            grille = self.grille
        if not (isinstance(entree, int) and entree >= 0 and entree < self.L):
            return -1 #l'entree n'est pas valide
        if grille[0][entree] != 0:
            return -1

        sy = self.joueurs[self.current]["symbole"]
        for ligne in range(self.H):
            if ligne+1 >= self.H:
                return ligne, entree
            if self.grille[ligne+1][entree] != 0:
                return ligne, entree
    def Get_name_current_player(self) -> str:
        return self.joueurs[self.current]["nom"]





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
    # jeu.grille = [
    #     [0,0,0,0,0,0,0],
    #     [0,"x",0,0,0,0,0],
    #     [0,0,"x",0,0,0,0],
    #     [0,0,0,"x",0,0,0],
    #     [0,0,0,0,0,0,0]
    # ]
    # jeu.grille = [
    #     ["x",0,"x","x","x","x","x"],
    #     ["x","x","x","x","x","x","x"],
    #     ["x","x","x","x","x","x","x"],
    #     ["x","x","x","x","x","x","x"],
    #     ["x","x","x","x","x","x","x"]
    # ]
    # jeu.hauteur_max=0
    # jeu.Play(1)
    jeu.Affiche()
    # jeu.Play(2)