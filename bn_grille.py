#
# Module bn_grille
#
# Implémente les classes :
#	- Bateau : modélise un bateau
#	- Grille : classe de base pour une grille
#		- GrilleJoueur : dérivée de Grille, la grille où on place ses bateaux
#		- GrilleSuivi : dérivée de Grille, la grille de suivi des coups
# 
# Auteurs : Frédéric Muller et Lionel Reboul
#
# Licence CC BY-NC-SA
#
# Version 0.1.0
#

import random as rand
from time import time

from bn_utiles import *

#
#----------------------------------------------------------------------------------------------------------------
#
class Bateau(object):
	"""Classe pour définir les bateaux"""
	def __init__(self, taille, start, sens):
		"""Un bateau est défini par :
			- Sa taille
			- Son point de départ (start)
			- Son sens (DROITE, GAUCHE, BAS, HAUT)
		On récupère les cases occupées par le bateau
		ainsi que les cases adjacentes"""
		
		self.taille = taille
		self.start = start
		self.sens = sens
		self.end = (self.start[0]+(self.taille-1)*self.sens[0] , self.start[1]+(self.taille-1)*self.sens[1])
		
		# Récupération des cases occupées par le bateau
		self.cases = []
		for k in range(taille):
			self.cases.append((self.start[0]+k*self.sens[0] , self.start[1]+k*self.sens[1]))
		
		# Récupération des cases adjacentes
		self.cases_adj = []
		self.cases_adj.append((self.start[0]-self.sens[0] , self.start[1]-self.sens[1]))
		self.cases_adj.append((self.end[0]+self.sens[0] , self.end[1]+self.sens[1]))
		for k in range(taille):
			self.cases_adj.append((self.cases[k][0]+self.sens[1] , self.cases[k][1]+self.sens[0]))
			self.cases_adj.append((self.cases[k][0]-self.sens[1] , self.cases[k][1]-self.sens[0]))
#
#----------------------------------------------------------------------------------------------------------------
#
class Grille(object):
	"""Classe pour définir la grille de jeu"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		"""Initialisation de la grille de jeu
		Les cases sont numérotées de 0 à (x|y)max-1"""
		# Liste des bateaux
		self.taille_bateaux_init = taille_bateaux[:]
		self.taille_bateaux = taille_bateaux[:]
		# Taille du plus grand et du plus petit bateau
		self.get_taille_max()
		self.get_taille_min()
		# Nombre de cases totales à toucher
		self.somme_tailles = sum(self.taille_bateaux)
		
		# Dimensions de la grille
		self.xmax = xmax
		self.ymax = ymax
		
		# État de chaque case : dictionnaire self.etat[case], où case = (i,j)
		#	1  : Contient un bateau
		#	-1 : Ne peut pas contenir de bateau, ou déjà joué et manqué
		#	0  : Case vide
		# Intérêts d'un dictionnaire par rapport à une liste double :
		#	- Plus facile à manipuler
		#	- Recherche plus efficace (table de hachage, donc recherche en O(1))
		self.etat = {}
		
		# Liste des cases vides
		self.vides = []
		
		# Initialisation de la grille
		self.reinit()
	
	#
	# Gestion de la grille ---------------------------------------------
	#
	def reinit(self):
		"""Réinitialisation de la grille"""
		self.etat = {}
		self.vide = []
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.etat[(i,j)] = 0
				self.vides.append((i,j))
				
	def update_vides(self):
		"""Met à jour la liste des cases vides"""
		# --> À optimiser mais remove ne marche pas... (j'ai essayé)
		self.vides = []
		for i in range(self.xmax):
			for j in range(self.ymax):
				if self.etat[(i,j)] == 0 :
					self.vides.append((i,j))
		
	def update(self):
		"""Met à jour les paramètres de la grille"""
		self.update_vides()
		self.get_taille_max()
		self.get_taille_min()
	
	def is_touche(self, case):
		"""Test si la case contient un bateau"""
		return self.etat[case] == 1
	
	#
	# Gestion des cases ------------------------------------------------
	#
	def test_case(self, case):
		"""Test si une case est valide (dans la grille) et vide"""
		return 0 <= case[0] < self.xmax and 0 <= case[1] < self.ymax and self.etat[case] == 0
	
	def adjacent(self, case):
		"""Retourne la liste des cases vides adjacentes à case
		dans l'ordre : DROITE, GAUCHE, HAUT, BAS"""
		adj = []
		for d in [BN_DROITE, BN_GAUCHE, BN_HAUT, BN_BAS]:
			case_adj = (case[0]+d[0] , case[1]+d[1])
			if  self.test_case(case_adj):
				adj.append(case_adj)
		return adj
	
	def copie_grille_tmp(self):
		"""Crée une copie temporaire e la grille"""
		grille_tmp = Grille()
		for case in self.etat :
			grille_tmp.etat[case] = self.etat[case]
		grille_tmp.taille_bateaux = self.taille_bateaux[:]
		return grille_tmp
	
	#
	# Calculs de probabilités ------------------------------------------
	# Marche pas !!!...
	#
	def case_max(self, n=1000):
		"""Essai de calcul des probabilité de cases touchée sur chaque case restante
		Retourne la case la plus probable en essayant différents arrangements des bateaux restants
		Marche pas... (pb dans Grille.make_bateau_alea(), fait une boucle infinie)"""
		start=time()
		
		# Dico contenant les probas de chaque case
		self.probas = {}
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.probas[(i,j)]=0
		
		# On crée différents arrangements aléatoires de bateaux
		for k in range(n):
			# On utilise une grille tempoaraire, copiée à partir de la grille_suivi courante
			grille_tmp = self.copie_grille_tmp()
			# Arrangement aléatoire de bateaux
			grille_tmp.init_bateaux_alea()
			for case in grille_tmp.etat :
				if self.etat[case] == 0 and grille_tmp.etat[case] == 1 :
					self.probas[case] += 1
		# Calcul des probas
		for case in self.probas :
			self.probas[case] *= 1/n
		
		# Détermination de la case la plus probable, parmi les cases "noires"
		case_max = (0,0)
		pmax = 0
		for case in self.probas :
			if self.probas[case] > pmax :#and (case[0]+case[1])%2 == 0:
				pmax = self.probas[case]
				case_max = case
		
		# Affichages pour les tests
		for j in range(self.ymax):
			for i in range(self.xmax-1):
				print("%.4f"%(self.probas[(i,j)]), end=' ')
			print("%.4f"%self.probas[(self.xmax-1,j)])
		
		print()
		print("Échantillon de taille %d" % n)
		print("Temps : %.4f secondes" % (time()-start))
		print("Case max :", case_max)
		print("Proba max : %.5f" % pmax)
		
		# Retourne la case la plus probable et sa proba
		return (case_max, pmax)

	#
	# Gestion des espaces impossibles ----------------------------------
	#
	def get_max_space(self, case, direction=BN_ALLDIR):
		"""Renvoie la plus grande place possible sur cette case dans une direction"""		
		if direction == BN_ALLDIR:
			return max(self.get_max_space(case, BN_HORIZONTAL), self.get_max_space(case, BN_VERTICAL))
		
		m = 1
		# Comptage des cases libres à gauche ou en haut
		x = case[0]
		y = case[1]
		while self.test_case((x-direction[0], y-direction[1])):
			m += 1
			x -= direction[0]
			y -= direction[1]
		# Comptage des cases libres à droite ou en bas
		x = case[0]
		y = case[1]
		while self.test_case((x+direction[0], y+direction[1])):
			m += 1
			x += direction[0]
			y += direction[1]
		return m
		
	def elimine_cases(self):
		"""Élimine les cases dans lesquelles le plus petit bateau ne peut pas rentrer"""
		self.get_taille_min()
		self.update_vides()
		cases_eliminees = []
		for case in self.vides :
			if 0 < self.get_max_space(case) < self.taille_min :
				self.etat[case] = -1
				cases_eliminees.append(case)
		self.update_vides()
		return cases_eliminees

	#
	# Gestion des tailles des bateaux ----------------------------------
	#
	def get_taille_max(self):
		"""Met à jour la taille du bateau le plus grand restant"""
		if self.taille_bateaux :
			self.taille_max = max(self.taille_bateaux)
		else :
			self.taille_max = 0
	
	def get_taille_min(self):
		"""Met à jour la taille du bateau le plus petit restant"""
		if self.taille_bateaux :
			self.taille_min = min(self.taille_bateaux)
		else :
			self.taille_min = 0
	
	def rem_bateau(self, taille):
		"""Enlève le bateau de taille taille de la liste"""
		self.taille_bateaux.remove(taille)
		self.get_taille_max()
		self.get_taille_min()

	#
	# Gestion des bateaux sur la grille ------------------------------------
	#
	def test_bateau(self, bateau):
		"""Test si le bateau est valide (rentre bien) dans la grille"""
		for case in bateau.cases :
			if not self.test_case(case):
				return False
		return True
	
	def add_bateau(self,bateau):
		"""Ajoute un bateau dans la grille et met à jour les états des cases adjacentes"""
		if self.test_bateau(bateau):
			for case in bateau.cases :
				self.etat[case] = 1
			for case in bateau.cases_adj:
				if self.test_case(case):
					self.etat[case] = -1
	
	def make_bateau_alea(self, taille):
		"""Crée un bateau aléatoire (pas forcément valide)"""
		x = rand.randrange(0, self.xmax)
		y = rand.randrange(0, self.ymax)
		#~ #self.update_vides()
		#~ #(x,y) = rand.choice(self.vides)
		sens = rand.choice([BN_DROITE, BN_GAUCHE, BN_HAUT, BN_BAS])
		bateau = Bateau(taille, (x,y), sens)
		return bateau
		
	#~ def make_bateau_alea(self, taille):
		#~ """Crée un bateau aléatoire (valide)"""
		#~ self.update_vides()
		#~ grille_tmp = self.copie_grille_tmp()
		#~ 
		#~ dir_possibles = []
		#~ while not dir_possibles :
			#~ (x,y) = rand.choice(self.vides)
			#~ for sens in [BN_DROITE, BN_GAUCHE, BN_HAUT, BN_BAS] :
				#~ if grille_tmp.test_bateau(Bateau(taille, (x,y), sens)):
					#~ dir_possibles.append(sens)
		#~ sens = rand.choice(dir_possibles)
		#~ bateau = Bateau(taille, (x,y), sens)
		#~ return bateau
	
	def add_bateau_alea(self, taille):
		"""Ajoute un bateau aléatoire (valide)"""
		#~ self.update_vides()
		valide = False
		while not valide :
			bateau = self.make_bateau_alea(taille)
			valide = self.test_bateau(bateau)
		self.add_bateau(bateau)
	
	def init_bateaux_alea(self):
		"""Initialise une grille avec des bateaux aléatoires"""
		for taille in self.taille_bateaux[::-1] :
			self.add_bateau_alea(taille)
	
	# 
	# Fin de partie ----------------------------------------------------
	#
	def fini(self):
		"""Renvoie True si tous les bateaux ont été coulés"""
		somme_touches = 0
		for case in self.etat :
			if self.etat[case] == 1 :
				somme_touches += 1
		return somme_touches == self.somme_tailles
	
	#
	# Affichage --------------------------------------------------------
	#
	def affiche(self):
		"""Affiche la grille"""
		# Méthode à surcharger suivant l'interface
		pass
	

# ---------------------------------------------------------------------------------------------------------------------------
# Les deux clases suivantes, héritées de Grille ont pour rôle de distinguer les fonctions spécifiques à chaque type de grille
# (Non utilisé pour l'instant)
# ---------------------------------------------------------------------------------------------------------------------------

class GrilleJoueur(Grille):
	"""La grille sur laquelle chaque joueur place ses bateaux"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuivi(GrilleJoueur):
	"""La grille de suivi des coups joués"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
if __name__ == "__main__" :
	# Essai de calcul de probabilité pour chaque case de contenir un bateau
	grille = GrilleSuivi()
	n = int(input("Taille de l'échantillon : "))
	print()
	grille.case_max(n)
	
