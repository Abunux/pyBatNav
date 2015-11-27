# Version 0.1.0

import random as rand
from time import time

from bn_grille import *

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
