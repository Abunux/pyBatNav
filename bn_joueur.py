"""Module bn_joueurs

Implémente les classes :
	- Joueur : la classe de base des joueurs
	- Ordinateur : dérivée de Joueur, 
		pour résoudre une grille automatiquement
	- Partie : déroulement d'une partie
 
Auteurs : Frédéric Muller et Lionel Reboul

Licence CC BY-NC-SA

Version 0.1.0"""


from time import time

from bn_grille import *
from bn_utiles import *

#
#----------------------------------------------------------------------------------------------------------------
#
class Joueur(object):
	"""Classe pour définir le joueur"""
	def __init__(self, nom='Joueur'):
		"""Initialisation du joueur"""
		# Nom du joueur
		self.nom = nom
		
		# Grilles de jeu
		self.grille_joueur = GrilleJoueur()
		self.grille_adverse = GrilleJoueur()
		self.grille_suivi = GrilleSuivi()
		
		# Liste des cases jouées
		self.cases_jouees = []
		
		# Nombre d'essais
		self.essais = 0

		# Liste des messages à afficher pendant la résolution
		self.messages = []
		
	def affiche_messages(self, affiche=True):
		"""Affiche la liste des messages"""
		# Méthode à surcharger suivant l'interface
		if affiche :
			while self.messages :
				info("<%s> %s "%(self.nom, self.messages.pop(0)))
	
	def add_bateau(self, taille, start, direction):
		"""Ajoute un bateau sur la grille du joueur"""
		bateau = Bateau(taille, start, direction)
		if self.grille_joueur.test_bateau(bateau):
			self.grille_joueur.add_bateau(bateau)
			return True
		else :
			return False
			
	def tire(self, case):
		"""Tire sur la case (x,y)
		Renvoie True si la case est touchée, 
		False si non touché ou case invalide"""
		# Coup invalide
		if case in self.cases_jouees :
			self.messages.append("%s : Déjà joué" % alpha(case))
			return False
		if not self.grille_suivi.test_case(case):
			self.messages.append("%s : Coup invalide" % alpha(case))
			return False
			
		# Coup valide
		if self.grille_adverse.is_touche(case):
			self.messages.append("%s : Touché" % alpha(case))
			resultat = True
			self.grille_suivi.etat[case] = 1
		else :
			self.messages.append("%s : Manqué" % alpha(case))
			resultat = False
			self.grille_suivi.etat[case] = -1
			
		# Mise à jour des paramètres du joueur et de la grille
		self.grille_suivi.update_vides()
		self.cases_jouees.append(case)
		self.essais += 1
		return resultat
	
	def case_aleatoire(self):
		"""Retourne une case aléatoire parmi les cases vides"""
		#~ return self.grille_suivi.case_max()[0]
		liste_cases = [(i,j) for (i,j) in self.grille_suivi.vides if (i+j)%2==0]
		if liste_cases :
			return rand.choice(liste_cases)
		else :
			return rand.choice(self.grille_suivi.vides)
	
	def tire_aleatoire(self):
		"""Tire sur une case aléatoire"""
		self.tire(self.case_aleatoire())
		
	def joue_coup(self):
		"""Joue un coup"""
		# Méthode à surcharger suivant l'interface 
		pass
	
	#
	# Partie solo sur une grille aléatoire -----------------------------
	#
	def jeu_solo(self):
		"""Lance une partie solo sur une grille aléatoire"""
		# Méthode à surcharger suivant l'interface
		pass
		
#
#----------------------------------------------------------------------------------------------------------------
#
class Ordi(Joueur):
	"""Algorithme de résolution"""
	def __init__(self, nom='HAL', level=5):
		# Initialisation de la classe Joueur
		Joueur.__init__(self, nom)
		
		# Niveau de l'ordinateur (type d'algo de résolution) :
		# --> À implémenter dans la suite
		# level=1 : Tous les coups aléatoires
		# level=2 : Aveugle aléatoire, ciblé 
		# level=3 : Aveugle aléatoire cases noires, ciblé
		# level=4 : Aveugle échantillons, ciblé
		# level=5 : Aveugle nb possibilités, ciblé 
		self.level = level
		
		# Initialisation de sa grille
		self.grille_joueur.init_bateaux_alea()
		
		# Variables pour la résolution :
		# ------------------------------
		# File d'attente
		self.queue = []
		# Liste des case touchées sur un bateau
		self.liste_touches = []
		# Case courante
		self.case_courante = None
		# Première case touchée sur un bateau
		self.case_touchee = None
	
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
		"""Choisit une case aléatoire (suivant l'algorithme choisit)"""
		if self.level==1 or self.level==2 :
			self.case_courante = rand.choice(self.grille_suivi.vides)
			self.messages.append("Je tire au hasard sur la case %s" % (alpha(self.case_courante)))
		elif self.level==3 :
			self.case_courante = rand.choice([(i,j) for (i,j) in self.grille_suivi.vides if (i+j)%2==0])
			self.messages.append("Je tire au hasard sur la case %s" % (alpha(self.case_courante)))
		elif self.level==4 :
			(case_max, pmax) = self.grille_suivi.case_max_echantillons()
			self.case_courante = case_max
			self.messages.append("Je tire sur la case %s qui est la plus probable (p=%.4f)" % (alpha(self.case_courante), pmax))
		else :
			(case_max, pmax) = self.grille_suivi.case_max()
			self.case_courante = case_max
			self.messages.append("Je tire sur la case %s qui est la plus probable (%d bateaux possibles)" % (alpha(self.case_courante), pmax))
	
	#
	# Tire sur une case ------------------------------------------------
	#
	def tire_case_courante(self):
		"""Tire sur la case courante"""
		return self.tire(self.case_courante)
	
	#
	# Gestion de la file d'attente -------------------------------------
	#
	def add_queue(self, case):
		"""Ajoute la case à la file d'attente"""
		self.messages.append("J'ajoute la case %s à la file d'attente" % alpha(case))
		self.queue.append(case)
	
	def rem_queue(self, case):
		"""Enlève la case de la file d'attente"""
		if case in self.queue :
			self.queue.remove(case)
			self.messages.append("J'enlève la case %s de la file d'attente" % alpha(case))
			
	def add_adjacentes_premiere(self):
		"""Ajoute les cases adjacentes possibles à 
		la premiere case touchée dans la  file d'attente"""
		# Récupération des cases adjacentes en fonction de la taille du plus petit bateau restant
		adj = self.grille_suivi.adjacent(self.case_touchee)
		self.grille_suivi.get_taille_min()
		
		# On teste si le bateau rentre horizontalement
		if self.grille_suivi.get_max_space(self.case_touchee, direction=BN_HORIZONTAL) >= self.grille_suivi.taille_min :
			for c in adj :
				if c[1] == self.case_touchee[1] :
					self.add_queue(c)
		else :
			self.messages.append("Le plus petit bateau, de taille %d, ne rentre pas horizontalement en case %s" % (self.grille_suivi.taille_min, alpha(self.case_touchee)))
		
		# On teste si le bateau rentre verticalement
		if self.grille_suivi.get_max_space(self.case_touchee, direction=BN_VERTICAL) >= self.grille_suivi.taille_min :
			for c in adj :
				if c[0] == self.case_touchee[0] :
					self.add_queue(c)
		else :
			self.messages.append("Le plus petit bateau, de taille %d, ne rentre pas verticalement en case %s" % (self.grille_suivi.taille_min, alpha(self.case_touchee)))
					
		# On mélange la file d'attente en fonction des probas
		self.shuffle_queue()
		
		self.affiche_queue()
	
	def update_queue_touche(self):
		"""Met à jour la file d'attente en enlevant les cases 
		qui ne sont pas dans la bonne direction après avoir
		touché une 2ème fois"""
		# Bateau horizontal :
		if self.case_courante[1] == self.case_touchee[1] :
			direction = BN_HORIZONTAL
		# Bateau vertical :
		else :
			direction = BN_VERTICAL
		
		# Si on vient de découvrir la direction, on l'affiche et on enlève de la file d'attente les cases qui ne sont pas dans la bonne direction
		if len(self.liste_touches)==1 :
			if direction == BN_HORIZONTAL :
				self.messages.append("Le bateau touché est horizontal")
			else :
				self.messages.append("Le bateau touché est vertical")
			# On enlève de la file d'attente les cases qui ne sont pas dans la bonne direction
			self.rem_queue((self.case_touchee[0]-direction[1], self.case_touchee[1]-direction[0]))
			self.rem_queue((self.case_touchee[0]+direction[1], self.case_touchee[1]+direction[0]))
			
		# Case adjacente à la nouvelle case touchée
		# signe(self.case_courante[k]-self.case_touchee[k]) permet de savoir de quel côté est la case adjacente (k=0 ou k=1)
		nv_case = (self.case_courante[0] + direction[0]*signe(self.case_courante[0]-self.case_touchee[0]) , self.case_courante[1] + direction[1]*signe(self.case_courante[1]-self.case_touchee[1]))
		if self.grille_suivi.test_case(nv_case):
			self.add_queue(nv_case)
		
		self.affiche_queue()
		
		# Mise à jour de la liste des cases touchées sur ce bateau
		self.liste_touches.append(self.case_courante)
	
	def update_queue_manque(self):
		"""Met à jour la file d'attente en éliminant une direction
		impossible, après avoir manqué la case en face"""
		# Écart entre la case touchee initiale et la case jouée
		delta = (self.case_courante[0]-self.case_touchee[0], self.case_courante[1]-self.case_touchee[1])
		# Direction dans laquelle on vient de jouer
		direction = (abs(self.case_courante[0]-self.case_touchee[0]), abs(self.case_courante[1]-self.case_touchee[1]))
		# Case en face de la case jouée
		case_face = (self.case_touchee[0]-delta[0], self.case_touchee[1]-delta[1])
		
		# On regarde s'il y a assez de place dans cette direction pour le plus petit bateau
		if self.grille_suivi.get_max_space(case_face, direction) < self.grille_suivi.taille_min-1 :
			if direction == BN_HORIZONTAL :
				self.messages.append("Après ce coup, le plus petit bateau, de taille %d, ne rentre pas horizontalement en case %s" % (self.grille_suivi.taille_min, alpha(self.case_touchee)))
			else :
				self.messages.append("Après ce coup, le plus petit bateau, de taille %d, ne rentre pas verticalement en case %s" % (self.grille_suivi.taille_min, alpha(self.case_touchee)))
			self.rem_queue(case_face)
	
	def pop_queue(self):
		"""Récupère, en l'enlevant, le premier élément de la queue"""
		self.case_courante = self.queue.pop(0)
		self.messages.append("Je tire sur la case %s de la file d'attente" % alpha(self.case_courante))
	
	def shuffle_queue(self):
		"""Mélange les cases de la file d'attente en les triant
		par ordre décroissant des bateaux possibles"""
		if len(self.queue)>1 :
			rand.shuffle(self.queue)
			self.messages.append("J'ordonne ma file d'attente en fonction des possibilités :")
			probas = self.grille_suivi.case_max_touchee(self.case_touchee)
			queue_tmp = []
			for p in probas :
				if p[0] in self.queue :
					queue_tmp.append(p[0])
					self.messages.append("%s : %d bateaux possibles" %(alpha(p[0]), p[1]))
			self.queue = queue_tmp[:]
		
	def vide_queue(self):
		"""Vide la file d'attente"""
		self.queue = []
		self.messages.append("Je vide ma file d'attente")
		
	
	def test_plus_grand(self):
		"""Renvoie True si on a touché autant de cases que 
		le plus grand bateau restant"""
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
		self.messages.append("Bateau de taille %d coulé ! Je l'enlève de la liste des bateaux à chercher" % len(self.liste_touches))
		self.affiche_bateaux()
	
	def elimine_adjacentes(self):
		"""Élimine les cases adjacents à un bateau coulé"""
		for case_touchee in self.liste_touches :
			for case_impossible in self.grille_suivi.adjacent(case_touchee):
				if self.grille_suivi.test_case(case_impossible):
					self.grille_suivi.etat[case_impossible] = -1
					self.messages.append("J'élimine la case adjacente %s" % alpha(case_impossible))
		self.grille_suivi.update()
	
	def elimine_petites(self):
		"""Élimine les cases dans lesquelles le plus petit bateau 
		ne peut pas rentrer"""
		cases_eliminees = self.grille_suivi.elimine_cases()
		for c in cases_eliminees :
			self.messages.append("J'élimine la cases %s : zone trop petite pour le plus petit bateau de taille %d" % (alpha(c), self.grille_suivi.taille_min))
	
	#
	# Résolution de la grille ------------------------------------------
	#
	def coup_suivant(self):
		"""Fait jouer à l'ordinateur le coup suivant"""
		# Si la file d'attente est vide : soit on a tiré dans le vide au hasard, soit on vient de couler un bateau
		if not self.queue or self.level == 1 :
			# Si on vient de couler un bateau
			if self.liste_touches :
				# On l'enlève de la liste des bateaux à couler
				self.rem_bateau()
				# Mise à jour des cases adjacentes au bateau coulé (cases impossibles)
				self.elimine_adjacentes()
				# Réinitialisation des cases touchées
				self.liste_touches = []
				
			# Élimination des cases dans lesquelles le plus petit bateau restant ne peut pas rentrer
			if self.level != 1 :
				self.elimine_petites()
			
			# Choisit sur une case aléatoire 
			self.make_case_aleatoire()
		
		# Si la file d'attente n'est pas vide, on choisit sa 1ère case qu'on enlève de la file d'attente
		else :
			self.pop_queue()
		
		# Tire sur la case choisie
		resultat = self.tire_case_courante()
		
		if self.level != 1 :
			# Si on touche
			if resultat :
				# Si c'est la 1ère case du bateau, on remplit la file d'attente avec ses 4 cases adjacentes possibles
				if not self.liste_touches :
					self.liste_touches = [self.case_courante]
					self.case_touchee = self.case_courante # 1ère case touchée du bateau
					
					# On ajoute les case adjacentes possibles à la case, en ordre aléatoire
					self.add_adjacentes_premiere()
					
				# Sinon on détermine le sens du bateau et on met à jour la file d'attente avec ses cases adjacentes
				# et on enlève celles qui ne sont pas dans la bonne direction
				else :
					self.update_queue_touche()

				# Si la taille du bateau qu'on est entrain de couler est la taille max des bateaux sur la grille, on arrête
				if self.test_plus_grand():
					self.vide_queue()
					
			# Si on manque
			else :
				if len(self.liste_touches) == 1 :
					# Si on n'a touché qu'une case et qu'on vient de manquer (on vient donc de tirer sur une de ses cases adjacentes)
					# On élimine alors la case dans la direction dans laquelle le plus petit bateau ne rentre pas (si c'est le cas)
					self.update_queue_manque()
	
	def resolution(self):
		"""Lance la résolution de la grille par l'ordinateur"""
		
		# Méthode à surcharger suivant l'interface
		
		# Lancement du chrono
		start = time()
		
		# C'est parti !!!
		while not self.grille_suivi.fini():
			self.coup_suivant()
			
		# Fin de la partie
		self.messages.append("Partie terminée en %d coups" % self.essais)
				
		# On renvoie de temps de résolution de la grille pour les tests de performance
		return time()-start

#
#----------------------------------------------------------------------------------------------------------------
#
class Partie(object):
	"""Gère le déroulement de la partie"""
	def __init__(self, joueur=Joueur(), adversaire=Ordi()):
		# Création des joueurs
		self.joueur = joueur
		self.adversaire = adversaire
		# Test si le joueur 2 est l'ordi
		self.ordi = isinstance(self.adversaire, Ordi) 
		
		# Lance la partie
		self.lance_partie()
		
	#
	# Gestion des bateaux du joueur ------------------------------------
	#
	def add_bateau_joueur(self, taille):
		"""Ajoute un bateau pour le joueur"""
		# Méthode à surcharger suivant l'interface
		pass
		
	def place_bateaux_joueur(self):
		"""Place tous les bateaux du joueur"""
		for taille in self.joueur.grille_joueur.taille_bateaux :
			while not self.add_bateau_joueur(taille):
				info("Le bateau de taille %d ne convient pas" % taille)

	
	#
	# Gestion de l'adversaire ------------------------------------------
	#
	def get_bateaux_adverse(self):
		"""Récupère la liste des bateaux adverses"""
		self.adversaire.grille_joueur = GrilleJoueur()
		if self.ordi :
			self.adversaire.grille_joueur.init_bateaux_alea()
		else :
			info("Récupération des bateaux de l'adversaire via le réseau à implémenter")
		self.joueur.grille_adverse = self.adversaire.grille_joueur
		
	def get_coup_adverse(self):
		"""Récupère le coup de l'adversaire"""
		if self.ordi :
			self.adversaire.coup_suivant()
		else :
			info("Récupération du coup de l'adversaire via le réseau à implémenter")
	
	#
	# Lancement de la partie -------------------------------------------
	#
	def lance_partie(self):
		"""Lance une partie à deux joueurs"""
		# Méthode à surcharger suivant l'interface
		pass

