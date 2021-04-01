
# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import scipy as spicy;			# for curve fitting

from Joueur import *
from Scorpion import *
from combinatoire import *



if __name__ == "__main__":

################# PARTIE 3 #################

	a=Aleatoire([2, 3, 13, 4, 5])
	print("Aleatoire : ", a.partie())

	n=Naive([2, 3, 13, 4, 5])
	print("Naive : ", n.partie())

	h=Heuristique([2, 3, 13, 4, 5])
	print("Heuristique : ", h.partie())

	p=Probabiliste([2, 3, 13, 4, 5])
	print("Probabiliste : ", p.partie())

	m=MonteCarlo([2, 3, 13, 4, 5], 10)
	print("MonteCarlo : ", m.partie())

################# PARTIE 4 #################

	matrice = np.array([[0.005,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005],
						[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.015,0.015,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.015,0.015,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
						[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
						[0.005,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005]])

	s=Scorpion(matrice, 10, 0.80)
	print("Scorpion : ", s.cherche_Scorpion())

################# PARTIE 2 #################

#   grille = genere_grille()
#   grille2 = genere_grille()

#   print(eq(grille1,grille1))
#   affiche(grille)

#   grille = np.zeros((10,10))
#   print(facons_placer_bateau(grille, 5))				# question 2.2
#   print(facons_placer_bateaux_1(grille, [2,3,13]))	# question 2.3
#   print(grille_tinder(grille))						# question 2.4
#   print(facons_placer_bateaux_2([2,3]))				# question 2.5

#	print(facons_placer_bateaux_3(1000))				# question 2.6





#############################################################
#															#
#			PLOTS, PLOTS AND MORE PLOTS						#
#															#
#############################################################	

# Plots for the Monte Carlo approach to approximate the possible number of grids (facons_placer_bateaux_3())

	#data = np.loadtxt('facons_placer_bateaux_3.txt')

	#x = data[:, 0]

	# for the log-lin plot
	#y1 = data[:, 1]
	#y2 = data[:, 2]
	#y3 = data[:, 3]
	#y4 = data[:, 4]
	#y5 = data[:, 5]

	# for the error plot
	#y1 =  data[:, 1]
	#y1=np.abs(y1-30095060976)
	#y2 = data[:, 2]
	#y2=np.abs(y2-30095060976)
	#y3 = data[:, 3]
	#y3=np.abs(y3-30095060976)
	#y4 = data[:, 4]
	#y4=np.abs(y4-30095060976)
	#y5 = data[:, 5]
	#y5=np.abs(y5-30095060976)
	
	#x_data = np.tile(x,5)
	#y_data = np.concatenate([y1,y2,y3,y4,y5])

	#plt.scatter(x, y1, s=24, c=22*['#a09cb0'], marker = 's')
	#plt.scatter(x, y2, s=24, c=22*['#987d7c'], marker = 'o')
	#plt.scatter(x, y4, s=24, c=22*['#a3b9c9'], marker = 'D')
	#plt.scatter(x, y5, s=24, c=22*['#abdae1'], marker = '+')
	#plt.scatter(x, y3, s=24, c=22*['#776d5a'], marker = '.')

	#plt.xscale('log')
	#plt.yscale('log') 																# for the error plot
	#plt.ylabel('nombre de grilles de bataille navale possibles', fontsize=12)		# for the lin-log grid plot
	#plt.ylabel('distance de l\'asymptote', fontsize=12)							# for the error plot
	#plt.xlabel('grilles de bataille navale générées', fontsize=12)
	#plt.gca().legend(('expérience 1','expérience 2', 'expérience 3', 'expérience 4', 'expérience 5'))

	# curve fitting for the error plot
	#def test_func(x, a, b):
	#	return a * np.power(x,b)

	#params, params_covariance = opt.curve_fit(test_func, x_data, y_data, p0=[2, 2])
	#print(params)
	#plt.plot(x_data, test_func(x_data, params[0], params[1]), '#d9d7c3')
	
	#print(np.std(y_data, axis=None, dtype=None, out=None, ddof=0))		#332567.9170416992
	#plt.show()

# Plots for different players

	#matrice = np.array([[0.005,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005],
	#					[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.015,0.015,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.015,0.015,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
	#					[0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01],
	#					[0.005,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.005]])

	#x = np.arange(1,1001)

	# for player performance plot
	#y1 = [(Aleatoire([2, 3, 13, 4, 5]).partie()) for i in range(1,100001)]
	#y1 = np.array(y1)
	#y2 = [(Naive([2, 3, 13, 4, 5]).partie()) for i in range(1,100001)]
	#y2 = np.array(y2)
	#y3 = [(Heuristique([2, 3, 13, 4, 5]).partie()) for i in range(1,100001)]
	#y3 = np.array(y3)
	#y4 = [(Probabiliste([2, 3, 13, 4, 5]).partie()) for i in range(1,100001)]
	#y4 = np.array(y4)
	#y5 = [(MonteCarlo([2, 3, 13, 4, 5], 1000).partie()) for i in range(1,1001)]
	#y5 = np.array(y5)
	#y6 = [(Scorpion(matrice, 10, 0.80)).cherche_Scorpion() for i in range(1,1001)]
	#y6 = np.array(y6)

	# the histogram of the data
	#n, bins, patches = plt.hist(y1, bins=100, range=(1,100), density=True, facecolor='#abdae1', alpha=0.75)
	#n, bins, patches = plt.hist(y2, bins=100, range=(1,100), density=True, facecolor='#776d5a', alpha=0.75)
	#n, bins, patches = plt.hist(y3, bins=100, range=(1,100), density=True, facecolor='#a09cb0', alpha=0.75)
	#n, bins, patches = plt.hist(y4, bins=100, range=(1,100), density=True, facecolor='#abdae1', alpha=0.75)
	#n, bins, patches = plt.hist(y5, bins=100, range=(1,100), density=True, facecolor='#776d5a', alpha=0.75)
	#n, bins, patches = plt.hist(y6, bins=100, range=(1,100), density=True, facecolor='#abdae1', alpha=0.90)

	#plt.xscale('log')
	#plt.yscale('log')
	#plt.xlabel('les coups avant la victoire', fontsize=12)
	#plt.ylabel('la densité de probabilité', fontsize=12)
	#plt.gca().legend(('Heuristique','Heuristique'))
	#plt.gca().legend(('Naïve','Naïve'))
	#plt.gca().legend(('Aléatoire','Aléatoire'))
	#plt.gca().legend(('Monte Carlo','Probabiliste'))

	# curve fitting geometrical distribution
	#def func_geom(k, p):
	#	return p*((1-p)**(k-1))

	#x_data = np.arange(1,101)
	#y_data = [func_geom(100-k, 0.17) for k in x_data]
	#y_data = np.array(y_data)
	#print(x_data)
	#print(y_data)
	#plt.plot(x_data, y_data, '#776d5a')
	#plt.gca().legend(('Distribution géométrique','Version aléatoire'))

	#plt.show()