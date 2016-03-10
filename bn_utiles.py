#!/usr/bin/env python3

"""Module bn_utiles

Implémente les constantes et quelques fonctions utiles

Auteur : Frédéric Muller

Licence CC BY-NC-SA

Version 0.1.0"""

#
# Constantes ----------------------------------------------------------------------------------------------------
#
DROITE = HORIZONTAL = (1, 0)
GAUCHE = (-1, 0)
BAS = VERTICAL = (0, 1)
HAUT = (0, -1)
TOUTES_DIR = (1,1)

# source : http://patorjk.com/software/taag/
TITRE = """     ╔══════════════════════════════════════════════════════════════════╗     
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

             Projet de formation ISN 2015/2016 de l'académie de Lyon
                Auteur : Frédéric Muller
                Code du projet : https://github.com/Abunux/pyBatNav
                Licence Creative Common CC BY-NC-SA v4.0
                Projet démarré le 14/11/2015"""

#
# Fonctions utiles ----------------------------------------------------------------------------------------------
#

def signe(x):
    """Retourne le signe de x"""
    if x > 0 :
        return 1
    elif x < 0 :
        return -1
    else :
        return 0

def alpha(case):
    """Convertit les coordonnées de case en notation du jeu
    Par ex (2,3) devient "C3" """
    return chr(case[0]+65)+str(case[1])

def coord(case_alpha):
    """Convertit une case en coordonnées
    par ex "C3" devient (2,3)"""
    return (ord(case_alpha[0].upper())-65, int(case_alpha[1]))
