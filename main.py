#!/usr/bin/python3

#
# Projet de bataille navale
# dans le cadre de la formation ISN 2015/2016
# de l'académie de Lyon
#
# Programme principal
#
# Auteurs : Frédéric Muller et Lionel Reboul
#
# Licence CC BY-NC-SA
#
# Projet démarré le 14/11/2015
# Dernière màj : 03/12/2015
# Version 0.1.0
#

import argparse

from bn_interface import *
from bn_console import *

if __name__== '__main__' :
	"""Programme principal"""
	
	# Récupération des arguments en ligne de commande
	parser = parser = argparse.ArgumentParser(description='Jeu de bataille navale')
	parser.add_argument('--interface', '-i', action="store", dest="interface", help="Choix de l'interface : console ou tkinter", default="console")
	
	options = parser.parse_args()
	
	# Lancement de l'interface
	if options.interface == "console" :
		app = main_console()
	elif options.interface == "tkinter" :
		print("Interface tkinter à implémenter")


