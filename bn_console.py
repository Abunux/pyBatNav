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
from math import *
import matplotlib.pyplot as plt
import numpy as np

from bn_grille import *
from bn_joueur import *

# --------------------------------------------
# Caractères graphiques (pour faire la grille)
# --------------------------------------------
# http://www.unicode.org/charts/ --> Box Drawing (U2500.pdf)

# Caractères simples pour la grille
# ---------------------------------
# Traits
CAR_H = u'\u2500'		# Trait Horizontal : ─
CAR_V = u'\u2502'		# Trait Vertical : │
# Coins
CAR_CHG = u'\u250C'		# Coin Haut Gauche : ┌
CAR_CHD = u'\u2510'		# Coin Haut Droite : ┐
CAR_CBG = u'\u2514'		# Coin Bas Gauche : └
CAR_CBD = u'\u2518'		# Coin Bas Droite : ┘
# T
CAR_TH = u'\u252C'		# T Haut : ┬
CAR_TB = u'\u2534'		# T Bas : ┴
CAR_TG = u'\u251C'		# T Gauche : ├
CAR_TD = u'\u2524'		# T Droite : ┤
# +
CAR_CX = u'\u253C'		# Croix Centrale : ┼

# Caractères en gras pour les bateaux
# -----------------------------------
# Traits
CAR_GH = u'\u2501'		# Trait Gras Horizontal : ━
CAR_GV = u'\u2503'		# Trait Gras Vertical : ┃
# T
CAR_GTB = u'\u2537'		# T Gras Bas : ┷
CAR_GTD = u'\u2528'		# T Gras Droite : ┨
CAR_GTDH = u'\u252A'	# T Droite Haut : ┪
CAR_GTDB = u'\u2529'	# T Droite Bas : ┩
CAR_GTBG = u'\u253A'	# T Bas Gauche : ┺
CAR_GTBD = u'\u2539'	# T Bas Droite : ┹

# Coins
CAR_GCBD = u'\u251B'	# Coin Gras Bas Gauche : ┛
# +
CAR_GCXHG = u'\u2546'	# Croix Gras Haut Gauche : ╆
CAR_GCXHD = u'\u2545'	# Croix Gras Haut Droite : ╅
CAR_GCXBG = u'\u2544'	# Croix Gras Bas Gauche : ╄
CAR_GCXBD = u'\u2543'	# Croix Gras Bas Droite : ╃
CAR_GCX = u'\u254B'		# Croix Gras Centrale : ╋
CAR_GCXH = u'\u253F'	# Croix Gras Horizontal : ┿
CAR_GCXV = u'\u2542'	# Croix Gras Vertical : ╂



# Touché / Manqué
# ---------------
CAR_TOUCH = u'\u2716' 	# Touché : ✖
CAR_MANQ = u'\u25EF' 	# Manqué : ◯

#
# Fonctions utiles ----------------------------------------------------------------------------------------------
#
def clear():
	"""Efface la console"""
	if (os.name == 'nt'):  
		os.system('cls')
	else:
		os.system('clear') 

def info(*args):
	"""Affiche les infos à l'écran"""
	print(*args)
	
def enter_to_continue():
	input("Appuyez sur Entrée pour continuer ")

def fusionne(chaine1, chaine2):
	"""Fusionne deux grilles pour l'affichage"""
	lignes1 = chaine1.split('\n')
	lignes2 = chaine2.split('\n')
	chaine = ""
	for k in range(len(lignes1)-1):
		chaine += lignes1[k] + '  ' + CAR_GV + '  ' + lignes2[k] + '\n'
	return chaine

def centre(chaine, longueur):
	"""Centre la chaine sur la longueur"""
	c = len(chaine)
	l = longueur
	return ' '*((l-c)//2) + chaine + ' '*((l-c)//2+(l-c)%2) + '\n'

def boite(texte, prefixe ='', larg_fen = 98):
	"""Affiche chaque ligne de texte précédée d'un préfixe
	dans une boîte de largeur larg_fen"""
	lignes = texte.split('\n')
	if larg_fen == 0 :
		larg_fen = max([len(l) for l in lignes])+2
	chaine = ""
	chaine += '╔' + '═'*larg_fen + '╗' + '\n'
	for ligne in lignes :
		chaine += "║ %s%s" % (prefixe, ligne) + ' '*(larg_fen-(len(ligne)+len(prefixe)+1)) + '║' + '\n'
	chaine += '╚' + '═'*larg_fen + '╝'
	return chaine
	
#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleC(Grille) :
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux = taille_bateaux)
		
		# Chaine de caractères pour affichage de la grille
		self.chaine = ""
		
	#
	# Affichage en console ---------------------------------------------
	#
	def make_chaine(self):
		"""Crée la grille avec des caractères graphiques"""
		self.chaine = ""
		
		# Ligne du haut
		self.chaine += '    ' + CAR_CHG + (CAR_H*3 + CAR_TH)*(self.xmax-1) + CAR_H*3 + CAR_CHD + '\n'
		
		# Ligne des lettres des colonnes
		self.chaine += '    ' + CAR_V
		for i in range(self.xmax):
			if i != self.xmax-1 :
				self.chaine += ' ' + chr(i+65) + ' ' + CAR_V
				#~ chaine += ' ' + str(i) + ' ' + CAR_V
			else :
				self.chaine += ' ' + chr(i+65) + ' ' + CAR_V + '\n'
				#~ chaine += ' ' + str(i) + ' ' + CAR_V + '\n'
				
		#Ligne sous les lettres
		self.chaine += CAR_CHG + (CAR_H*3+CAR_CX)*self.xmax + CAR_H*3 + CAR_TD + '\n'
		
		# Lignes suivantes
		for j in range(self.ymax):
			# 1ère colonne (chiffres des lignes)
			chaine_tmp = CAR_V + ' ' + str(j) + ' ' + CAR_V
			
			# Cases suivantes
			for i in range(self.xmax):
				if self.etat[(i,j)] == 1 :
					symbole = CAR_TOUCH
				elif self.etat[(i,j)] == -1 :
					symbole = CAR_MANQ
				else :
					symbole = ' '
				chaine_tmp += ' ' + symbole + ' ' + CAR_V
			self.chaine += chaine_tmp + '\n'
			
			# Sépartion lignes intermédiaires
			if j != self.ymax-1 :
				self.chaine += CAR_TG + (CAR_H*3+CAR_CX)*self.xmax + CAR_H*3 + CAR_TD + '\n'
				
			# Dernière ligne
			else :
				self.chaine += CAR_CBG + (CAR_H*3+CAR_TB)*self.xmax + CAR_H*3 + CAR_CBD + '\n'
		
		return self.chaine
		
	def make_chaine_adverse(self, grille=None):
		"""Crée la grille avec des caractères graphiques
		en entourant en gras nos bateaux"""
		#~ ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
		#~ │ 4 │   │   │   │   │   │   │   │   │   │   │
		#~ ├───┼───┼───┼───╆━━━╅───┼───┼───┼───┼───┼───┤
		#~ │ 5 │   │   │   ┃ ✖ ┃   │   │   │   │   │   │
		#~ ├───┼───┼───┼───╂───╂───┼───┼───╆━━━╅───┼───┤
		#~ │ 6 │   │   │   ┃ ✖ ┃   │   │   ┃   ┃   │   │
		#~ ├───┼───┼───┼───╄━━━╋━━━┿━━━╅───╂───╂───┼───┤
		#~ │ 7 │   │   │   │   ┃   │   ┃   ┃ ✖ ┃   │   │
		#~ ├───┼───┼───┼───┼───╄━━━┿━━━╃───╂───╂───╆━━━┪
		#~ │ 8 │   │   │   │   │   │   │   ┃   ┃   ┃   ┃
		#~ ├───┼───┼───┼───┼───┼───┼───┼───╄━━━╃───╂───┨
		#~ │ 9 │   │   │   │   │   │   │   │   │   ┃   ┃
		#~ └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┺━━━┛
		
		# grille est la grille du joueur, celle pour laquelle on entoure les bateaux en gras
		if not grille :
			grille = self
		
		chaine = ""
		
		# Ligne du haut
		chaine += '    ' + CAR_CHG + (CAR_H*3 + CAR_TH)*(grille.xmax-1) + CAR_H*3 + CAR_CHD + '\n'
		
		# Ligne des lettres des colonnes
		chaine += '    '+CAR_V
		for i in range(grille.xmax):
			if i != grille.xmax-1 :
				chaine += ' ' + chr(i+65) + ' ' + CAR_V
				#~ chaine += ' '+str(i)+' '+CAR_V
			else :
				chaine += ' ' + chr(i+65) + ' ' + CAR_V + '\n'
				#~ chaine += ' '+str(i)+' '+CAR_V+'\n'
				
		# Ligne sous les lettres (à cause du coin en haut à gauche)
		j = 0
		chaine += CAR_CHG + CAR_H*3
		for i in range(grille.xmax) :
			if i == 0 :
				if grille.etat[(i,j)] == 1 :
					chaine += CAR_GCXHG + CAR_GH*3
				else :
					chaine += CAR_CX + CAR_H*3
			else :
				if grille.etat[(i,j)] == 1 :
					if grille.etat[(i-1, j)] == 1 :
						chaine += CAR_GCXH + CAR_GH*3
					else :
						chaine += CAR_GCXHG + CAR_GH*3
				else :
					if grille.etat[(i-1, j)] == 1 :
						chaine += CAR_GCXHD + CAR_H*3
					else :
						chaine += CAR_CX + CAR_H*3
		i = grille.xmax-1
		if grille.etat[(i,j)] == 1 :
			chaine += CAR_GTDH + '\n'
		else :
			chaine += CAR_TD + '\n'
		
		# Lignes suivantes
		for j in range(grille.ymax):
			# 1ère colonne (chiffres des lignes)
			chaine += CAR_V + ' ' + str(j) + ' '
			
			# Cases suivantes
			for i in range(grille.xmax):
				# Symbole est l'état de la case dans la grille de suivi
				if self.etat[(i,j)] == 1 :
					symbole = ' ' + CAR_TOUCH + ' '
				elif self.etat[(i,j)] == -1 :
					symbole = ' ' + CAR_MANQ + ' '
				else :
					symbole = '   '
					
				# Création de la ligne
				if grille.etat[(i,j)] == 1 :
					if (i == 0 or grille.etat[(i-1, j)] != 1) :
						chaine += CAR_GV + symbole
					elif (grille.etat[(i-1, j)] == 1) or ((i < grille.xmax-1) and grille.etat[(i+1, j)] == 1) :
						chaine += CAR_V + symbole
				else :
					if (i > 0 and grille.etat[(i-1, j)] == 1) :
						chaine += CAR_GV + symbole
					else :
						chaine += CAR_V + symbole
			i = grille.xmax-1
			if grille.etat[(i, j)] == 1 :
				chaine += CAR_GV + '\n'
			else :
				chaine += CAR_V + '\n'
			
			# Sépartion lignes intermédiaires
			if j != grille.ymax-1 :
				chaine += CAR_TG + CAR_H*3
				for i in range(grille.xmax):
					if i == 0 :
						if grille.etat[(i, j)] == 1 :
							if grille.etat[(i, j+1)] == 1 :
								chaine += CAR_GCXV + CAR_H*3
							else :
								chaine += CAR_GCXBG + CAR_GH*3
						else :
							if grille.etat[(i, j+1)] == 1 :
								chaine += CAR_GCXHG + CAR_GH*3
							else :
								chaine += CAR_CX + CAR_H*3
					else :
						if grille.etat[(i, j)] == 1 :
							if grille.etat[(i, j+1)] == 1 :
								chaine += CAR_GCXV + CAR_H*3
							else :
								if grille.etat[(i-1, j)] == 1 :
									chaine += CAR_GCXH + CAR_GH*3
								else :
									if grille.etat[(i-1, j+1)] == 1 :
										chaine += CAR_GCX + CAR_GH*3
									else :
										chaine += CAR_GCXBG + CAR_GH*3
						else :
							if grille.etat[(i, j+1)] == 1 :
								if grille.etat[(i-1, j+1)] == 1 :
									chaine += CAR_GCXH + CAR_GH*3
								else :
									if grille.etat[(i-1, j)] == 1 :
										chaine += CAR_GCX + CAR_GH*3
									else :
										chaine += CAR_GCXHG + CAR_GH*3
							else :
								if grille.etat[(i-1, j)] == 1 :
									if grille.etat[(i-1, j+1)] == 1 :
										chaine += CAR_GCXV + CAR_H*3
									else :
										chaine += CAR_GCXBD + CAR_H*3
								else :
									if grille.etat[(i-1, j+1)] == 1 :
										chaine += CAR_GCXHD + CAR_H*3
									else :
										chaine += CAR_CX + CAR_H*3
				i = grille.xmax-1
				if grille.etat[(i,j)] == 1 :
					if grille.etat[(i,j+1)] == 1 :
						chaine += CAR_GTD + '\n'
					else :
						chaine += CAR_GTDB + '\n'
				else :
					if grille.etat[(i,j+1)] == 1 :
						chaine += CAR_GTDH + '\n'
					else :
						chaine += CAR_TD + '\n'
				
			# Dernière ligne
			else :
				chaine += CAR_CBG + CAR_H*3
				for i in range(grille.xmax) :
					if i == 0 :
						if grille.etat[(i,j)] == 1 :
							chaine += CAR_GTBG + CAR_GH*3
						else :
							chaine += CAR_TB + CAR_H*3
					else :
						if grille.etat[(i,j)] == 1 :
							if grille.etat[(i-1, j)] == 1 :
								chaine += CAR_GTB + CAR_GH*3
							else :
								chaine += CAR_GTBG + CAR_GH*3
						else :
							if grille.etat[(i-1, j)] == 1 :
								chaine += CAR_GTBD + CAR_H*3
							else :
								chaine += CAR_TB + CAR_H*3
				i = grille.xmax-1
				if grille.etat[(i,j)] == 1 :
					chaine += CAR_GCBD + '\n'
				else :
					chaine += CAR_CBD + '\n'

		return chaine
		
		
	def affiche(self):
		"""Affiche une grille"""
		self.make_chaine()
		info(self.chaine)
		
	def affiche_adverse(self, grille=None):
		"""Affiche la grille de suivi de l'adversaire en entourant nos propres bateaux"""
		info(self.make_chaine_adverse(grille))
		

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
		
		# Largeur de la zone d'affichage de la grille
		self.long_affiche = 5 + 4*self.grille_suivi.xmax
		# Création de la boîte d'affichage du nom
		self.chaine_nom = ''
		lnom = len(self.nom)
		self.chaine_nom += centre('╔'  + '═'*(lnom+2) +  '╗', self.long_affiche)
		self.chaine_nom += centre('║ ' +   self.nom   + ' ║', self.long_affiche)
		self.chaine_nom += centre('╚'  + '═'*(lnom+2) +  '╝', self.long_affiche)

	def affiche_messages(self, affiche=True):
		if affiche :
			info(boite('\n'.join(self.messages), prefixe="<%s> " % self.nom))
			self.messages = []
		
	def joue_coup(self):
		"""Joue un coup sur une case"""
		ok = False
		while not ok :
			case = input('<%s> Coup (Entrée pour un coup aléatoire) : ' % self.nom)
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
		
	def resolution(self, affiche=True, grille=None):
		"""Lance la résolution de la grille par l'ordinateur"""
		# affiche : affichage ou non des informations (pour les tests)
		
		# Lancement du chrono
		start = time()
		self.messages.append("C'est parti !!!")
		# C'est parti !!!
		while not self.grille_suivi.fini():
			if affiche :
				clear()
				self.grille_suivi.affiche_adverse(grille)
			
			self.affiche_messages(affiche=affiche)
			
			self.coup_suivant()
			
			if affiche :
				input("Entrée pour continuer")
			
		# Fin de la partie
		if affiche :
			clear()
			self.grille_suivi.affiche_adverse(grille)
			
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
		case = input("Case de départ (Entrée pour un bateau aléatoire) : ")
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
		info("  H : Haut")
		info("  B : Bas")
		info("  D : Droite")
		info("  G : Gauche")
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
			self.add_bateau_joueur()
			return False
		return self.joueur.add_bateau(taille, case, direction)
		
	def place_bateaux_joueur(self):
		"""Place tous les bateaux du joueur"""
		for taille in self.joueur.grille_joueur.taille_bateaux[::-1] :
			clear()
			info(boite("Placement de vos bateaux", larg_fen=0))
			#~ info()
			self.joueur.grille_joueur.affiche_adverse()
			while not self.add_bateau_joueur(taille):
				info("Le bateau de taille %d ne convient pas" % taille)
				info()
		for case in self.joueur.grille_joueur.etat :
			if self.joueur.grille_joueur.etat[case] == -1 :
				self.joueur.grille_joueur.etat[case] = 0 
	
	#
	# Lancement de la partie -------------------------------------------
	#
	def affiche_grilles(self, fin=False, cheat=False):
		"""Affiche les deux grilles cote à cote, avec les noms des joueurs"""
		clear()
		grille1 = self.joueur.chaine_nom
		# Pour l'affichage en fin de partie on affiche en gras les bateaux de l'adversaire
		# cheat permet de tricher en affichant les bateaux de l'adversaire (pour les tests)
		if fin or cheat :
			grille1 += self.joueur.grille_suivi.make_chaine_adverse(self.adversaire.grille_joueur)
		else :
			grille1 += self.joueur.grille_suivi.make_chaine()
			
		grille2 = self.adversaire.chaine_nom
		grille2 += self.adversaire.grille_suivi.make_chaine_adverse(self.joueur.grille_joueur)
		
		info(fusionne(grille1, grille2))
	
	def lance_partie(self):
		"""Partie à deux joueurs"""
		# Placement des bateaux
		self.place_bateaux_joueur()
		self.get_bateaux_adverse()
		self.adversaire.grille_adverse = self.joueur.grille_joueur
		clear()
		info(boite("Votre grille de jeu", larg_fen=0))
		self.joueur.grille_joueur.affiche_adverse()
		
		# Détermination du joueur qui commence
		joueur_en_cours = rand.randint(0,1) 
		if  joueur_en_cours == 0 :
			info(boite("Vous allez commencer", larg_fen=0))
		else :
			info(boite("%s va commencer" % self.adversaire.nom, larg_fen=0))
		info()
		enter_to_continue()
		
		# Début de la partie
		nb_coups = 0
		while not self.joueur.grille_suivi.fini() and not self.adversaire.grille_suivi.fini() :
			nb_coups += 1
			# Le joueur joue
			if joueur_en_cours == 0 and not self.adversaire.grille_suivi.fini():
				clear()
				self.affiche_grilles()
				self.joueur.joue_coup()
				self.affiche_grilles()
				self.joueur.affiche_messages()
				enter_to_continue()
			
			# L'adversaire joue
			else :
				clear()
				self.get_coup_adverse()
				self.affiche_grilles()
				self.adversaire.affiche_messages()
				enter_to_continue()
			
			# Changement de joueur
			joueur_en_cours = (joueur_en_cours + 1) % 2
				
		# Fin de la partie
		clear()
		self.affiche_grilles(fin=True)
		info()
		if self.joueur.grille_suivi.fini():
			info(boite("Bravo !! Vous avez gagné en %d coups" % self.joueur.essais))
		else :
			info(boite("%s a gagné en %d coups" % (self.adversaire.nom, self.adversaire.essais)))


#
#----------------------------------------------------------------------------------------------------------------
#

class MainConsole(object):
	"""Programme principal en mode console"""
	def __init__(self):
		self.launch_menu()

	#
	# Modes de jeu -----------------------------------------------------
	#
	def jeu_ordi(self, affiche=True, xmax=10, ymax=10, taille_bateaux=[5,4,3,3,2]):
		"""Résolution d'une grille par l'ordinateur"""
		# Initialisation de la partie
		grille = GrilleJoueurC(xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		grille.init_bateaux_alea()
		ordi = OrdiC()
		ordi.grille_adverse = grille
		ordi.grille_suivi = GrilleSuiviC(xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		ordi.grille_suivi.reinit()
		
		temps = ordi.resolution(affiche=affiche, grille=grille)
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


	def test_algo(self, n=1000, xmax=10, ymax=10, taille_bateaux=[5,4,3,3,2]):
		"""Test l'ago de l'ordinateur en faisant n parties"""
		# Lancement de la simulation
		start = time()
		temps_resolution = 0
		liste_essais = []
		for k in range(n):
			(essais, temps) = self.jeu_ordi(affiche=False, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
			temps_resolution += temps
			liste_essais.append(essais)
			if (k+1) % (n/10) == 0 :
				info("Avancement : %d%% (Temps restant estimé : %.2f secondes)" % (100*(k+1)//n, (n-k-1)*(time()-start)/(k+1)))
		
		# Création de la liste de distribution des effectifs
		distrib = [0]*(xmax*ymax)
		for e in liste_essais :
				distrib[e] += 1
		
		# Indicateurs statistiques
		mini = min(liste_essais)
		maxi = max(liste_essais)
		moyenne = sum(liste_essais)/n
		mode = distrib.index(max(distrib))
		liste_essais_sorted = liste_essais[:]
		liste_essais_sorted.sort()
		if n % 2 != 0 :
			mediane = liste_essais_sorted[(n+1)//2-1]
		else :
			mediane = (liste_essais_sorted[n//2-1]+liste_essais_sorted[n//2])/2
		q1 = liste_essais_sorted[ceil(n/4)-1]
		q3 = liste_essais_sorted[ceil(3*n/4)-1]
		variance = 0
		for k in range(n):
			variance += (liste_essais[k]-moyenne)**2
		variance *= 1/n
		sigma = sqrt(variance) 
		
		info()
		info(boite("Résultats de la simulation", larg_fen=0))
		info()
		info("Dimensions de la grille : %d*%d" % (xmax , ymax))
		info("Liste des bateaux : %s" % str(taille_bateaux))
		info("Nombre de parties : %d" % n)
		info()
		info("Min : %d" % mini)
		info("Q1  : %d" % q1)
		info("Méd : %.1f" % mediane)
		info("Q3  : %d" % q3)
		info("Max : %d" % maxi)
		info()
		info("Mode : %d" % mode)
		info()
		info("Moyenne : %.2f" % moyenne)
		info("Sigma   : %.2f" % sigma)
		
		info()
		tmoy = temps_resolution/n
		info("Temps moyen par partie : %.5f secondes" % (temps_resolution/n))
		info("Temps total            : %.2f secondes" % (time()-start))
		
		filename = "distrib_HAL_NEW_(n=%d,xmax=%d,ymax=%d,bateaux=%s)" % (n, xmax, ymax,str(taille_bateaux))
		# --> L'idée c'est de voir quelle loi de proba suit le nombre d'essais
		# et de calculer des indicateurs statistiques
		# Sauvegarde de cette liste dans un fichier texte
		#~ stats_file = open("distrib_HAL_NEW_(n=%d,nb_echantillons=%d,xmax=%d,ymax=%d,bateaux=%s).txt" % (n, nb_echantillons, xmax, ymax,str(taille_bateaux)), "w")
		stats_file = open(filename + ".txt", "w")
		for k in range(len(distrib)) :
			stats_file.write(str(distrib[k])+'\n')
		stats_file.close()
		
		# Figure statistique 
		# ------------------
		fig = plt.figure()
		# Création de l'histogramme
		plt.hist(liste_essais, bins=np.arange(mini-0.5, maxi+1.5, 1), normed=1, facecolor='g', alpha=0.75)
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
		plt.title("Résolution par l'ordinateur sur n=%d parties\nXmax=%d , Ymax=%d , Bateaux : %s" % (n, xmax, ymax," ".join([str(t) for t in taille_bateaux])))
		plt.grid(True)
		plt.savefig(filename + ".png", dpi=fig.dpi)
		plt.show()
		
		return liste_essais # Pour tests futurs
	
	def launch_test_algo(self):
		"""Lancement de la procédure de test de l'algorithme de résolution"""
		clear()
		xmax = ymax = 10
		taille_bateaux = [5, 4, 3, 3, 2]
		# Paramètres des parties à simuler
		info("Paramètres par défaut : xmax=%d, ymax=%d, bateaux=%s\n" % (xmax, ymax, taille_bateaux))
		rep = input("Voulez-vous changer ces paramètres ? [o|[N]] ")
		if rep.lower()=='o' :
			ok = False
			while not ok :
				try :
					xmax = int(input("xmax : "))
					ymax = int(input("ymax : "))
					tb = input("Bateaux (séparés par un espace) : ")
					taille_bateaux = [int(t) for t in tb.split(' ')]
					ok = True
				except :
					info("Saisie invalide\n")
					ok = False

		ok = False
		while not ok :
			try :
				n = int(input("Nombre de parties : "))
				ok = True
			except :
				info("Saisie invalide\n")
				ok = False
		# Lancement du test
		self.test_algo(n, xmax, ymax, taille_bateaux)
	
	#
	# Menu de lancement ------------------------------------------------
	#
	def launch_menu(self):
		"""Menu de lancement """
		defaut = self.jeu_contre_ordi
		
		clear()
		info(boite("""
 Pour un affichage du jeu optimal, veuillez passer 
 en mode plein écran (F11),régler les couleurs du  
 terminal en écriture noire sur fond blanc et, si 
 besoin, diminuer la taille de la police (pour une 
 résolution de 1024x768, une taille 12 convient). 
""", larg_fen=0))
		info()
		enter_to_continue()
		clear()
		
		# source : http://patorjk.com/software/taag/
		info("""     ╔══════════════════════════════════════════════════════════════════╗
     ║                                                                  ║
     ║   ██████╗  █████╗ ████████╗ █████╗ ██╗██╗     ██╗     ███████╗   ║
     ║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║██║     ██║     ██╔════╝   ║
     ║   ██████╔╝███████║   ██║   ███████║██║██║     ██║     █████╗     ║
     ║   ██╔══██╗██╔══██║   ██║   ██╔══██║██║██║     ██║     ██╔══╝     ║
     ║   ██████╔╝██║  ██║   ██║   ██║  ██║██║███████╗███████╗███████╗   ║
     ║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝   ║
     ║                                                                  ║
     ║        ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ███████╗       ║
     ║        ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝       ║
     ║        ██╔██╗ ██║███████║██║   ██║███████║██║     █████╗         ║
     ║        ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝         ║
     ║        ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗███████╗       ║
     ║        ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝       ║
     ║                                                                  ║
     ╚══════════════════════════════════════════════════════════════════╝
""")
		info("             Projet de formation ISN 2015/2016 de l'académie de Lyon")
		info("                Auteurs : Frédéric Muller et Lionel Reboul")
		info("                Code du projet : https://github.com/Abunux/pyBatNav")
		info("                Licence Creative Common CC BY-NC-SA")
		
		# source : http://www.chris.com/ascii/index.php?art=transportation/nautical
		info(r"""
                                     |__
                                     |\/
                                     ---
                                     / | [
                              !      | |||
                            _/|     _/|-++'
                        +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                                                                     BB-61/
 \_________________________________________________________________________|
 """)
		info()
		
		while True :
			enter_to_continue()
			clear()
			info(boite("Choix du jeu", larg_fen=0))
			info("""  J : Jeu contre l'ordinateur
  S : Jeu en solo sur une grille aléatoire
  O : Résolution d'une grille par l'ordinateur
  T : Test des performances de l'algorithme de résolution
  Q : Quitter
	  """)
			choix = input("Votre choix ([J]|s|o|t|q) : ")
			
			if choix.lower() == 's' :
				self.jeu_solo()
				
			elif choix.lower() == 't' :
				self.launch_test_algo()
				
			elif choix.lower() == 'o' :
				self.jeu_ordi()
				
			elif choix.lower() == 'j' :
				self.jeu_contre_ordi()
				
			elif choix.lower() == 'q' :
				info()
				info("Au revoir...")
				quit()
			
			# Par défaut
			else :
				defaut()

if __name__ == "__main__" :
	app = MainConsole()
