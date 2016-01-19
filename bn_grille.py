"""Module bn_grille

Implémente les classes :
	- Bateau : modélise un bateau
	- Grille : classe de base pour une grille
		- GrilleJoueur : dérivée de Grille, la grille où on place ses bateaux
		- GrilleSuivi : dérivée de Grille, la grille de suivi des coups
 
Auteurs : Frédéric Muller et Lionel Reboul

Licence CC BY-NC-SA

Version 0.1.0"""

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
		"""Crée une copie temporaire de la grille"""
		grille_tmp = Grille()
		for case in self.etat :
			grille_tmp.etat[case] = self.etat[case]
		grille_tmp.taille_bateaux = self.taille_bateaux[:]
		grille_tmp.vides = self.vides
		return grille_tmp
	
	#
	# Calculs de probabilités ------------------------------------------
	#
	def get_possibles(self, affiche=False):
		"""Crée la liste des bateaux possibles sur chaque case"""
		# --> Il reste quelques fonctions de tri qui ne sont pas utiles pour la suite, mais c'est juste pour l'affichage des tests
		self.update_vides()
		
		# Liste des bateaux et sens possibles sur chaque case
		# Par ex {(0,0):[(5,(1,0)), (5,(0,1)),...], (0,1):...}
		self.possibles_case = {}
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.possibles_case[(i,j)] = []
				
		# Récupère les éléments une seule fois de self.taille_bateaux, triés en ordre décroissant
		tmp_taille_bateaux = sorted(list(set(self.taille_bateaux)), reverse=True)
		
		# Regarde pour chaque case vide la taille maxi d'un bateau dans chaque direction
		for case in self.vides :
			for direction in [BN_DROITE, BN_BAS] :
				tmax = self.get_max_space(case, direction=direction, sens=0)
				self.possibles_case[case] += [(taille, direction) for taille in tmp_taille_bateaux if taille <= tmax]

		# Liste des cases et sens possibles pour chaque bateau
		# Par ex : {5:[((0,0), (1,0)), ((0,0), (0,1)), ((1,0), (1,0)),...], 4:...}
		self.possibles = {}
		for taille in tmp_taille_bateaux :
			self.possibles[taille] = []
		for case in self.possibles_case :
			for placement in self.possibles_case[case]:
				self.possibles[placement[0]].append((case, placement[1]))
		for taille in self.taille_bateaux :
			self.possibles[taille].sort()
		
		if affiche : # Pour les tests
			for case in grille.vides :
				print(case,grille.possibles_case[case])
			print()
			for taille in grille.possibles :
				print("Taille %d :" % taille)
				print("-----------")
				i=1
				for pos in grille.possibles[taille] :
					print(i,pos[0], pos[1])
					i+=1
				print() 
			
	
	def case_max(self, affiche=False):
		"""Détermine la case qui contient le plus de bateaux et
		regardant sur chaque case le nombre de bateaux possibles"""
		
		# Dictionnaire contenant les probas de chaque case
		self.probas = {}
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.probas[(i,j)] = 0
		
		self.get_possibles()
		
		for taille in self.taille_bateaux :
			for (case, direction) in self.possibles[taille] :
				for k in range(taille) :
					self.probas[(case[0]+k*direction[0], case[1]+k*direction[1])] += 1
		
		# Calcul des probas
		#~ for case in self.probas :
			#~ self.probas[case] *= 1/len(self.vides)
		
		# Détermination de la case la plus probable
		self.case_proba = (0,0)
		self.pmax = 0
		for case in self.probas :
			if self.probas[case] > self.pmax :#and (case[0]+case[1])%2 == 0:
				self.pmax = self.probas[case]
				self.case_proba = case
		
		# Affichages pour les tests
		if affiche :
			for j in range(self.ymax):
				for i in range(self.xmax-1):
					print("%.4f"%(self.probas[(i,j)]), end=' ')
				print("%.4f"%self.probas[(self.xmax-1,j)])
			
			print()
			print("Temps : %.4f secondes" % (time()-start))
			print("Case max :", self.case_proba)
			print("Proba max : %.5f" % self.pmax)
		
		# Retourne la case la plus probable et sa proba
		return (self.case_proba, self.pmax)
	
	def case_max_touchee(self, case_touchee):
		"""Retourne le nombre de bateaux possibles
		sur chaque case adjacentes à case (qui vient d'être touchée)"""
		# --> Sera appelé dans Ordi.shuffle_queue() pour trier la file quand on touche
		# --> Code à améliorer (trop bordélique)
		
		# On marque temporairement la case comme vide pour pouvoir tester si on peut y placer des bateaux
		self.etat[case_touchee] = 0
		
		self.get_possibles()
		probas = {}
		for case in self.adjacent(case_touchee) :
			probas[case] = 0
			
		for taille in self.taille_bateaux :
			# Bateaux horizontaux possibles
			direction = (1, 0)
				# Bateau qui se termine sur case_touchee
				# On ajoute 1 à sa case à gauche
			if case_touchee[0]-(taille-1)*direction[0] >= 0 and \
				((case_touchee[0]-(taille-1)*direction[0], case_touchee[1]), direction) in self.possibles[taille]:
					probas[(case_touchee[0]-1, case_touchee[1])] += 1
				# Bateaux à cheval strictement sur case_touchee
				# On ajoute 1 à gauche et à droite
			for k in range(1, taille-1) :
				if case_touchee[0]-k*direction[0] >= 0 and \
					((case_touchee[0]-k*direction[0], case_touchee[1]), direction) in self.possibles[taille]:
					probas[(case_touchee[0]-1, case_touchee[1])] += 1
					probas[(case_touchee[0]+1, case_touchee[1])] += 1
				# Bateau qui démarre sur case_touchee
				# On ajoute 1 à droite
			if ((case_touchee[0], case_touchee[1]), direction) in self.possibles[taille]:
					probas[(case_touchee[0]+1, case_touchee[1])] += 1
					
			# Bateaux verticaux possibles
			direction = (0, 1)
				# Bateau qui se termine sur case_touchee
				# On ajoute 1 à sa case au-dessus
			if case_touchee[1]-(taille-1)*direction[1] >= 0 and \
				((case_touchee[0], case_touchee[1]-(taille-1)*direction[1]), direction) in self.possibles[taille]:
					probas[(case_touchee[0], case_touchee[1]-1)] += 1
				# Bateaux à cheval strictement sur case_touchee
				# On ajoute 1 à au-dessus et en-dessous
			for k in range(1, taille-1) :
				if case_touchee[1]-k*direction[1] >= 0 and \
					((case_touchee[0], case_touchee[1]-k*direction[1]), direction) in self.possibles[taille]:
					probas[(case_touchee[0], case_touchee[1]-1)] += 1
					probas[(case_touchee[0], case_touchee[1]+1)] += 1
				# Bateau qui démarre sur case_touchee
				# On ajoute 1 en-dessous
			if ((case_touchee[0], case_touchee[1]), direction) in self.possibles[taille]:
					probas[(case_touchee[0], case_touchee[1]+1)] += 1
		
		# On remet la case comme touchée
		self.etat[case_touchee] = 1
		
		# Retour des probas (en fait juste le nombre de bateaux possibles)
		probas_liste = [(case, probas[case]) for case in probas]
		return sorted(probas_liste, key=lambda proba: proba[1], reverse = True)
		
	

	

	#
	# Gestion des espaces impossibles ----------------------------------
	#
	def get_max_space(self, case, direction=BN_ALLDIR, sens=1):
		"""Renvoie la plus grande place possible sur cette case 
		dans une direction"""
		# sens = 0 : ne compte qu'à droite ou en bas (pour l'IA)
		# car BN_DROITE=BN_HORIZONTAL et BN_BAS=BN_VERTICAL, donc obligé de spécifier
		if direction == BN_ALLDIR:
			return max(self.get_max_space(case, BN_HORIZONTAL), self.get_max_space(case, BN_VERTICAL))
		
		m = 1
		# Comptage des cases libres dans un seul sens
		x = case[0]
		y = case[1]
		while self.test_case((x+direction[0], y+direction[1])):
			m += 1
			x += direction[0]
			y += direction[1]
		if sens == 1 :
			# Comptage des cases libres sur toute une direction
			x = case[0]
			y = case[1]
			while self.test_case((x-direction[0], y-direction[1])):
				m += 1
				x -= direction[0]
				y -= direction[1]
		return m
		
	def elimine_cases(self):
		"""Élimine les cases dans lesquelles
		le plus petit bateau ne peut pas rentrer"""
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
		
	
	
	def add_bateau(self, bateau):
		"""Ajoute un bateau dans la grille
		et met à jour les états des cases adjacentes"""
		if self.test_bateau(bateau):
			for case in bateau.cases :
				self.etat[case] = 1
			for case in bateau.cases_adj:
				if self.test_case(case):
					self.etat[case] = -1
	
	def init_bateaux_alea(self, ordre='random'):
		"""Initialise une grille avec des bateaux aléatoires"""
		ok = False
		nb_bateaux = 0
		while nb_bateaux < len(self.taille_bateaux) :
			nb_bateaux = 0
			gtmp = self.copie_grille_tmp()
			for taille in self.taille_bateaux :
				gtmp.get_possibles()
				if not gtmp.possibles[taille] :
					break
				else :
					(case, direction) = rand.choice(gtmp.possibles[taille])
					gtmp.add_bateau(Bateau(taille, case, direction))
					nb_bateaux += 1
		self.etat = gtmp.etat

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
		"""Affiche la grille
		Méthode à surcharger suivant l'interface"""
		pass
				
	# --------------------------------
	# Poubelle 
	# Méthodes plus utilisées (backup)
	# --------------------------------
	#~ 
	# --> Les deux méthodes suivantes sont appelées à disparaître
	# --> Mais je les laisse pour des raisons temporaires de compatibilité
	# --> Elles sont utilisées dans le placement aléatoire de bateaux du joueur
	# --> Mais à terme il faudra une option pour placer directement tous les bateaux
	# --> de manière aléatoire d'un coup avec init_bateaux_alea(self)
	def make_bateau_alea(self, taille):
		"""Crée un bateau aléatoire (pas forcément valide)"""
		(x,y) = rand.choice(self.vides)
		dir_possibles = []
		if x >= taille-1 :
			dir_possibles.append(BN_GAUCHE)
		if x <= self.xmax - taille :
			dir_possibles.append(BN_DROITE)
		if y >= taille-1 :
			dir_possibles.append(BN_HAUT)
		if y <= self.ymax - taille :
			dir_possibles.append(BN_BAS)
		sens = rand.choice(dir_possibles)
		bateau = Bateau(taille, (x,y), sens)
		return bateau
		
	def add_bateau_alea(self, taille, nb_essais_max=20):
		"""Ajoute un bateau aléatoire (valide)"""
		# Essaie de placer un bateau aléatoire nb_essais_max fois
		# et quitte s'il n'y arrive pas, pour éviter une situation de blocage
		valide = False
		nb_essais = 0
		while not valide and nb_essais < nb_essais_max:
			nb_essais += 1
			bateau = self.make_bateau_alea_bak(taille)
			valide = self.test_bateau(bateau)
		if valide :
			self.add_bateau(bateau)
			return True
		else :
			return False
	#~ 
		#~ 
	#~ def make_bateau_alea_bak(self, taille):
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
		
	def make_bateau_alea_bak(self, taille):
		"""Crée un bateau aléatoire (pas forcément valide)"""
		x = rand.randrange(0, self.xmax)
		y = rand.randrange(0, self.ymax)
		#~ #self.update_vides()
		#~ #(x,y) = rand.choice(self.vides)
		sens = rand.choice([BN_DROITE, BN_GAUCHE, BN_HAUT, BN_BAS])
		bateau = Bateau(taille, (x,y), sens)
		return bateau
	#~ 
	
			#~ 
	#~ def add_bateau_alea_bak(self, taille):
		#~ """Ajoute un bateau aléatoire (valide)"""
		#~ valide = False
		#~ while not valide:
			#~ bateau = self.make_bateau_alea(taille)
			#~ valide = self.test_bateau(bateau)
	#~ 
	#~ def init_bateaux_alea(self, ordre='random'):
		#~ """Initialise une grille avec des bateaux aléatoires"""
		#~ # L'odre dans lequel on place les bateaux a une influence sur les probas !!!
		#~ tmp_taille_bateaux = self.taille_bateaux[:]
		#~ if ordre == 'random' :
			#~ rand.shuffle(tmp_taille_bateaux)
		#~ elif ordre == 'croissant' :
			#~ tmp_taille_bateaux.sort()
		#~ elif ordre == 'decroissant' :
			#~ tmp_taille_bateaux.sort()
			#~ tmp_taille_bateaux = tmp_taille_bateaux[::-1]
			#~ 
		#~ ok = False
		#~ while not ok :
			#~ ok = True
			#~ gtmp = self.copie_grille_tmp()
			#~ for taille in tmp_taille_bateaux :
				#~ valide = gtmp.add_bateau_alea(taille)
				#~ ok = ok and valide
#~ 
		#~ self.etat = gtmp.etat
			#~ 
	def init_bateaux_alea_bak(self, ordre='random'):
		"""Initialise une grille avec des bateaux aléatoires"""
		# L'ordre dans lequel on place les bateaux a une influence sur les probas !!!
		tmp_taille_bateaux = self.taille_bateaux[:]
		if ordre == 'random' :
			rand.shuffle(tmp_taille_bateaux)
		elif ordre == 'croissant' :
			tmp_taille_bateaux.sort()
		elif ordre == 'decroissant' :
			tmp_taille_bateaux.sort()
			tmp_taille_bateaux = tmp_taille_bateaux[::-1]
		
		for taille in tmp_taille_bateaux :
			self.add_bateau_alea(taille)
			#~ 
	def case_max_echantillons(self, nb_echantillons=1000, ordre='decroissant'):
		"""Calcul des probabilités sur chaque case vide de contenir
		un bateau. Retourne la case la plus probable en essayant 
		différents arrangements des bateaux restants"""
		start=time()
		
		# Dictionnaire contenant les probas de chaque case
		self.probas = {}
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.probas[(i,j)] = 0
		
		# On crée différents arrangements aléatoires de bateaux
		for k in range(nb_echantillons):
			# On utilise une grille temporaire, copiée à partir de la grille_suivi courante
			grille_tmp = self.copie_grille_tmp()
			# Arrangement aléatoire de bateaux et récupération des cases occupées
			grille_tmp.init_bateaux_alea_bak(ordre=ordre)
			for case in grille_tmp.etat :
				if self.etat[case] == 0 and grille_tmp.etat[case] == 1 :
					self.probas[case] += 1
		# Calcul des probas
		for case in self.probas :
			self.probas[case] *= 1/nb_echantillons
		
		# Détermination de la case la plus probable
		case_max = (0,0)
		pmax = 0
		for case in self.probas :
			if self.probas[case] > pmax :#and (case[0]+case[1])%2 == 0:
				pmax = self.probas[case]
				case_max = case
		
		# Retourne la case la plus probable et sa proba
		return (case_max, pmax)
		
	#~ def affiche(self):
		#~ """Affiche la grille"""
		#~ # Méthode à surcharger suivant l'interface
		#~ # --> À virer d'ici (juste temporaire pour tests)
		#~ pass
		#~ CAR_H=u'\u2500'		# Trait Horizontal
		#~ CAR_V=u'\u2502'		# Trait Vertical
		#~ # Coins
		#~ CAR_CHG=u'\u250C'	# Coin Haut Gauche
		#~ CAR_CHD=u'\u2510'	# Coin Haut Droite
		#~ CAR_CBG=u'\u2514'	# Coin Bas Gauche
		#~ CAR_CBD=u'\u2518'	# Coin Bas Droite
		#~ # T
		#~ CAR_TH=u'\u252C'	# T Haut
		#~ CAR_TB=u'\u2534'	# T Bas
		#~ CAR_TG=u'\u251C'	# T Gauche
		#~ CAR_TD=u'\u2524'	# T Droite
		#~ # +
		#~ CAR_CX=u'\u253C'	# Croix centrale
		#~ # Touché / Manqué
		#~ CAR_TOUCH = u'\u2716' # ou u'\u2737', u'\u3718'
		#~ CAR_MANQ = u'\u25EF'
#~ 
		#~ # Ligne du haut
		#~ print('    '+CAR_CHG+(CAR_H*3+CAR_TH)*(self.xmax-1)+CAR_H*3+CAR_CHD)
		#~ 
		#~ # Ligne des lettres des colonnes
		#~ print('    '+CAR_V, end='')
		#~ for i in range(self.xmax):
			#~ if i!=self.xmax-1 :
				#~ print(' '+str(i)+' ', end=CAR_V)
			#~ else :
				#~ print(' '+str(i)+' '+CAR_V)
				#~ 
		#~ #Ligne sous les lettres
		#~ print(CAR_CHG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)
		#~ 
		#~ # Lignes suivantes
		#~ for j in range(self.ymax):
			#~ # 1ère colonne (chiffres des lignes)
			#~ chaine = CAR_V+' '+str(j)+' '+CAR_V
			#~ 
			#~ # Cases suivantes
			#~ for i in range(self.xmax):
				#~ if self.etat[(i,j)] == 1 :
					#~ symbole = CAR_TOUCH
				#~ elif self.etat[(i,j)] == -1 :
					#~ symbole = CAR_MANQ
				#~ else :
					#~ symbole = ' '
				#~ chaine += ' '+symbole+' '+CAR_V
			#~ print(chaine)
			#~ 
			#~ # Sépartion lignes intermédiaires
			#~ if j!=self.ymax-1 :
				#~ print(CAR_TG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)
				#~ 
			#~ # Dernière ligne
			#~ else :
				#~ print(CAR_CBG+(CAR_H*3+CAR_TB)*self.xmax+CAR_H*3+CAR_CBD)

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
class GrilleSuivi(Grille):
	"""La grille de suivi des coups joués"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
if __name__ == "__main__" :
	grille = GrilleSuivi()
	grille.etat[(1,2)]=1
	grille.etat[(3,2)]=-1
	print(grille.case_max_touchee((1,2)))
	#~ for i in range(7):
		#~ for j in range(10):
			#~ grille.etat[(i,j)]=-1
	#~ grille.get_possibles()?
	#~ print(grille.possibles)
	#~ input()
	#~ for taille in grille.possibles :
		#~ print("Taille %d :" % taille)
		#~ print("-----------")
		#~ i=1
		#~ for pos in grille.possibles[taille] :
			#~ print(i,pos[0], pos[1])
			#~ i+=1
		#~ print() 
	#~ for case in grille.vides :
		#~ print(case,grille.possibles_case[case])
	#~ quit()
	# Essai de calcul de probabilité pour chaque case de contenir un bateau
	#~ grille = GrilleSuivi()

		#~ 
	#~ start = time()
	#~ grille.init_bateaux_alea()
	#~ print(time()-start)
	#~ grille.affiche()
	#~ quit()
	#~ 
	#~ quit()
	#~ n = int(input("Taille de l'échantillon : "))
	#~ print()
	#~ start = time()
	#~ grille.case_max(100)
	#~ print(time()-start)
	
