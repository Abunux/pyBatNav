#
# Projet de bataille navale
# dans le cadre de la formation ISN
#
# Auteurs : Frédéric Muller et Lionel Reboul
#
# Projet démarré le 14/11/2015
# Dernière màj : 27/11/2015
# Version 0.0.17
#
# Licence CC BY-NC-SA
#

import random as rand
import os
from time import time

#
# Constantes ----------------------------------------------------------------------------------------------------
#
BN_DROITE = BN_HORIZONTAL =(1, 0)
BN_GAUCHE = (-1, 0)
BN_BAS = BN_VERTICAL = (0, 1)
BN_HAUT = (0, -1)
BN_ALLDIR = (1,1)

#
# Fonctions utiles ----------------------------------------------------------------------------------------------
#
def clear():
	"""Efface la console"""
	# http://stackoverflow.com/questions/2084508/clear-terminal-in-python
	if (os.name == 'nt'):    
		c = os.system('cls')
	else:
		c = os.system('clear')
	del c 

def info(*args):
	"""Affiche les infos de débug"""
	print(*args)
	
def signe(x):
	"""Retourne le signe de x"""
	if x > 0 : return 1
	elif x < 0 : return -1
	else : return 0

def alpha(case) :
	"""Convertit les coordonnées de case en notation du jeu
	Par ex (2,3) devient "C3" """
	return chr(case[0]+65)+str(case[1])

#
#----------------------------------------------------------------------------------------------------------------
#
class Bateau :
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
		
		# Récupération des casses occupées par le bateau
		self.cases = []
		for k in range(taille) :
			self.cases.append((self.start[0]+k*self.sens[0] , self.start[1]+k*self.sens[1]))
		
		# Récupération des cases adjacentes
		self.cases_adj = []
		self.cases_adj.append((self.start[0]-self.sens[0] , self.start[1]-self.sens[1]))
		self.cases_adj.append((self.end[0]+self.sens[0] , self.end[1]+self.sens[1]))
		for k in range(taille) :
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
				
	def update_vides(self) :
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
	
	def adjacent(self, case) :
		"""Retourne la liste des cases vides adjacentes à case
		dans l'ordre : DROITE, GAUCHE, HAUT, BAS"""
		adj = []
		for d in [BN_DROITE, BN_GAUCHE, BN_HAUT, BN_BAS]:
			case_adj = (case[0]+d[0] , case[1]+d[1])
			if  self.test_case(case_adj):
				adj.append(case_adj)
		return adj

	#
	# Gestion des tailles des bateaux ----------------------------------
	#
	def get_taille_max(self) :
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
	# Affichage --------------------------------------------------------
	#
	def affiche(self):
		"""Affiche la grille avec des caractère graphiques"""
		# Caractères pour faire la grille
		# -------------------------------
		# http://www.unicode.org/charts/
		# Traits
		CAR_H=u'\u2500'		# Trait Horizontal
		CAR_V=u'\u2502'		# Trait Vertical
		# Coins
		CAR_CHG=u'\u250C'	# Coin Haut Gauche
		CAR_CHD=u'\u2510'	# Coin Haut Droite
		CAR_CBG=u'\u2514'	# Coin Bas Gauche
		CAR_CBD=u'\u2518'	# Coin Bas Droite
		# T
		CAR_TH=u'\u252C'	# T Haut
		CAR_TB=u'\u2534'	# T Bas
		CAR_TG=u'\u251C'	# T Gauche
		CAR_TD=u'\u2524'	# T Droite
		# +
		CAR_CX=u'\u253C'	# Croix centrale
		# Touché / Manqué
		CAR_TOUCH = u'\u2716' # ou u'\u2737', u'\u3718'
		CAR_MANQ = u'\u25EF'

		# Ligne du haut
		print('    '+CAR_CHG+(CAR_H*3+CAR_TH)*(self.xmax-1)+CAR_H*3+CAR_CHD)
		
		# Ligne des lettres des colonnes
		print('    '+CAR_V, end='')
		for i in range(self.xmax):
			if i!=self.xmax-1 :
				print(' '+chr(i+65)+' ', end=CAR_V)
				#~ print(' '+str(i)+' ', end=CAR_V)
			else :
				print(' '+chr(i+65)+' '+CAR_V)
				#~ print(' '+str(i)+' '+CAR_V)
				
		#Ligne sous les lettres
		print(CAR_CHG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)
		
		# Lignes suivantes
		for j in range(self.ymax):
			# 1ère colonne (chiffres des lignes)
			chaine = CAR_V+' '+str(j)+' '+CAR_V
			
			# Cases suivantes
			for i in range(self.xmax) :
				if self.etat[(i,j)] == 1 :
					symbole = CAR_TOUCH
				elif self.etat[(i,j)] == -1 :
					symbole = CAR_MANQ
				else :
					symbole = ' '
				chaine += ' '+symbole+' '+CAR_V
			print(chaine)
			
			# Sépartion lignes intermédiaires
			if j!=self.ymax-1 :
				print(CAR_TG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)
				
			# Dernière ligne
			else :
				print(CAR_CBG+(CAR_H*3+CAR_TB)*self.xmax+CAR_H*3+CAR_CBD)
	

# ---------------------------------------------------------------------------------------------------------------------------
# Les deux clases suivantes, héritées de Grille ont pour rôle de distinguer les fonctions spécifiques à chaque type de grille
# ---------------------------------------------------------------------------------------------------------------------------

class GrilleJoueur(Grille):
	"""La grille sur laquelle chaque joueur place ses bateaux"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

	#
	# Gestion des bateaux sur la grille ------------------------------------
	#
	def test_bateau(self, bateau):
		"""Test si le bateau est valide (rentre bien) dans la grille"""
		for case in bateau.cases :
			if not self.test_case(case) :
				return False
		return True
	
	def add_bateau(self,bateau):
		"""Ajoute un bateau dans la grille et met à jour les états des cases adjacentes"""
		if self.test_bateau(bateau):
			for case in bateau.cases :
				self.etat[case] = 1
			for case in bateau.cases_adj :
				if self.test_case(case):
					self.etat[case] = -1
					
	def make_bateau_alea(self, taille):
		"""Crée un bateau aléatoire (pas forcément valide)"""
		x = rand.randint(0, self.xmax-1)
		y = rand.randint(0, self.ymax-1)
		sens = rand.choice([BN_DROITE, BN_GAUCHE, BN_HAUT, BN_BAS])
		bateau = Bateau(taille, (x,y), sens)
		return bateau
	
	def add_bateau_alea(self, taille):
		"""Ajoute un bateau aléatoire (valide)"""
		#~ bateau = self.make_bateau_alea(taille)
		valide = False
		while not valide :
			bateau = self.make_bateau_alea(taille)
			valide = self.test_bateau(bateau)
		self.add_bateau(bateau)
	
	def init_bateaux_alea(self):
		"""Initialise une grille avec des bateaux aléatoires"""
		for taille in self.taille_bateaux :
			self.add_bateau_alea(taille)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuivi(Grille):
	"""La grille de suivi des coups joués"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

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
		while self.test_case((x-direction[0], y-direction[1])) :
			m += 1
			x -= direction[0]
			y -= direction[1]
		# Comptage des cases libres à droite ou en bas
		x = case[0]
		y = case[1]
		while self.test_case((x+direction[0], y+direction[1])) :
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
#----------------------------------------------------------------------------------------------------------------
#
class Joueur:
	"""Classe pour définir le joueur"""
	def __init__(self, nom='Joueur'):
		"""Initialisation du joueur"""
		self.nom = nom
		self.grille_joueur = GrilleJoueur()
		self.grille_adverse = GrilleJoueur()
		self.grille_suivi = GrilleSuivi()
		self.coups_joues = []
		self.essais = 0

		# Liste des messages à afficher pendant la résolution
		self.messages = []
		
	def affiche_messages(self, affiche=True):
		"""Affiche la liste des messages"""
		if affiche :
			while self.messages :
				print("<%s> %s "%(self.nom, self.messages.pop(0)))
		
	def tire(self, case):
		"""Tire sur la case (x,y)
		Renvoie un tuple (booléen, string)
		où booléen = True si la case est touchée, False si non touché ou case invalide
		et la string est un message à afficher"""
		
		# Coup invalide
		if case in self.coups_joues :
			return (False, "%s : Déjà joué" % alpha(case))
		if not self.grille_suivi.test_case(case) :
			return (False, "%s : Coup invalide" % alpha(case))
			
		# Coup valide
		if self.grille_adverse.is_touche(case) :
			resultat = (True, "%s : Touché" % alpha(case))
			self.grille_suivi.etat[case] = 1
		else :
			resultat = (False, "%s : Manqué" % alpha(case))
			self.grille_suivi.etat[case] = -1
			
		# Mise à jour des paramètres du joueur et de la grille
		self.grille_suivi.update_vides()
		self.coups_joues.append(case)
		self.essais += 1
		
		return resultat


class Ordi(Joueur):
	def __init__(self, nom='HAL'):
		# Initialisation de la classe Joueur
		Joueur.__init__(self, nom)
		
		# File d'attente
		self.queue = []
		# Liste des case touchées sur un bateau
		self.liste_touches = []
		# Case courante
		self.case_courante = None
		# Première case touchée sur un bateau
		self.case_touchee = None
		
		# Liste des cases que l'ordi va jouer
		# Le but est de remplir cette liste dès le début de la partie et de la vider au fur et à mesure
		self.cases_jouees = [] 
	
	#
	# Affichages -------------------------------------------------------
	#
	def affiche_suivi(self):
		"""Affiche la grille de suivi des coups"""
		self.grille_suivi.affiche()
	
	def affiche_bateaux(self):
		"""Affiche la liste des bateaux restant à couler"""
		self.messages.append("Bateaux restant à couler : %s"%' '.join([str(t) for t in self.grille_suivi.taille_bateaux]))
	
	def affiche_queue(self):
		"""Affiche le contenu de la file d'attente"""
		if self.queue :
			self.messages.append("File d'attente : %s"%' '.join([alpha(case) for case in self.queue])) 
	
	#
	# Tire aléatoire ---------------------------------------------------
	#
	def make_case_aleatoire(self):
		"""Choisi une case aléatoire"""
		self.case_courante = rand.choice([(i,j) for (i,j) in self.grille_suivi.vides if (i+j)%2==0])
		self.messages.append("Je tire au hasard sur la case %s"%alpha(self.case_courante))
	
	#
	# Tire sur une case ------------------------------------------------
	#
	def tire_case(self):
		"""Tire sur la case courante"""
		(resultat, message) = self.tire(self.case_courante)
		self.messages.append(message)
		return resultat
	
	#
	# Gestion de la file d'attente -------------------------------------
	#	
	def add_queue(self, case):
		"""Ajoute la case à la file d'attente"""
		self.messages.append("J'ajoute la case %s à la file d'attente"%alpha(case))
		self.queue.append(case)
	
	def rem_queue(self, case):
		if case in self.queue :
			self.queue.remove(case)
			self.messages.append("J'enlève la case %s de la file d'attente" % alpha(case))
			
	def add_adjacentes_premiere(self):
		"""Ajoute les cases adjacentes possibles à la premiere case touchée dans la queue"""
		# Récupération des cases adjacentes en fonction de la taille du plus petit bateau restant
		adj = self.grille_suivi.adjacent(self.case_touchee)
		self.grille_suivi.get_taille_min()
		
		# On teste si le bateau rentre horizontalement
		if self.grille_suivi.get_max_space(self.case_touchee, direction=BN_HORIZONTAL) >= self.grille_suivi.taille_min :
			for c in adj :
				if c[1] == self.case_touchee[1] :
					self.add_queue(c)
		else :
			self.messages.append("Le plus petit bateau, de taille %d, ne rentre pas horizontalement en case %s"%(self.grille_suivi.taille_min, alpha(self.case_touchee)))
		
		# On teste si le bateau rentre verticalement
		if self.grille_suivi.get_max_space(self.case_touchee, direction=BN_VERTICAL) >= self.grille_suivi.taille_min :
			for c in adj :
				if c[0] == self.case_touchee[0] :
					self.add_queue(c)
		else :
			self.messages.append("Le plus petit bateau, de taille %d, ne rentre pas verticalement en case %s"%(self.grille_suivi.taille_min, alpha(self.case_touchee)))
					
		# On mélange la file d'attente pour ne pas que l'algo soit prévisible
		self.shuffle_queue()
		
		self.affiche_queue()
	
	def update_queue_touche(self):
		"""Met à jour la file d'attente en enlevant le cases qui ne sont pas dans la bonne direction après avoir touché une 2ème fois"""
		# Bateau horizontal :
		if self.case_courante[1] == self.case_touchee[1] :
			direction = BN_HORIZONTAL
		# Bateau vertical :
		else :
			direction = BN_VERTICAL
		
		# Si on vient de découvrir la direction, on l'affiche et on enlève de la queue les cases qui ne sont pas dans la bonne direction
		if len(self.liste_touches)==1 :
			if direction == BN_HORIZONTAL :
				self.messages.append("Le bateau touché est horizontal")
			else :
				self.messages.append("Le bateau touché est vertical")
			# On enlève de la queue les cases qui ne sont pas dans la bonne direction
			self.rem_queue((self.case_touchee[0]-direction[1], self.case_touchee[1]-direction[0]))
			self.rem_queue((self.case_touchee[0]+direction[1], self.case_touchee[1]+direction[0]))
			
		# Case adjacente à la nouvelle case touchée
		# signe(case_courante[0]-case_touchee[0]) permet de savoir de quel côté est la case adjacente
		nv_case = (self.case_courante[0] + direction[0]*signe(self.case_courante[0]-self.case_touchee[0]) , self.case_courante[1] + direction[1]*signe(self.case_courante[1]-self.case_touchee[1]))
		if self.grille_suivi.test_case(nv_case) :
			self.add_queue(nv_case)
		
		self.affiche_queue()
		
		# Mise à jour de la liste des cases touchées sur ce bateau
		self.liste_touches.append(self.case_courante)
	
	def update_queue_manque(self) :
		"""Met à jour la file d'attente en éliminant une direction impossible, après avoir manqué la case en face"""
		# Écart entre la case touchee initiale et la case jouée
		delta = (self.case_courante[0]-self.case_touchee[0], self.case_courante[1]-self.case_touchee[1])
		# Direction dans laquelle on vient de jouer
		direction = (abs(self.case_courante[0]-self.case_touchee[0]), abs(self.case_courante[1]-self.case_touchee[1]))
		# Case en face de la case jouée
		case_face = (self.case_touchee[0]-delta[0], self.case_touchee[1]-delta[1])
		
		# On regarde s'il y a assez de place dans cette direction pour le plus petit bateau
		if self.grille_suivi.get_max_space(case_face, direction) < self.grille_suivi.taille_min-1 :
			if direction == BN_HORIZONTAL :
				self.messages.append("Après ce coup, le plus petit bateau, de taille %d, ne rentre pas horizontalement en case %s" % (self.grille_suivi.taille_min, alpha(self.case_courante)))
			else :
				self.messages.append("Après ce coup, le plus petit bateau, de taille %d, ne rentre pas verticalement en case %s" % (self.grille_suivi.taille_min, alpha(self.case_courante)))
			self.rem_queue(case_face)
	
	def pop_queue(self):
		"""Récupère, en l'enlevant, le premier élément de la queue"""
		self.case_courante = self.queue.pop(0)
		self.messages.append("Je tire sur la case %s de la file d'attente" % alpha(self.case_courante))
	
	def shuffle_queue(self):
		"""Mélange les cases de la file d'attente"""
		rand.shuffle(self.queue)
		self.messages.append("Je mélange ma file d'attente")
		
	def vide_queue(self):
		"""Vide la file d'attente"""
		self.messages.append("Je vide ma file d'attente")
		self.queue = []
	
	def test_plus_grand(self):
		"""Renvoie True si on a touché autant de cases que le plus grand bateau"""
		if len(self.liste_touches) == self.grille_suivi.taille_max :
			self.messages.append("Bateau de taille %d coulé car c'est le plus grand restant" % self.grille_suivi.taille_max)
			return True
		else :
			return False
			
	#
	# Gestion de la grille ---------------------------------------------
	#
	def rem_bateau(self):
		"""Enlève le dernier bateau coulé"""
		self.grille_suivi.rem_bateau(len(self.liste_touches))
		self.messages.append("Bateau coulé, je l'enlève de la liste des bateaux à chercher")
		self.affiche_bateaux()
	
	def elimine_adjacentes(self):
		"""Élimine les cases adjacents à un bateau coulé"""
		for case_touchee in self.liste_touches :
			for case_impossible in self.grille_suivi.adjacent(case_touchee):
				if self.grille_suivi.test_case(case_impossible) :
					self.grille_suivi.etat[case_impossible] = -1
					self.messages.append("J'élimine la case adjacente %s" % alpha(case_impossible))
		self.grille_suivi.update()
	
	def elimine_petites(self):
		"""Élimine les cases dans lesquelles le plus petit bateau ne peut pas rentrer"""
		cases_eliminees = self.grille_suivi.elimine_cases()
		for c in cases_eliminees :
			self.messages.append("J'élimine la cases %s : zone trop petite pour le plus petit bateau de taille %d" % (alpha(c), self.grille_suivi.taille_min))
	
	#
	# Résolution de la grille ------------------------------------------
	#
	def joue(self, affiche=True):
		"""Lance la partie de l'ordinateur"""
		# affiche : affichage ou non des informations
		
		# Lancement du chrono
		start = time()
		
		# C'est parti !!!
		while not self.grille_suivi.fini():
			if affiche :
				clear()
				self.grille_suivi.affiche()
			
			self.affiche_messages(affiche=affiche)
				
			# Si la file d'attente est vide : soit on a tiré dans le vide au hasard, soit on vient de couler un bateau
			if not self.queue :
				# Si on vient de couler un bateau
				if self.liste_touches :
					# On l'enlève de la liste des bateaux à couler
					self.rem_bateau()
					# Mise à jour des cases adjacentes au bateau coulé (cases impossibles)
					self.elimine_adjacentes()
					
				# Élimination des cases dans lesquelles le plus petit bateau restant ne peut pas rentrer
				self.elimine_petites()
				# Réinitialisation des cases touchées
				self.liste_touches = []
				
				# Choisit sur une case aléatoire 
				self.make_case_aleatoire()
			
			# Si la file d'attente n'est pas vide, on choisit sa 1ère case qu'on enlève de la file d'attente
			else :
				self.pop_queue()
			
			# Tire sur la case choisie
			self.cases_jouees.append(self.case_courante)
			resultat = self.tire_case()

			# Si on touche
			if resultat :
				# Si c'est la 1ère case du bateau, on remplit la file d'attente avec ses 4 cases adjacentes possibles
				if not self.liste_touches :
					self.liste_touches = [self.case_courante]
					self.case_touchee = self.case_courante # 1ère case touchée du bateau
					
					# On ajoute les case adjacentes possibles à la case, en ordre aléatoire :
					self.add_adjacentes_premiere()
					
				# Sinon on détermine le sens du bateau et on met à jour la queue avec ses cases adjacentes
				# en enlevant celles qui ne sont pas dans la bonne direction
				else :
					self.update_queue_touche()

				# Si la taille du bateau qu'on est entrain de couler est la taille max des bateaux sur la grille, on arrête
				if self.test_plus_grand():
					self.vide_queue()
					
			# Si on manque
			else :
				if len(self.liste_touches) == 1:
					# Si on n'a touché qu'une case et qu'on vient de manquer, on vient donc de tirer sur une de ses cases adjacentes
					# On élimine alors la case dans la direction dans laquelle le plus petit bateau ne rentre pas (si c'est le cas)
					self.update_queue_manque()
			
			if affiche :
				input("Entrée pour continuer")
			
		# Fin de la partie
		if affiche :
			clear()
			self.grille_suivi.affiche()
			
		self.messages.append("Partie terminée en %d coups"%self.essais)
		self.affiche_messages(affiche=affiche)
		
		if affiche :
			info("Grille de l'adversaire :")
			self.grille_adverse.affiche()
			info("Coups joués : ", ' '.join([alpha(case) for case in self.cases_jouees]))
		
		# On renvoie de temps de résolution de la grille pour les tests de performance
		return time()-start
				

#
#----------------------------------------------------------------------------------------------------------------
#
if __name__== '__main__':
	"""Programme principal"""

#
#----------------------------------------------------------------------------------------------------------------
#

	def jeu_ordi(affiche = True) :
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		ordi = Ordi()
		ordi.grille_adverse = grille
		temps = ordi.joue(affiche = affiche)
		return (ordi.essais, temps) # Pour les tests de performance

#
#----------------------------------------------------------------------------------------------------------------
#

	def jeu_solo() :
		"""Jeu solo sur une grille aléatoire"""
		# Initialisation de la partie
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		joueur = Joueur()
		joueur.grille_adverse = grille
		message = "Début de partie"
		
		# Début de partie
		while not joueur.grille_suivi.fini():
			clear()
			joueur.grille_suivi.affiche()
			print(message)
			case = input('Coups (Entrée pour un coup aléatoire) : ')
			if case == '' :
				message = joueur.tire((rand.randint(0,joueur.grille_adverse.xmax-1), rand.randint(0,joueur.grille_adverse.ymax-1)))[1]
			else :
				try :
					message = joueur.tire((ord(case[0])-65, int(case[1])))[1]
				except :
					message = "%s : Coup invalide" % case

		# Fin de partie
		clear()
		joueur.grille_suivi.affiche()
		print("Bravo !! Partie terminée en %d coups" % joueur.essais)
#
#----------------------------------------------------------------------------------------------------------------
#




# Menu de lancement 
	print("""Choix du jeu :
  S : Solo
  O : Ordi 
  T : Test algo""")
	choix = input("--> [O|s|t] ")
	if choix.lower() == 's' :
		jeu_solo()
	elif choix.lower() == 't' :
		n = int(input("Nombre de répétitions : "))
		temps = 0
		s = 0
		for k in range(n) :
			(e,t) = jeu_ordi(affiche=False)
			s += e
			temps += t
		print("Moyenne : %.2f"%(s/n))
		print("Temps moyen : %.5f secondes"%(temps/n))
	else :
		jeu_ordi()



