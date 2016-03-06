#!/usr/bin/python3

"""
 ╔══════════════════════════════════════════════════════════════════╗
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


 Projet dans le cadre de la formation ISN 2015/2016 de l'académie de Lyon

 Programme principal

 Auteur : Frédéric Muller
 Code du projet : https://github.com/Abunux/pyBatNav
 Licence Creative Common CC BY-NC-SA

 Projet démarré le 14/11/2015
 Dernière màj : 04/03/2016
 Version 0.1.0"""


import argparse

from bn_console import *
from bn_tkinter import *

if __name__== '__main__' :
    """Programme principal"""

    # Récupération des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Jeu de bataille navale')
    parser.add_argument('--interface', '-i', action="store", dest="interface", help="Choix de l'interface : 'console' ou 'tkinter'", default="")

    options = parser.parse_args()

    # Lancement de l'interface
    if options.interface.lower() == "console" :
        app = MainConsole()
    elif options.interface.lower() == "tkinter" :
        app = MainTK()
    else :
        print("""Choix de l'interface :
  C : Console
  T : Tkinter""")
        choix = input("Votre choix (C|t) : ")
        if choix.lower() == 't' :
            app = MainTK()
        else :
            app = MainConsole()


