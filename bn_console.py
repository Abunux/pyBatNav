import os
import matplotlib.pyplot as plt
import numpy as np

from bn_grille import *
from bn_joueur import *

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


# Caractères graphqiues (pour faire la grille)
# --------------------------------------------
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

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleC(Grille) :
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2])
	
	#
	# Affichage en console ---------------------------------------------
	#
	def affiche(self):
		"""Affiche la grille avec des caractère graphiques"""
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
			for i in range(self.xmax):
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

class GrilleJoueurC(GrilleC, GrilleJoueur):
	"""La grille sur laquelle chaque joueur place ses bateaux"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuiviC(GrilleC, GrilleSuivi):
	"""La grille de suivi des coups joués"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class JoueurC(Joueur):
	def __init__(self, nom='Joueur'):
		Joueur.__init__(self, nom)
		self.grille_joueur = GrilleJoueurC()
		self.grille_adverse = GrilleJoueurC()
		self.grille_suivi = GrilleSuiviC()
	
	def joue_coup(self):
		"""Joue un coup sur une case"""
		case = input('Coups (Entrée pour un coup aléatoire): ')
		if case == '' :
			self.tire_aleatoire()
		else :
			try :
				self.tire(coord(case))
			except :
				self.messages.append("%s : Coup invalide" % case)
				self.joue_coup()
		#~ self.affiche_messages()
	
	#
	# Partie solo sur une grille aléatoire -----------------------------
	#
	def jeu_solo(self):
		"""Lance une partie solo sur une grille aléatoire"""
		self.messages.append("Début de partie")
		# Début de la partie
		while not self.grille_suivi.fini():
			# Affichages
			clear()
			self.grille_suivi.affiche()
			self.affiche_messages()
			
			# Joue un coup
			self.joue_coup()
			
		# Fin de partie
		clear()
		self.grille_suivi.affiche()
		self.messages.append("Bravo !! Partie terminée en %d coups" % self.essais)
		self.affiche_messages()
		info("Grille de l'adversaire :")
		self.grille_adverse.affiche()
		info("Coups joués : ", ' '.join([alpha(case) for case in self.cases_jouees]))
#
#----------------------------------------------------------------------------------------------------------------
#
class OrdiC(JoueurC, Ordi):
	def __init__(self, nom='HAL'):
		Ordi.__init__(self, nom)
		JoueurC.__init__(self, nom)
		
	
	def resolution(self, affiche=True):
		"""Lance la résolution de la grille par l'ordinateur"""
		# affiche : affichage ou non des informations
		
		# Lancement du chrono
		start = time()
		
		# C'est parti !!!
		while not self.grille_suivi.fini():
			if affiche :
				clear()
				self.grille_suivi.affiche()
			
			self.affiche_messages(affiche=affiche)
			
			self.coup_suivant()
			
			if affiche :
				input("Entrée pour continuer")
			
		# Fin de la partie
		if affiche :
			clear()
			self.grille_suivi.affiche()
			
		self.messages.append("Partie terminée en %d coups" % self.essais)
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
class PartieC(Partie):
	"""En cours de construction..."""
	def __init__(self, joueur=Joueur(), adversaire=Ordi()):
		Partie.__init__(self, joueur, adversaire)
		
	#
	# Gestion des bateaux du joueur ------------------------------------
	#
	def add_bateau_joueur(self, taille):
		"""Ajoute un bateau pour le joueur"""
		info("Placement du bateau de taille %d" % taille)
		case = input("Case de départ (entrée pour un bateau aléatoire) : ")
		try :
			case = coord(case)
		except :
			if case == "" :
				self.joueur.grille_joueur.add_bateau_alea(taille)
				return True
			info("Saisie invalide")
			info()
			return False
		info("Direction :")
		info("H : Haut")
		info("B : Bas")
		info("D : Droite")
		info("G : Gauche")
		d = input("Direction : ")
		if d.upper() == 'H' :
			direction = BN_HAUT
		elif d.upper() == 'B' :
			direction = BN_BAS
		elif d.upper() == 'D' :
			direction = BN_DROITE
		elif d.upper() == 'G' :
			direction = BN_GAUCHE
		try :
			bateau = Bateau(taille, case, direction)
		except :
			info("Saisie invalide")
			info()
			return False
		return self.joueur.add_bateau(taille, case, direction)
		
	def place_bateaux_joueur(self):
		"""Place tous les bateaux du joueur"""
		for taille in self.joueur.grille_joueur.taille_bateaux :
			clear()
			self.joueur.grille_joueur.affiche()
			while not self.add_bateau_joueur(taille):
				print("Le bateau de taille %d ne convient pas" % taille)
				print()
	
	#
	# Lancement de la partie -------------------------------------------
	#
	def lance_partie(self):
		"""Partie à deux joueurs"""
		self.place_bateaux_joueur()
		self.get_bateaux_adverse()
		self.adversaire.grille_adverse = self.joueur.grille_joueur
		
		clear()
		print("Votre grille de jeu :")
		print()
		self.joueur.grille_joueur.affiche()
		print()
		input("Entrée pour commencer la partie")
		
		while not self.joueur.grille_suivi.fini() and not self.adversaire.grille_suivi.fini() :
			clear()
			print("Votre grille de suivi :")
			print()
			self.joueur.grille_suivi.affiche()
			self.joueur.joue_coup()
			clear()
			print()
			print()
			self.joueur.grille_suivi.affiche()
			self.joueur.affiche_messages()
			print()

			if not self.adversaire.grille_suivi.fini() :
				input("Entrée pour le coup suivant")
				clear()
				self.get_coup_adverse()
				print("Grille de suivi l'adversaire : ")
				print()
				self.adversaire.grille_suivi.affiche()
				self.adversaire.affiche_messages()
				print()
				input("Entrée pour le coup suivant")
				
		if self.joueur.grille_suivi.fini():
			print("Vous avez gagné en %d coups" % self.joueur.essais)
		else :
			print("L'adversaire a gagné en %d coups" % self.adversaire.essais)


#
#----------------------------------------------------------------------------------------------------------------
#

class main_console(object):
	"""Programme principal en mode console"""
	def __init__(self):
		self.launch_menu()

	def jeu_ordi(self, affiche=True):
		"""Résolution d'une grille par l'ordinateur"""
		# Initialisation de la partie
		grille = GrilleJoueurC()
		grille.init_bateaux_alea()
		ordi = OrdiC()
		ordi.grille_adverse = grille
		
		temps = ordi.resolution(affiche=affiche)
		return (ordi.essais, temps) # Pour les tests de performance


	def jeu_solo(self):
		"""Jeu solo sur une grille aléatoire"""
		# Initialisation de la partie
		grille = GrilleJoueurC()
		grille.init_bateaux_alea()
		joueur = JoueurC()
		joueur.grille_adverse = grille
		joueur.jeu_solo()


	def jeu_contre_ordi(self):
		"""Partie en duel contre l'ordi"""
		joueur = JoueurC("Toto")
		ordi = OrdiC()
		partie = PartieC(joueur, ordi)


	def test_algo(self, n=1000):
		"""Test l'ago de l'ordinateur en faisant n parties"""
		# Lancement de la simulation
		temps_total = 0
		liste_essais = []
		for k in range(n):
			(essais,temps) = self.jeu_ordi(affiche=False)
			temps_total += temps
			liste_essais.append(essais)
		
		# Création de la liste de distribution de fréquences
		distrib = [0]*100
		for e in liste_essais :
				distrib[e] += 1
		for k in range(len(distrib)) :
			distrib[k] *= 1/n
		
		# Sauvegarde de cette liste dans un fichier texte
		stats_file = open("distrib_HAL_%d.txt" % n, "w")
		for k in range(len(distrib)) :
			stats_file.write(str(distrib[k])+'\n')
		stats_file.close()
		
		# Résultats de la simulation
		mini = min(liste_essais)
		maxi = max(liste_essais)
		moyenne = sum(liste_essais)/n
		
		print()
		print("Résultats de la simulation :")
		print()
		print("Nombre de coups moyen : %.2f coups" % moyenne)
		print("Nombre de coups minimum : %.2f coups" % mini)
		print("Nombre de coups maximum : %.2f coups" % maxi)
		print()
		print("Temps moyen par partie : %.5f secondes" % (temps_total/n))
		
		# Création de l'histogramme
		plt.hist(liste_essais, bins=np.arange(mini-0.5, maxi+1.5, 1), normed=1, facecolor='g', alpha=0.75)
		plt.xlabel("Nombre de coups")
		plt.ylabel("Fréquence de parties")
		plt.title("Résolution par l'ordinateur sur %d parties" % n)
		plt.grid(True)
		plt.show()
		
		return liste_essais
		
	def launch_menu(self):
		"""Menu de lancement """
		clear()
		# http://patorjk.com/software/taag/
		print("""
    ██████╗  █████╗ ████████╗ █████╗ ██╗██╗     ██╗     ███████╗
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║██║     ██║     ██╔════╝
    ██████╔╝███████║   ██║   ███████║██║██║     ██║     █████╗  
    ██╔══██╗██╔══██║   ██║   ██╔══██║██║██║     ██║     ██╔══╝  
    ██████╔╝██║  ██║   ██║   ██║  ██║██║███████╗███████╗███████╗
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

        ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ███████╗
        ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝
        ██╔██╗ ██║███████║██║   ██║███████║██║     █████╗  
        ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝  
        ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗███████╗
        ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝
                                                   

""")
		#~ print("| Bataille navalle |")
		#~ print("--------------------")
		print("(Il est conseillé de passer en mode plein écran)")
		print()
		print("""Choix du jeu :
--------------
  S : Solo
  O : Ordi 
  J : Jeu contre l'ordinateur
  T : Test algo
	  """)
		choix = input("--> [S|O|T|[J]] ")
		
		if choix.lower() == 's' :
			self.jeu_solo()
			
		elif choix.lower() == 't' :
			clear()
			n = int(input("Nombre de répétitions : "))
			self.test_algo(n)
			
		elif choix.lower() == 'o' :
			self.jeu_ordi()
			
		else :
			self.jeu_contre_ordi()


if __name__ == "__main__" :
	app = main_console()
