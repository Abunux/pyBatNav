# Version 0.1.0

import os

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
