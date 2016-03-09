#!/usr/bin/env python3

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
 Licence Creative Common CC BY-NC-SA v4.0

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
    parser.add_argument('--console','-c', action="store_true", dest="console", default=False, help="Interface console")
    parser.add_argument('--tkinter','-t', action="store_true", dest="tkinter", default=False, help="Interface tkinter")
    parser.add_argument('--web', '-w', action="store_true", dest="web", default=False, help="Interface web (serveur)")
    options = parser.parse_args()

    # Lancement de l'interface
    if options.console :
        app = MainConsole()
    elif options.tkinter :
        app = MainTK()
    elif options.web :
        launch_serveur()
    else :
        print("""Choix de l'interface :
  T : Tkinter
  C : Console
  W : Web (serveur)""")
        choix = input("Votre choix ([t]|c|w) : ")
        if choix.lower() == 'c' :
            app = MainConsole()
        if choix.lower() == 'w' :
            launch_serveur()
        else :
            app = MainTK()
