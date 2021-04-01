import combinatoire as comb
from collections import Counter



class Bataille:
	"""Construit la grille principale du jeu et place la liste des bateaux donnée,
	gère l'interaction de la classe joueur avec la grille de jeu."""

	def __init__(self, liste_bateaux):
		self.liste_bateaux = liste_bateaux
		self.nb_bateaux = len(liste_bateaux)
		self.grille, self.bateaux_places = comb.genere_grille_bateaux(liste_bateaux)
		self.bateaux_touchees = []
		self.bateaux_coulees = []

	def get(self, position):
		x, y = position
		return int(self.grille[x,y])

	def joue(self,position):
		"""Si il n'y a aucun bateau sur la case, renvoie "vide",
		si la case est occupée par une partie d'un bateau, renvoie "touche"
		si c'est la dernière case touchée d'un bateau, renvoie "coule", le bateau, sa position et sa direction"""
		i=0
		valeur_case = self.get(position)
		if valeur_case==0:
			return "vide"
		else:
			(self.bateaux_touchees).append(valeur_case)							# Ajoute le bateau dans la liste des bateaux touchés
			bateau=[valeur_case for i in range(0,valeur_case%10)]				# La liste des cases d'un bateau
			if (list((Counter(bateau) & Counter(self.bateaux_touchees)).elements()) == bateau) and not(bateau==[]):
				"""Intersection de (la liste des cases d'un bateau) et de (la liste des cases des bateaux touchés) == liste des cases d'un bateau"""
				(self.bateaux_coulees).append(valeur_case)						# Ajoute le bateau dans la liste des bateaux coulés
				while self.bateaux_places[i][0] != valeur_case:					# Trouve l'index du bateau dans la liste des bateaux placés
					i+=1
				direction = self.bateaux_places[i][2]
				position_bateau = self.bateaux_places[i][1]
				return "coule", valeur_case, position_bateau, direction
			else:
				return "touche"

	def victoire(self):
		return len(self.bateaux_coulees) == len(self.liste_bateaux)
