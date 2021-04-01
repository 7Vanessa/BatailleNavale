import random
import matplotlib.pyplot as plt
import numpy as np



def peut_placer(grille, bateau, position, direction):
	"""Retourne vrai si il est possible de placer le bateau sur la grille
	à la position et à la direction données en paramètre de la fonction (1-horizontale, 2-verticale)."""
	taille_bateau = bateau%10                   								# bateau%10 car dans main.py nous utilisons cette liste de bateaux [2,3,13,4,5] or 13 représente un bateau de taille 3
	if direction==1:                            								# Si direction horizontale
		if position[1]+taille_bateau<=10: 										# Si il y a assez de place pour placer le bateau sur la ligne
			for i in range(position[1],position[1]+taille_bateau): 				# Pour les cases pouvant être occupées par le bateau courant
				if grille[position[0],i]!=0: 									# Teste si la case n'est pas déjà occupée par un autre bateau, si non retourne faux
					return False
		else: return False 														# Si il n'y a pas assez de place pour placer le bateau retourne faux
	else:                                       								# Si direction verticale
		if position[0]+taille_bateau<=10: 										# Si il y a assez de place pour placer le bateau sur la colonne
			for i in range(position[0],position[0]+taille_bateau): 				# Pour les cases pouvant être occupée par le bateau courant
				if grille[i,position[1]]!=0: 									# Teste si la case n'est pas déjà occupée par un autre bateau, si non retourne faux
					return False
		else: return False 														# Si il n'y a pas assez de place pour placer le bateau retourne faux
	return True

def place(grille, bateau, position, direction):
	"""Si l'operation est possible, rend la grille modifiée
	où le bateau a été place comme indiqué."""
	taille_bateau = bateau%10 													# bateau%10 car dans main.py nous utilisons cette liste de bateaux [2,3,13,4,5] or 13 représente un bateau de taille 3
	if not(peut_placer(grille, bateau, position, direction)): 					# Fait appel à la fonction peut_placer pour savoir si l'opération est possible
		return
	if direction==1: 															# Si la direction est horizontale
		grille[position[0],(position[1]):(position[1]+taille_bateau)] = bateau 	# On place le bateau sur les n cases consécutives correspondant à la taille du bateau à partir de la position entrée en paramètre de la fonction
	else: 																		# Si la direction est verticale
		grille[(position[0]):(position[0]+taille_bateau),position[1]] = bateau 	# On place le bateau sur les n cases consécutives correspondant à la taille du bateau à partir de la position entrée en paramètre de la fonction

def place_alea(grille, bateau):
	"""Place aleatoirement le bateau dans la grille
	en tirant uniformement une position et une direction aléatoires
	jusqu'à ce que le positionnement choisi soit admissible et effectué."""
	position = (random.randint(0,9), random.randint(0,9)) 						# On choisit une position aléatoirement
	direction = random.randint(1,2) 											# On choisit une direction aléatoirement
	if peut_placer(grille, bateau, position, direction)==True: 					# Si le bateau peut être placé à la position et à la direction choisies aléatoirement
		place(grille, bateau, position, direction) 								# Alors on place le bateau dans la grille
	else: place_alea(grille, bateau) 											# Si le bateau ne peut pas être placé, on rappelle la fonction jusqu'à ce que le bateau puisse être placé

def affiche(grille):
	"""Affichage de la grille de jeu."""
	grid = plt.imshow(grille, origin=None) 										# Grid represente l'image de la grille de jeu entrée en parametre
	grid.axes.get_xaxis().set_visible(False) 									# Désactive l’axe pour l’axe X
	grid.axes.get_yaxis().set_visible(False) 									# Désactive l’axe pour l’axe Y
	plt.show() 																	# Affiche l'image de la grille

def eq(grilleA, grilleB):
	"""Teste l'égalité entre deux grilles."""
	return np.array_equal(grilleA, grilleB) 									# Retourne vrai les 2 grilles sont identiques

def genere_grille_bateaux(bateaux):
	"""Retourne une grille aleatoire comprenant une liste donnee des bateaux et
	renvoie la liste des bateaux placés comprenant les positions et directions."""
	bateaux_places = [] 														# On initialise une liste vide qui contiendra des tuples. Chaque tuple correspondant au bateau placé dans la grille, a sa position, ainsi qu'à sa direction
	grille = np.zeros((10,10)) 													# On initialise une grille 10x10 avec 0 dans toutes ses cases
	for b in bateaux: 															# Pour tous les bateau à placer. bateaux : liste des bateaux à placer dans la grille
		position = (random.randint(0,9), random.randint(0,9)) 					# On choisit une position aléatoire
		direction = random.randint(1,2) 										# On choisit une direction aléatoire
		while peut_placer(grille, b, position, direction)==False: 				# Tant qu'il n'est pas possible de placer le bateau sur la grille
			position = (random.randint(0,9), random.randint(0,9)) 				# On choisit aléatoirement une position
			direction = random.randint(1,2) 									# On choisit aleatoirement une direction, jusqu'à ce que le bateau puisse être placé dans la grille
		place(grille, b, position, direction) 									# Ainsi quand cela est possible on place le bateau dans la grille
		bateaux_places.append((b, position, direction)) 						# Et on l'ajoute à la liste des bateaux qui on deja été placés
	return grille, bateaux_places 												# Retourne la grille ainsi que la liste des bateaux placés contenant des tuples correspondant au bateau, à sa position, ainsi qu'à sa direction dans la grille

def genere_grille():
	"""Retourne une grille aleatoire comprenant l'ensemble des bateaux."""
	grille = np.zeros((10,10)) 													# On initialise une grille 10x10 avec 0 dans toutes ses cases
	bateaux = [2, 3, 13, 4, 5]  												# Liste des bateaux à placer dans la grille
	for b in bateaux: 															# Pour chaque bateau de la liste
		place_alea(grille, b) 													# On le place aléatoirement dans la grille
	return grille 																# On retourne la grille

def facons_placer_bateau(grille, bateau):
	"""Permet de calculer le nombre de facons de placer
	un bateau entré en parametre sur une grille vide."""
	total_facons=0  															# Compteur
	for d in [1,2]: 															# Pour chaque direction
		for i in range(0, 10): 													# Pour chaque ligne
			for j in range(0,10): 												# Pour chaque colonne
				if peut_placer(grille, bateau, (i,j), d): 						# Si il est possible de placer le bateau entré en paramètre sur la grille à la position et à la direction courante
					total_facons+=1 											# On incrémente donc notre compteur
	return total_facons 														# Retourne le nombre de possibilité

def grille_tinder(grille):
	"""Prend en parametre une grille, genere des grilles aleatoirement
	jusqu'a ce que la grille generee soit egale a la grille passee
	en parametre et renvoie le nombre de grilles generees."""
	potential_matches=0 														# Compteur des grilles générées jusqu'à qu'une grille générées corresponde à la grille entrée en parametre de la fonction
	grille_match=None 															# Variable qui contiendra la grille courante
	while not(eq(grille_match,grille)): 										# On génère une nouvelle grille jusqu'à ce que la grille courante soit égale à la grille entrée en paramètre
		grille_match=genere_grille() 											# Génère une grille aléatoire
		potential_matches+=1 													# On incrémente le compteur à chaque nouvelle grille générée
	return potential_matches 													# On retourne le nombre de grilles générées

def facons_placer_bateaux_1(grille, bateaux):
	"""Permet de calculer le nombre de facons de placer une liste de bateaux
	sur une grille vide."""
	total = 0 																	# Compteur
	for b in bateaux: 															# Pour chaque bateau de la liste de bateau entrée en paramètre
		for d in [1,2]: 														# Pour chaque direction
			for i in range(0, 10): 												# Pour chaque ligne de la grille
				for j in range(0,10): 											# Pour chaque colonne de la grille
					if peut_placer(grille, b, (i,j), d): 						# On teste si le bateau peut y être placer
						total += 1 												# Si oui, on incrémente notre compteur
						bateaux1 = bateaux[1:] 									# On initialise une variable bateaux1 contenant la liste des bateaux entrée en paramètre à laquelle on retire le premier élément
						if bateaux1!=[]: 										# Si bateaux1 ne correspond pas à la liste vide
							place(grille, b, (i,j), d) 							# On place dans la grille le bateau courant à la position et à la direction courante
							total += facons_placer_bateaux_1(grille, bateaux1) 	# On incrémente la valeur du compteur avec le retour de la fonction appelé cette fois avec la liste bateaux1
							grille = np.zeros((10,10)) 							# On réinitialise la grille
	return total 																# On retourne le compteur du nombre de facons de placer une liste de bateaux

def facons_placer_bateaux_2(bateaux):           								# Pas efficace, beaucoup trop long
	"""Permet d'approximer le nombre total de grilles pour une liste de bateaux."""
	i = 0 																		# Compte le nombre de fois consécutives qu'une grille est déjà été générée
	grilles = [] 																# On initialise une liste vide qui contiendra les différentes grilles générées (elles seront uniques)
	grille=[]
	grille.append(genere_grille_bateaux(bateaux)[0].tolist()) 					# On initialise une variable qui contiendra la grille courante, une grille générée aléatoirement avec la liste de bateaux entrée en paramètre
	while i<=10: 																# Si on gérère consécutivement 10 grilles déjà présentent dans la liste alors on quitte la boucle
		if grille not in grilles : 												# Si la grille courante n'a pas encore été générée, c'est à dire qu'elle n'est pas encore présente dans la liste
			grilles.append(grille) 												# Alors on l'ajoute à la liste
			i=0 																# Et on remet le compteur à 0
		else : 																	# Si la grille a déjà été générée
			i+=1 																# Alors on incrémente le compteur
		grille = []
		grille.append(genere_grille_bateaux(bateaux)[0].tolist()) 				# Grille prend la valeur d'une nouvelle grille aléatoire
	return len(grilles) 														# On retourne la taille de la liste, c'est à dire le nombre de grilles différentes générées

def facons_placer_bateaux_3(etapes):
	"""Permet d'approximer le nombre total de grilles pour une liste de bateaux."""
	total_facons = 0 															# Compteur du nombre de total de façons de placer une liste de bateaux
	for e in range(0,etapes): 													# On répète les instructions suivantes n fois correspondant au nombre d'étapes entré en paramètre
		facons = 1 																# Initialisation du compteur du nombre de façons de placer liste de bateaux sur une grille
		bateaux = [2, 3, 13, 4, 5] 												# Liste des bateaux à placer dans la grille
		grille = np.zeros((10,10)) 												# On initialise une grille 10x10 avec 0 dans toutes les cases
		for b in bateaux: 														# Pour chaque bateau de la liste
			facons *= facons_placer_bateau(grille, b) 							# On multiplie le compteur par le nombre de façons de placer le bateau courant sur la grille
			place_alea(grille, b) 												# On place aléatoirement le bateau courant sur la grille
		total_facons += facons 													# On ajoute au compteur total le nombre de façons de placer une liste de bateaux durant une étape
	return total_facons//etapes 												# On retourne le nombre de façons totales trouvées divisé par le nombre d'étapes réalisées
