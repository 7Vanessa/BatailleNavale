import random
import numpy as np
import combinatoire as comb
from Bataille import *



class Joueur :

	def __init__(self, liste_bateaux) :
		self.b = Bataille(liste_bateaux)
		self.deja_jouee = []



class Aleatoire(Joueur) :
	"""Une grille aléatoire est tirée, chaque coup du jeu est ensuite tiré aléatoirement
	(éliminant les positions déjà jouées) jusqu’à ce que tous les bateaux soient touchés.
	La fonction devra renvoyer le nombre de coups joués."""

	def __init__(self, liste_bateaux) :
		super().__init__(liste_bateaux)

	def partie(self) :
		i=0
		position = (random.randint(0,9), random.randint(0,9))
		while not(self.b.victoire()):
			while position in self.deja_jouee:
				position = (random.randint(0,9), random.randint(0,9))
			self.b.joue(position)
			self.deja_jouee.append(position)
			i+=1
		return i



class Naive(Joueur) :
	"""Une version naive qui explore les cases ligne par ligne."""

	def __init__(self, liste_bateaux) :
		super().__init__(liste_bateaux)

	def partie(self) :
		i=0
		for l in range(0, 10):
				for c in range(0,10):
					if self.b.victoire():
						return i
					self.b.joue((l,c))
					i+=1
		return i



class Heuristique(Joueur) :
	"""Une version heuristique composée de deux comportements : un comportement aléatoire, c'est à dire que
	tant que rien n’est touché et un comportement qui va explorer les cases connexes
	lorsqu’un coup touche un bateau."""

	def __init__(self, liste_bateaux) :
		super().__init__(liste_bateaux)

	def partie(self) :
		i=0
		position = (random.randint(0,9), random.randint(0,9))
		while not(self.b.victoire()):
			while position in self.deja_jouee:
				position = (random.randint(0,9), random.randint(0,9))   # On choisit aléatoirement une position
			etat_case = self.b.joue(position)
			self.deja_jouee.append(position)
			i+=1
			if etat_case == "touche":                                   # Si un bateau a été touché
				for l in range(10-position[0], position[0]):            # On joue sur les cases de même ligne
					if etat_case[0] == "coule": break
					for c in range(position[1], 10-position[1]):        # On joue sur les cases de même colone
						if not(position in self.deja_jouee):
							etat_case = self.b.joue((l,c))
							self.deja_jouee.append(position)
							i+=1
		return i



class Probabiliste(Joueur) :
	"""À chaque tour, pour chaque bateau restant, on calcule la probabilité pour
	chaque case de contenir ce bateau sans tenir compte de la position des autres bateaux.
	Pour cela, en examinant toutes les positions possibles du bateau sur la grille, on obtient
	pour chaque case le nombre de fois où le bateau apparaît potentiellement. On dérive ainsi
	la probabilité jointe de la présence d’un bateau sur une case (en considérant que
	la position des bateaux est indépendante)."""

	def __init__(self, liste_bateaux) :
		super().__init__(liste_bateaux)
		self.bateaux_restantes = liste_bateaux.copy()
		self.grille_visible = np.zeros((10,10))
		self.grille_probabilite = np.zeros((10,10))

	def partie(self) :
		i=0
		etat_case = "vide"
		self.construit_grille_probabilite()								# Construit la "grille de probabilite" initiale
		while not(self.b.victoire()):
			position = self.trouve_max()								# Trouve la case contenant la plus grande valeur (la probabilité la plus élévée)
			etat_case = self.b.joue(position)							# Etats possibles: "vide","touche","coule"
			if etat_case == "vide":										# Si la case est vide
				self.grille_visible[position] = 1						# On place 1 dans la grille_visible (1 == la case ne peut pas contenir un bateau)
				self.construit_grille_probabilite()						# Re-calcule la "grille de probabilite"
			elif etat_case[0] == "coule":								# Si un bateau a été coulé
				bateau = etat_case[1]									# self.b.joue(position) renvoie ("coule", bateau, position, direction)
				position_bateau = etat_case[2]
				direction = etat_case[3]
				comb.place(self.grille_visible, bateau, position_bateau, direction)		# Place le bateau dans la grille_visible
				self.bateaux_restantes.remove(bateau)
				self.construit_grille_probabilite()						# Re-calcule la "grille de probabilite"
			i+=1
		return i

	def trouve_max(self) :
		"""Renvoie l'index de la première occurence de la valeur max
		de la grille transformée en tableau à 1 dimension."""
		maxindex = self.grille_probabilite.argmax()
		return (maxindex//10, maxindex%10)

	def construit_grille_probabilite(self) :
		"""En examinant toutes les positions possibles du bateau sur la grille,
		on obtient pour chaque case le nombre de fois où le bateau apparaît potentiellement."""
		self.grille_probabilite = np.ones((10,10))
		for bateau in self.bateaux_restantes:
			grille_probabilite = np.zeros((10,10))
			for i in range(0, 10):
				for j in range(0,10):
					if comb.peut_placer(self.grille_visible, bateau, (i,j), 1):  # Direction=1
						grille_probabilite[i,j:j+bateau%10]+=1
					if comb.peut_placer(self.grille_visible, bateau, (i,j), 2):  # Direction=2
						grille_probabilite[i:i+bateau%10,j]+=1
			self.grille_probabilite = np.multiply(self.grille_probabilite,(np.ones((10,10)) - (grille_probabilite/100)))	# P(case est vide) = P(le bateau 1 ne l'occupe pas) * P(le bateau 2 ne l'occupe pas) * ...
		self.grille_probabilite = np.ones((10,10))-self.grille_probabilite													# P(case contient un bateau) = 1 - P(case est vide)



class MonteCarlo(Probabiliste) :
	""" Prend la grille courante en entrée.
		Crée une copie de la grille.
		Simule un nombre spécifique d'échantillons (donné par <iterations>), dont chacun est une grille aléatoire avec les bateaux restantes.
		Regroupe toutes les simulations et somme le total de bateaux dans chaque case ( en faisant attention aux bateaux qui chevauchent les coups existants).
		Fait la moyenne de chaque case, nous donnant une matrice de fréquences ou bien une carte thermique.
		Prend la plus grande valeur correspondant à un mouvement dans la matrice.
		Répète jusqu'à la victoire."""

	def __init__(self, liste_bateaux, iterations) :
		super().__init__(liste_bateaux)
		self.iterations = iterations
		self.augmenter = False

	def partie(self) :
		"""Il s’agit de tirer aléatoirement et uniformément des grilles correspondant aux contraintes connues
		(les positions déjà touchées, les bateaux déjà coulés) et d’en moyenner les résultats."""
		i=0
		etat_case = None
		while not(self.b.victoire()):
			self.grille_probabilite = np.zeros((10,10))
			for j in range(0,self.iterations):
				bateaux = self.bateaux_restantes.copy()
				grille = self.grille_visible.copy()
				self.construit_grille_strategie(bateaux, grille)		# Construit la "grille de stratégie" basée sur la grille visible
			self.grille_probabilite/=self.iterations
			position = self.trouve_max()								# Trouve la position où la probabilité de trouver le bateau est la plus élevée
			etat_case = self.b.joue(position)							# Joue la position, états des cases possibles: "vide","touche","coule"

			#update visible grid
			if etat_case == "vide":										# Si la case est vide
				self.grille_visible[position] = 1						# Place 1 dans la grille_visible (1 == la case ne peut pas contenir de bateau)
			elif etat_case == "touche":									# Si la case est touchée
				self.grille_visible[position] = -1						# Place -1 dans la grille_visible (-1 == la case est touchée)
			elif etat_case[0] == "coule":								# Si un bateau a été coulé
				bateau = etat_case[1]									# etat_case = ("coule", bateau, position, direction)
				position_bateau = etat_case[2]
				direction = etat_case[3]
				self.place_si_coule(bateau, position_bateau, direction)	# Place le bateau coulé dans la grille_visible
				self.bateaux_restantes.remove(bateau)

			i+=1

		return i

	def construit_grille_strategie(self, bateaux, grille):
		"""Il s’agit de tirer aléatoirement et uniformément des grilles correspondant aux contraintes connues
		(les positions déjà touchées, les bateaux déjà coulés) et d’en moyenner les résultats."""
		while bateaux != []:
			bateau = random.choice(bateaux)								# On choisit aléatoirement un bateau dans la liste des bateaux non encore coulés
			self.place_alea(grille, bateau)								# On choisit aléatoirement une position d'un bateau dans la grille visible
			bateaux.remove(bateau)

	def place_alea(self, grille, bateau):
		"""Place aleatoirement le bateau dans la grille
		en tirant uniformement une position et une direction aléatoires
		jusqu'à ce que le positionnement choisit soit admissible et effectué."""
		position = (random.randint(0,9), random.randint(0,9))
		direction = random.randint(1,2)
		c=0
		while c < 500:
			if self.peut_placer(grille, bateau, position, direction)==True:
				self.place(grille, bateau, position, direction)
				return
			else:
				position = (random.randint(0,9), random.randint(0,9))
				direction = random.randint(1,2)
				c+=1

	def place(self, grille, bateau, position, direction):
		"""Si l'operation est possible, rend la grille modifiee
		ou le bateau a ete place comme indique."""
		taille_bateau = bateau%10
		if direction==1:
			for i in range(position[1],position[1]+taille_bateau):
				if self.grille_visible[position[0],i]==0:
					self.grille_probabilite[position[0],i] += 1
					if self.augmenter:									# Attention aux bateaux qui chevauchent les coups existants
						self.grille_probabilite[position[0],i] += 1
			if self.augmenter:
				self.augmenter = False
		else:
			for i in range(position[0],position[0]+taille_bateau):
				if self.grille_visible[i,position[1]]==0:
					self.grille_probabilite[i,position[1]] += 1
					if self.augmenter:									# Attention aux bateaux qui chevauchent les coups existants
						self.grille_probabilite[i,position[1]] += 1
			if self.augmenter:
				self.augmenter = False

	def peut_placer(self, grille, bateau, position, direction):
		"""Retourne vrai si il est possible de placer le bateau sur la grille
		à la position et dans la direction donnée (1-horizontale, 2-verticale)."""
		taille_bateau = bateau%10
		if direction==1:												# Direction horizontale
			if position[1]+taille_bateau<=10:
				for i in range(position[1],position[1]+taille_bateau):
					if grille[position[0],i]==-1:
						self.augmenter = True							# Va servir a souligner les bateaux qui chevauchent les coups existants
					elif grille[position[0],i]!=0:
						return False
			else: return False
		else:															# Direction verticale
			if position[0]+taille_bateau<=10:
				for i in range(position[0],position[0]+taille_bateau):
					if grille[i,position[1]]==-1:
						self.augmenter = True							# Va servir a souligner les bateaux qui chevauchent les coups existants
					elif grille[i,position[1]]!=0:
						return False
			else: return False
		return True

	def place_si_coule(self, bateau, position, direction):
		"""Si l'opération est possible, rend la grille modifiée
		où le bateau a été placé comme indiqué."""
		taille_bateau = bateau%10
		if direction==1:
			self.grille_visible[position[0],(position[1]):(position[1]+taille_bateau)] = bateau
		else:
			self.grille_visible[(position[0]):(position[0]+taille_bateau),position[1]] = bateau
