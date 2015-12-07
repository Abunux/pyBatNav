#!/usr/bin/python3

# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║   ██████╗  █████╗ ████████╗ █████╗ ██╗██╗     ██╗     ███████╗   ║
# ║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║██║     ██║     ██╔════╝   ║
# ║   ██████╔╝███████║   ██║   ███████║██║██║     ██║     █████╗     ║
# ║   ██╔══██╗██╔══██║   ██║   ██╔══██║██║██║     ██║     ██╔══╝     ║
# ║   ██████╔╝██║  ██║   ██║   ██║  ██║██║███████╗███████╗███████╗   ║
# ║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝   ║
# ║                                                                  ║
# ║        ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ███████╗       ║
# ║        ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝       ║
# ║        ██╔██╗ ██║███████║██║   ██║███████║██║     █████╗         ║
# ║        ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝         ║
# ║        ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗███████╗       ║
# ║        ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝       ║
# ║                                                                  ║
# ╚══════════════════════════════════════════════════════════════════╝

#
# Projet dans le cadre de la formation ISN 2015/2016 de l'académie de Lyon
#
# Programme principal
#
# Auteurs : Frédéric Muller et Lionel Reboul
# Code du projet : https://github.com/Abunux/pyBatNav
# Licence Creative Common CC BY-NC-SA
#
# Projet démarré le 14/11/2015
# Dernière màj : 07/12/2015
# Version 0.1.0
#

import argparse

from bn_interface import *
from bn_console import *

if __name__== '__main__' :
	"""Programme principal"""
	
	# Récupération des arguments en ligne de commande
	parser = argparse.ArgumentParser(description='Jeu de bataille navale')
	parser.add_argument('--interface', '-i', action="store", dest="interface", help="Choix de l'interface : 'console' ou 'tkinter'", default="console")
	
	options = parser.parse_args()
	
	# Lancement de l'interface
	if options.interface.lower() == "console" :
		app = MainConsole()
	elif options.interface.lower() == "tkinter" :
		print("Interface tkinter à implémenter")


