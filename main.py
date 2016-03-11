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


 Projet de validation de la formation ISN 2015/2016 de l'académie de Lyon

 Programme principal

 Auteur : Frédéric Muller
 Code du projet : https://github.com/Abunux/pyBatNav
 Licence Creative Common CC BY-NC-SA v4.0

 Projet démarré le 14/11/2015
 Dernière màj : 11/03/2016
 Version 0.1.0"""

import argparse

if __name__== '__main__' :
    """Programme principal"""

    # Récupération des arguments en ligne de commande
    # -----------------------------------------------
    parser = argparse.ArgumentParser(description='Jeu de bataille navale')
    parser.add_argument('--console','-c', action="store_true", dest="console", default=False, help="Interface console")
    parser.add_argument('--tkinter','-t', action="store_true", dest="tkinter", default=False, help="Interface tkinter")
    parser.add_argument('--web', '-w', action="store_true", dest="web", default=False, help="Interface web (serveur)")
    options = parser.parse_args()

    # Lancement de l'interface
    # ------------------------
    if options.console :
        from bn_console import *
        app = MainConsole()
    elif options.tkinter :
        from bn_tkinter import *
        app = MainTK()
    elif options.web :
        from bn_webserveur import *
        launch_serveur()

    # Si pas d'option, un petit menu
    else :
        print("""Choix de l'interface :
  T : Tkinter
  C : Console
  W : Web (serveur)""")
        choix = input("Votre choix ([t]|c|w) : ")
        if choix.lower() == 'c' :
            from bn_console import *
            app = MainConsole()
        if choix.lower() == 'w' :
            from bn_webserveur import *
            launch_serveur()
        else :
            from bn_tkinter import *
            app = MainTK()
