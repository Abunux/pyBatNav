"""Module bn_stats

Implémente les classes :
	- Stats : outils d'étude statistique
 
Auteurs : Frédéric Muller et Lionel Reboul

Licence CC BY-NC-SA

Version 0.1.0"""


from bn_grille import *

from math import *

import numpy as np
import matplotlib.pyplot as plt



# Intégration de matplotlib dans tkinter : 
# http://matplotlib.org/examples/user_interfaces/embedding_in_tk.html


class Stats(object):
	"""Implémente les outils d'étude statistique"""
	def __init__(self, data=None, filename="", tmoy=0, param_grille={'xmax':10, 'ymax':10, 'taille_bateaux':[5, 4, 3, 3, 2]}, niveau_str="5"):
		# data est une liste d'effectifs : data[43] = nombre de parties à 43 coups
		# filename le nom du fichier où sont stockées les données
		# tmoy : temps moyen par partie de la simulation
		# param_grille : paramètres de la grille
		# niveau_str : le niveau de l'algorithme en chaine de caractères 
		#		(pour le niveau 4 : "4(100)" pour 100 échantillons)
		if data :
			self.data = data
		elif filename :
			self.filename = filename
			self.load_data()
		else :
			return
		
		self.get_all_stats()
		
		self.freq=[]
		for d in self.data :
			self.freq.append(d/self.effectif)
		
		# filename pour sauver les données
		if filename : 
			self.filename = filename
		else :
			self.filename = "distrib_HAL_niveau=%s_n=%d" % (self.niveau_str, self.effectif)
		
		self.tmoy = tmoy
		self.param_grille = param_grille
		self.niveau_str = niveau_str
	
	#
	# Chargement et sauvegarde des données (pour analyse future)--------
	#
	def load_data(self) :
		"""Charge les données à partir d'un fichier texte"""
		self.data = []
		with open(self.filename+".txt","r") as datafile:
			for v in datafile:
				self.data.append(int(v))
	
	def save_data(self):
		"""Sauvegarde les données dans un fichier texte"""
		with open(self.filename + ".txt", "w") as datafile :
			for k in range(len(self.data)) :
				datafile.write(str(self.data[k]) + '\n')
		
		# Sauvegarde dans un tableau en LaTeX :
		with open(self.filename + ".tex", "w") as datafile :
			for k in range(len(self.data)) :
				datafile.write(str(k) + " & " + str(self.data[k]) + r'\\' + '\n')
				datafile.write(r"\hline" + '\n')
		
	#
	# Récupération des paramètres statistiques basiques ----------------
	#
	def get_all_stats(self) :
		"""Récupère tous les indicateurs statistiques"""
		self.get_effectif()
		self.get_mini()
		self.get_maxi()
		self.get_quartiles()
		self.get_mode()
		self.get_moyenne()
		self.get_sigma()
	
	def resume_stat(self) :
		"""Affiche un résumé statistique"""
		print("Mini : %d" % self.mini)
		print("Q1 : %d" % self.quartiles[0])
		print("Med : %d" % self.quartiles[1])
		print("Q3 : %d" % self.quartiles[2])
		print("Maxi : %d" % self.maxi)
		print()
		print("Mode : %d" % self.mode)
		print()
		print("Moyenne : %.2f" % self.moyenne)
		print("Sigma : %.2f" % self.sigma)
	
	def get_effectif(self) :
		"""Calcul de l'effectif total"""
		self.effectif = sum(self.data)
	
	def get_mini(self):
		"""Calcul du minimum"""
		k = 0
		while self.data[k] == 0 and k < len(self.data):
			k += 1
		self.mini = k
	
	def get_maxi(self):
		"""Calcul du maximum""" 
		k = len(self.data)-1
		while self.data[k] == 0 and k >= 0:
			k -= 1
		self.maxi = k
	
	def get_quartiles(self):
		"""Calcul des quartiles. Renvoie une liste [Q1, Med, Q3].
		Q1 et Q2 sont les termes de rangs ceil(n/4) et ceil(3n/4)
		La médiane est définie comme le terme de rang ceil(n/2)""" 
		n = self.effectif
		indexes = [ceil(n/4), ceil(n/2), ceil(3*n/4)]
		cumules = [self.data[0]]
		for k in range(1,len(self.data)):
			cumules.append(cumules[k-1]+self.data[k])
		quartiles = [0, 0, 0]
		for k in range(len(cumules)):
			for i in range(3):
				if cumules[k]>=indexes[i] and cumules[k-1]<indexes[i] :
					quartiles[i] = k
		self.quartiles = quartiles
		
	def get_mode(self):
		"""Calcul du mode"""
		self.mode = self.data.index(max(self.data))
	
	def get_moyenne(self):
		"""Calcul de la moyenne"""
		n = self.effectif
		total = 0
		for k in range(len(self.data)):
			total += self.data[k]*k
		self.moyenne = total/n
	
	def get_sigma(self):
		"""Calcul de l'écart-type"""
		n = self.effectif
		m = self.moyenne
		total = 0
		for k in range(len(self.data)):
			total += self.data[k]*(k-m)**2
		variance = total/n
		self.sigma = sqrt(variance)
	
	#
	# Création de l'histogramme ----------------------------------------
	#
	def histogramme(self, show=True, save=True):
		"""Crée la représentation graphique des données avec :
			- Un histogramme des fréquences
			- Un diagramme en boîte à moustache
			- Tous les indicateurs statistiques"""
			
		# Récupération des indicateurs statistiques et des paramètres de la grille
		n = self.effectif
		mini = self.mini
		maxi = self.maxi
		mode = self.mode
		q1 = self.quartiles[0]
		mediane = self.quartiles[1]
		q3 = self.quartiles[2]
		moyenne = self.moyenne
		sigma = self.sigma
		tmoy = self.tmoy
		xmax = self.param_grille['xmax']
		ymax = self.param_grille['ymax']
		taille_bateaux = self.param_grille['taille_bateaux']
		niveau_str = self.niveau_str
		
		# Figure statistique 
		# ------------------
		fig = plt.figure()
		
		# Création de l'histogramme
		for k in range(self.mini, self.maxi+1):
			plt.bar(k-0.5, self.freq[k], width=1, bottom=0, color='g', alpha=0.75) 
		plt.text(mode, 0, r"$%d$" % mode, horizontalalignment='center', verticalalignment='bottom', bbox={'facecolor':'white', 'alpha':1, 'pad':2} )
		
		# Création du diagramme en boite
		  # Dimensions de la grille et des objets graphiques
		plt.ylim(ymin=0)
		gymin, gymax = plt.ylim()
		gxmin, gxmax = plt.xlim()
		yboite = (gymin+gymax)/2		# Position verticale de la boite
		hboite = (gymax-gymin)/10		# Hauteur de la boite
		hbornes = (gymax-gymin)/30		# Hauteur des taquets en xmin et xmax
		   # Q1, Med et Q3
		plt.hlines(yboite-hboite, q1, q3, linewidths=2)
		plt.hlines(yboite+hboite, q1, q3, linewidths=2)
		plt.vlines(q1, yboite-hboite, yboite+hboite, linewidths=2)
		plt.vlines(mediane, yboite-hboite, yboite+hboite, linewidths=2)
		plt.vlines(q3, yboite-hboite, yboite+hboite, linewidths=2)
		plt.text(q1, yboite, r"$%d$" % q1, horizontalalignment='center', verticalalignment='center', bbox={'facecolor':'white', 'alpha':1, 'pad':2} )
		plt.text(mediane, yboite, r"$%d$" % mediane, horizontalalignment='center', verticalalignment='center', bbox={'facecolor':'white', 'alpha':1, 'pad':2} )
		plt.text(q3, yboite, r"$%d$" % q3, horizontalalignment='center', verticalalignment='center', bbox={'facecolor':'white', 'alpha':1, 'pad':2} )
		#~ plt.text((q1+q3)/2, yboite-hboite, r"$Q_3-Q_1=%d$" % (q3-q1), horizontalalignment='center', verticalalignment='bottom', bbox={'facecolor':'white', 'alpha':1, 'pad':0} )
		   # Xmin et Xmax
		plt.hlines(yboite, mini, q1, linewidths=2)
		plt.hlines(yboite, q3, maxi, linewidths=2)
		plt.vlines(mini, yboite-hbornes, yboite+hbornes, linewidths=2)
		plt.vlines(maxi, yboite-hbornes, yboite+hbornes, linewidths=2)
		plt.text(mini, yboite, r"$%d$" % mini, horizontalalignment='center', verticalalignment='center', bbox={'facecolor':'white', 'alpha':1, 'pad':2} )
		plt.text(maxi, yboite, r"$%d$" % maxi, horizontalalignment='center', verticalalignment='center', bbox={'facecolor':'white', 'alpha':1, 'pad':2} )
		
		# Texte de résumé statistique
		plt.text(gxmin+(gxmax-gxmin)*0.05, gymin+(gymax-gymin)*0.95, 
					r"$\bar x=%.2f$" % moyenne + '\n' + "$\sigma=%.2f$" % sigma + '\n\n' + r"$t_{moy}=%.1f\,ms$" % (1000*tmoy), 
					horizontalalignment='left', verticalalignment='top', fontsize=15, bbox={'facecolor':'white', 'alpha':1, 'pad':15} )
		
		# Mise en forme et affichage du graphique
		plt.xlabel("Nombre de coups")
		plt.ylabel("Fréquence de parties")
		plt.title("Résolution par l'ordinateur sur n=%d parties\nNiveau=%s, Xmax=%d , Ymax=%d , Bateaux : %s" % (n, niveau_str, xmax, ymax," ".join([str(t) for t in taille_bateaux])))
		plt.grid(True)
		if save :
			plt.savefig(self.filename + ".png", dpi=fig.dpi)
		if show :
			plt.show()


if __name__ == "__main__" :
	pass
	#~ s = Stats(filename= "distrib_HAL_niveau=6_n=10000", tmoy=1.441, niveau_str="6(60)")
	#~ s.filename="distrib_HAL_niveau=6(60)_n=10000"
	#~ s.save_data()
	#~ s.histogramme(save=True)



# -------------------------------------------------------------------------------------------
#
#			POUBELLE
#
# -------------------------------------------------------------------------------------------

# Loi normale asymétrique
# https://fr.wikipedia.org/wiki/Loi_normale_asym%C3%A9trique
def gamma(distrib):
	m = moyenne(distrib)
	s = sigma(distrib)
	g = 0
	for k in range(len(distrib)) :
		g += distrib[k]*((k-m)/s)**3
	return g/sum(distrib)

def delta(distrib):
	g = abs(gamma(distrib))
	return sqrt(pi/2)*(g**(1/3))/sqrt(g**(2/3)+((4-pi)/2)**(2/3))

def norm_asym_param(distrib):
	d = delta(distrib)
	alpha = d/sqrt(1-d**2)
	omega = s/sqrt(1-2*d**2/pi)
	xi = m-omega*d*sqrt(2/pi)
	return {"alpha":alpha, "omega":omega, "xi":xi}

def phi(x):
	return 1/sqrt(2*pi)*exp(-x**2/2)

def Phi(x):
	return 0.5*(1+erf(x/sqrt(2)))
	
def f(x, omega, xi, alpha):
	return (2/omega)*phi((x-xi)/omega)*Phi(alpha*(x-xi)/omega)

#~ x = np.arange(mini, maxi,0.01)

#~ y = []
#~ for k in range(len(x)):
	#~ y.append(f(x[k],omega,xi,alpha))

#~ plt.plot(x, distrib_n, color='g')
#~ plt.plot(x,y, color='k')


from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html


def surface_probas(grille = GrilleSuivi()):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.view_init(elev=24., azim=106)

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Possibilités', rotation=180)
	labels = [chr(65+i) for i in range(10)]
	ax.set_xticklabels(labels)
	ax.invert_xaxis()

	# Divers réglages graphiques peu concluants...
	#~ ax.w_xaxis.pane.set_visible(False)
	#~ ax.w_xaxis.gridlines.set_visible(False)
	#~ ax.w_xaxis.line.set_visible(False)
	#~ ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
	#~ ax.set_axis_off()

	#~ grille.etat[(2,3)] = -1 # Petite variation sur la grille
	start = time()
	(case, pmax) = grille.case_max_echantillons(100, affiche=True)
	print("Temps : %.5f secondes" % (time()-start))
	
	ax.text(case[0],case[1],pmax,"Max=%d en %s" % (pmax, alpha(case)), ha="center")
	#~ ax.set_title("Échantillon de taile %d" % n)
	x = y = np.arange(0, 10, 1)
	X, Y = np.meshgrid(x, y)
	zs = np.array([grille.probas[(i,j)] for i,j in zip(np.ravel(X), np.ravel(Y))])
	Z = zs.reshape(X.shape)

	# Couleurs : http://matplotlib.org/examples/color/colormaps_reference.html
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.7)
	#~ surf2 = ax.plot_wireframe(X, Y, Z)

	fig.colorbar(surf, shrink=0.5, aspect=5)
	plt.show()

#~ if __name__ == "__main__" :
	#~ taille_bateaux=[2,3,3,4,5]
	#~ surface_probas(n=100000, grille=GrilleSuivi(taille_bateaux=taille_bateaux))
	#~ grille=GrilleSuivi()
	#~ for i in range(7):
		#~ for j in range(10):
			#~ grille.etat[(i,j)]=-1
	#~ cases=[(i,j) for i in range(grille.xmax) for j in range(grille.ymax)]
	#~ rand.shuffle(cases)
	
	#~ for k in range(20):
		#~ grille.etat[(rand.randrange(0, grille.xmax), rand.randrange(0, grille.ymax))] = -1
		#~ grille.etat[cases[k]]=-1
	#~ surface_probas(grille=grille)
