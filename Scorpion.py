import random
import numpy as np



class Recherche:
    """Le bateau Scorpion est posé aléatoirement dans une grille,
    le bateau est trouvé si la fonction trouve(self, position) renvoie -->True."""

    def __init__(self, n):
        self.grille = np.zeros((n,n))
        self.grille[random.randint(0,n-1), random.randint(0,n-1)] = 1

    def trouve(self, position):
        return self.grille[position]==1



class Scorpion() :
    """Une matrice des probabilités indique la probabilité de trouver le bateau dans chaque case,
     on vérifie la case k et si il n’y a pas eu de détection dans k, on augmente la probabilité des autres cases."""

    def __init__(self, matrice, n, p_s) :
        self.r = Recherche(n)
        self.matrice = matrice                          # matrice - la matrice de probabilités initiales
        self.p_s = p_s                                  # p_s - la probabilité que le senseur détecte l’objet s'il se trouve dans la case
        self.n = n                                      # n - taille de la matrice

    def cherche_Scorpion(self):
        i=1
        position = self.trouve_max()                    # Trouve la case avec la plus grande probabilité de contenir le bateau dans la matrice donnée
        while not(self.r.trouve(position)):             # Tant que le bateau n'est pas trouvé
            pi_i = self.matrice[position]
            pi_k = self.calcule_pi_k(pi_i)              # Calcule la nouvelle probabilité de la case actuelle sachant que le senseur a detecté une case vide
            self.transformer_matrice(pi_i, pi_k)        # Augmente la probabilité des autres cases
            self.matrice[position] = pi_k               # Mise à jour de la probabilité de la case actuelle
            position = self.trouve_max()                # Trouve la case avec la plus grande probabilité de contenir le bateau
            i+=1
        return i

    def calcule_pi_k(self, pi_i):
        """Calcule pi_k."""
        return (pi_i-pi_i*self.p_s)/(1-pi_i*self.p_s)

    def transformer_matrice(self, pi_i, pi_k):
        """Mets à jour la matrice."""
        augmente = (pi_i-pi_k)/(self.n*self.n-1)
        self.matrice += augmente

    def trouve_max(self) :
        """Renvoie l'index de la première occurence de la valeur max
        de la grille transformée en tableau à 1 dimension."""
        maxindex = self.matrice.argmax()
        return (maxindex//self.n, maxindex%self.n)
