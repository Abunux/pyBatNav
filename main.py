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
from bn_webserveur import *

if __name__== '__main__' :
    """Programme principal"""

    # Récupération des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Jeu de bataille navale')
    parser.add_argument('--interface', '-i', action="store", dest="interface", help="Choix de l'interface : 'tkinter', 'console' ou 'web'", default="")

    options = parser.parse_args()

    # Lancement de l'interface
    if options.interface.lower() == "console" :
        app = MainConsole()
    elif options.interface.lower() == "tkinter" :
        app = MainTK()
    elif options.interface.lower() == "web" :
        launch_serveur()
    else :
        print("""Choix de l'interface :
  T : Tkinter
  C : Console
  W : Web""")
        choix = input("Votre choix ([t]|c|w) : ")
        if choix.lower() == 'c' :
            app = MainConsole()
        if choix.lower() == 'w' :
            launch_serveur()
        else :
            app = MainTK()


