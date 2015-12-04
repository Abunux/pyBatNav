#!/usr/bin/python3
#
# Module bn_console
#
# Interface de jeu en mode console
#
# Auteurs : Frédéric Muller et Lionel Reboul
#
# Licence CC BY-NC-SA
#
# Version 0.1.0
#

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

def fusionne(chaine1, chaine2):
	"""Fusionne deux grilles pour l'affichage"""
	lignes1 = chaine1.split('\n')
	lignes2 = chaine2.split('\n')	
	chaine = ""
	for k in range(len(lignes1)-1):
		chaine += lignes1[k]+'  '+u'\u2503'+'  '+lignes2[k]+'\n'	
	return chaine

def centre(chaine, longueur):
	"""Centre la chaine sur la longueur"""
	c = len(chaine)
	l = longueur
	return ' '*((l-c)//2)+chaine+' '*((l-c)//2+(l-c)%2)+'\n'



# Caractères graphqiues (pour faire la grille)
# --------------------------------------------
# http://www.unicode.org/charts/ : Box Drawing (U2500.pdf)
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
		
		# Chaine de caractère pour affichage de la grille
		self.chaine = ""
		
	#
	# Affichage en console ---------------------------------------------
	#
	def make_chaine(self):
		"""Affiche la grille avec des caractères graphiques"""
		self.chaine = ""
		# Ligne du haut
		self.chaine += '    '+CAR_CHG+(CAR_H*3+CAR_TH)*(self.xmax-1)+CAR_H*3+CAR_CHD+'\n'
		
		# Ligne des lettres des colonnes
		self.chaine += '    '+CAR_V
		for i in range(self.xmax):
			if i!=self.xmax-1 :
				self.chaine += ' '+chr(i+65)+' '+CAR_V
				#~ chaine += ' '+str(i)+' '+CAR_V
			else :
				self.chaine += ' '+chr(i+65)+' '+CAR_V+'\n'
				#~ chaine += ' '+str(i)+' '+CAR_V+'\n'
				
		#Ligne sous les lettres
		self.chaine += CAR_CHG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD+'\n'
		
		# Lignes suivantes
		for j in range(self.ymax):
			# 1ère colonne (chiffres des lignes)
			chaine_tmp = CAR_V+' '+str(j)+' '+CAR_V
			
			# Cases suivantes
			for i in range(self.xmax):
				if self.etat[(i,j)] == 1 :
					symbole = CAR_TOUCH
				elif self.etat[(i,j)] == -1 :
					symbole = CAR_MANQ
				else :
					symbole = ' '
				chaine_tmp += ' '+symbole+' '+CAR_V
			self.chaine += chaine_tmp+'\n'
			
			# Sépartion lignes intermédiaires
			if j!=self.ymax-1 :
				self.chaine += CAR_TG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD+'\n'
				
			# Dernière ligne
			else :
				self.chaine += CAR_CBG+(CAR_H*3+CAR_TB)*self.xmax+CAR_H*3+CAR_CBD+'\n'
		
		return self.chaine
		
	def affiche(self):
		self.make_chaine()
		print(self.chaine)
		#~ print(fusionne(self.chaine, self.chaine))
	
class GrilleJoueurC(GrilleC, GrilleJoueur):
	"""La grille sur laquelle chaque joueur place ses bateaux"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleJoueur.__init__(self, xmax, ymax, taille_bateaux)
		GrilleC.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuiviC(GrilleC, GrilleSuivi):
	"""La grille de suivi des coups joués"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleSuivi.__init__(self, xmax, ymax, taille_bateaux)
		GrilleC.__init__(self, xmax, ymax, taille_bateaux)

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
		ok = False
		while not ok :
			case = input('<%s> Coups (Entrée pour un coup aléatoire) : ' % self.nom)
			if case == '' :
				self.tire_aleatoire()
				ok = True
			else :
				try :
					tmp_cases_jouees = self.cases_jouees[:]
					self.tire(coord(case))
					if coord(case) in tmp_cases_jouees :
						self.affiche_messages()
					else :
						ok = True
				except :
					self.messages.append("%s : Coup invalide" % case)
					self.affiche_messages()
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
		# affiche : affichage ou non des informations (pour les tests)
		
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
	def lance_partie0(self):
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
	
	def affiche_grilles(self):
		clear()
		grille1 = centre(self.joueur.nom, 5+4*self.joueur.grille_suivi.xmax)
		grille1 += self.joueur.grille_suivi.make_chaine()
		grille2 = centre(self.adversaire.nom, 5+4*self.adversaire.grille_suivi.xmax)
		grille2 += self.adversaire.grille_suivi.make_chaine()
		print(fusionne(grille1, grille2))
	
	def lance_partie(self):
		"""Partie à deux joueurs"""
		self.place_bateaux_joueur()
		self.get_bateaux_adverse()
		self.adversaire.grille_adverse = self.joueur.grille_joueur
		
		clear()
		print("Votre grille de jeu :")
		print()
		for case in self.joueur.grille_joueur.etat :
			if self.joueur.grille_joueur.etat[case] == -1 :
				self.joueur.grille_joueur.etat[case] = 0 
		self.joueur.grille_joueur.affiche()
		print()
		enter_to_continue()
		
		while not self.joueur.grille_suivi.fini() and not self.adversaire.grille_suivi.fini() :
			clear()
			self.affiche_grilles()

			self.joueur.joue_coup()
			self.affiche_grilles()
			self.joueur.affiche_messages()
			print()

			if not self.adversaire.grille_suivi.fini() :
				enter_to_continue()
				clear()
				self.get_coup_adverse()
				self.affiche_grilles()
				self.adversaire.affiche_messages()
			if not self.adversaire.grille_suivi.fini() :
				print()
				enter_to_continue()

		print()
		if self.joueur.grille_suivi.fini():
			print("Vous avez gagné en %d coups" % self.joueur.essais)
		else :
			print("%s a gagné en %d coups" % (self.adversaire.nom, self.adversaire.essais))


#
#----------------------------------------------------------------------------------------------------------------
#

class main_console(object):
	"""Programme principal en mode console"""
	def __init__(self):
		self.launch_menu()
	#
	# Modes de jeu -----------------------------------------------------
	#
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
			(essais, temps) = self.jeu_ordi(affiche=False)
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
	
	#
	# Menu de lancement ------------------------------------------------
	#
	def launch_menu(self):
		"""Menu de lancement """
		clear()
		# http://patorjk.com/software/taag/
		print("""╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██████╗  █████╗ ████████╗ █████╗ ██╗██╗     ██╗     ███████╗   ║
║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║██║     ██║     ██╔════╝   ║
║   ██████╔╝███████║   ██║   ███████║██║██║     ██║     █████╗     ║
║   ██╔══██╗██╔══██║   ██║   ██╔══██║██║██║     ██║     ██╔══╝     ║
║   ██████╔╝██║  ██║   ██║   ██║  ██║██║███████╗███████╗███████╗   ║
║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝   ║
║                                                                  ║
║       ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ███████╗        ║
║       ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝        ║
║       ██╔██╗ ██║███████║██║   ██║███████║██║     █████╗          ║
║       ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝          ║
║       ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗███████╗        ║
║       ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
		print("Projet de formation ISN 2015/2016 de l'académie de Lyon")
		print("   Auteurs : F.Muller et L.Reboul")
		print("   Licence Creative Common CC BY-NC-SA")
		print()
		print("Il est conseillé de passer en mode plein écran (F11)")
		enter_to_continue()
		clear()
		print("""╔════════════════╗
║ Choix du jeu : ║ 
╚════════════════╝
  S : Jeu en solo sur une grille aléatoire
  O : Résolution d'une grille par l'ordinateur
  J : Jeu contre l'ordinateur
  T : Test des performances de l'algorithme de résolution
  Q : Quitter
	  """)
		choix = input("Votre choix [s|o|j|t|[Q]] : ")
		
		if choix.lower() == 's' :
			self.jeu_solo()
			
		elif choix.lower() == 't' :
			clear()
			n = int(input("Nombre de répétitions de l'algorithme : "))
			self.test_algo(n)
			
		elif choix.lower() == 'o' :
			self.jeu_ordi()
			
		elif choix.lower() == 'j' :
			self.jeu_contre_ordi()
			
		else :
			info()
			info("Au revoir...")
			quit()


if __name__ == "__main__" :
	app = main_console()
