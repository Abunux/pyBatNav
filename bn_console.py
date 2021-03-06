#!/usr/bin/env python3

"""Module bn_console

Interface de jeu en mode console

Auteur : Frédéric Muller

Licence CC BY-NC-SA

Version 0.1.0"""

import os
from math import *
from time import *

from bn_grille import *
from bn_joueur import *
from bn_stats import *

# --------------------------------------------
# Caractères graphiques (pour faire la grille)
# --------------------------------------------

print("""
 Pour un affichage du jeu optimal, vous avez besoin de pouvoir
 afficher au moins 125 caractères par lignes. Sous Windows, clic droit
 sur la barre de titre du terminal, Propriétés et régler la largeur du
 tampon à 125.""")

# Le terminal Windows a des soucis avec Unicode (les caractères gras de la grille
# font planter le programme), aussi j'ai mis un jeu de caractères de secours.
print("""
 Ce programme peut afficher les grilles en caractères unicodes.
 En cas de problème d'affichage ou de plantage, il faut désactiver
 cette fonctionnalité.
 """)
uni = input("Voulez-vous utiliser les caractères Unicodes ([o]|n) ? ")

if uni.lower() != 'n' :
    UNI = True
    print("Caractères Unicodes activés\n")
    # http://www.unicode.org/charts/ --> Box Drawing (U2500.pdf)

    # Caractères simples pour la grille
    # ---------------------------------
    # Traits
    CAR_H = u'\u2500'       # Trait Horizontal : ─
    CAR_V = u'\u2502'       # Trait Vertical : │
    # Coins
    CAR_CHG = u'\u250C'     # Coin Haut Gauche : ┌
    CAR_CHD = u'\u2510'     # Coin Haut Droite : ┐
    CAR_CBG = u'\u2514'     # Coin Bas Gauche : └
    CAR_CBD = u'\u2518'     # Coin Bas Droite : ┘
    # T
    CAR_TH = u'\u252C'      # T Haut : ┬
    CAR_TB = u'\u2534'      # T Bas : ┴
    CAR_TG = u'\u251C'      # T Gauche : ├
    CAR_TD = u'\u2524'      # T Droite : ┤
    # +
    CAR_CX = u'\u253C'      # Croix Centrale : ┼

    # Caractères en gras pour les bateaux
    # -----------------------------------
    # Traits
    CAR_GH = u'\u2501'      # Trait Gras Horizontal : ━
    CAR_GV = u'\u2503'      # Trait Gras Vertical : ┃
    # T
    CAR_GTB = u'\u2537'     # T Gras Bas : ┷
    CAR_GTD = u'\u2528'     # T Gras Droite : ┨
    CAR_GTDH = u'\u252A'    # T Droite Haut : ┪
    CAR_GTDB = u'\u2529'    # T Droite Bas : ┩
    CAR_GTBG = u'\u253A'    # T Bas Gauche : ┺
    CAR_GTBD = u'\u2539'    # T Bas Droite : ┹

    # Coins
    CAR_GCBD = u'\u251B'    # Coin Gras Bas Droite : ┛
    # +
    CAR_GCXHG = u'\u2546'   # Croix Gras Haut Gauche : ╆
    CAR_GCXHD = u'\u2545'   # Croix Gras Haut Droite : ╅
    CAR_GCXBG = u'\u2544'   # Croix Gras Bas Gauche : ╄
    CAR_GCXBD = u'\u2543'   # Croix Gras Bas Droite : ╃
    CAR_GCX = u'\u254B'     # Croix Gras Centrale : ╋
    CAR_GCXH = u'\u253F'    # Croix Gras Horizontal : ┿
    CAR_GCXV = u'\u2542'    # Croix Gras Vertical : ╂

    # Touché / Manqué
    # ---------------
    CAR_TOUCH = u'\u2716'   # Touché : ✖
    CAR_MANQ = u'\u25EF'    # Manqué : ◯

else :
    UNI = False
    print("Caractères Unicodes désactivés\n")
    # Caractères de secours
    CAR_H = '-'
    CAR_V = '|'
    CAR_CHG = ' '
    CAR_CHD = ' '
    CAR_CBG = ' '
    CAR_CBD = ' '
    CAR_TH = ' '
    CAR_TB = ' '
    CAR_TG = ' '
    CAR_TD = ' '
    CAR_CX = '+'
    CAR_GH = '-'
    CAR_GV = '|'
    CAR_GTB = ' '
    CAR_GTD = ' '
    CAR_GTDH = ' '
    CAR_GTDB = ' '
    CAR_GTBG = ' '
    CAR_GTBD = ' '
    CAR_GCBD = ' '
    CAR_GCXHG = '+'
    CAR_GCXHD = '+'
    CAR_GCXBG = '+'
    CAR_GCXBD = '+'
    CAR_GCX = '+'
    CAR_GCXH = '+'
    CAR_GCXV = '+'
    CAR_TOUCH = 'x'
    CAR_MANQ =  'o'

#
# Fonctions utiles ----------------------------------------------------------------------------------------------
#

def clear():
    """Efface la console"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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
    """Affichage de la grille en mode console"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        Grille.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)

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
        """Crée la grille avec des caractères graphiques en entourant
        en gras les bateaux de la grille passée en paramètre"""
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
                #~ chaine += ' '+str(i)+' '+CAR_V          # Intitulés en chiffres des colonnes
            else :
                chaine += ' ' + chr(i+65) + ' ' + CAR_V + '\n'
                #~ chaine += ' '+str(i)+' '+CAR_V+'\n'

        # Ligne sous les lettres
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
        print(self.chaine)

    def affiche_adverse(self, grille=None):
        """Affiche la grille de suivi de l'adversaire
        en entourant nos propres bateaux"""
        print(self.make_chaine_adverse(grille))

#
#----------------------------------------------------------------------------------------------------------------
#

class GrilleJoueurC(GrilleC, GrilleJoueur):
    """La grille sur laquelle chaque joueur place ses bateaux"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        GrilleJoueur.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        GrilleC.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#

class GrilleSuiviC(GrilleC, GrilleSuivi):
    """La grille de suivi des coups joués"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        GrilleSuivi.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        GrilleC.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#

class JoueurC(Joueur):
    """Joueur en mode console"""
    def __init__(self, nom='Joueur'):
        Joueur.__init__(self, nom=nom)
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
        """Affiche les messages du joueur"""
        if affiche :
            print(boite('\n'.join(self.messages), prefixe="<%s> " % self.nom))
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
                    self.add_message("%s : Coup invalide" % case)
                    self.affiche_messages()

    #
    # Partie solo sur une grille aléatoire -----------------------------
    #
    def jeu_solo(self, cheat=True):
        """Lance une partie solo sur une grille aléatoire"""
        self.add_message("Début de partie")
        # Début de la partie
        while not self.grille_suivi.fini():
            # Affichages
            clear()
            if cheat :
                self.grille_suivi.affiche_adverse(self.grille_adverse)
            else :
                self.grille_suivi.affiche()

            self.affiche_messages()

            # Joue un coup
            self.joue_coup()

        # Fin de partie
        clear()
        self.grille_suivi.affiche_adverse(self.grille_adverse)
        self.add_message("Bravo !! Partie terminée en %d coups" % self.essais)
        self.affiche_messages()
        print("Coups joués : ", ' '.join([alpha(case) for case in self.cases_jouees]))

#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiC(JoueurC, Ordi):
    """Résoultion de la grille en mode console"""
    def __init__(self, nom='HAL', niveau=4, nb_echantillons=100, seuil=20):
        Ordi.__init__(self, nom=nom, niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)
        JoueurC.__init__(self, nom)

    def resolution(self, affiche=True, grille=None):
        """Lance la résolution de la grille par l'ordinateur"""
        # affiche : affichage ou non des printrmations (pour les tests)

        # Lancement du chrono
        start = time()
        self.add_message("C'est parti !!!")
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

        self.add_message("Partie terminée en %d coups" % self.essais)
        self.affiche_messages(affiche=affiche)

        # On renvoie de temps de résolution de la grille pour les tests de performance
        return time()-start

    def resolution_latex(self, affiche=True, grille=None):
        """Lance la résolution de la grille par l'ordinateur
        avec affichage en LaTeX pour copier-coller dans le rapport"""

        # Lancement du chrono
        start = time()
        self.add_message("C'est parti !!!")
        # C'est parti !!!
        while not self.grille_suivi.fini():
            if affiche :
                print(r"{\scriptsize")
                print(r"\begin{verbatim}")
                self.grille_suivi.affiche_adverse(grille)

            self.affiche_messages(affiche=affiche)
            print(r"\end{verbatim}}")
            print(r"\hrule")
            print()
            self.coup_suivant()

        # Fin de la partie
        if affiche :
            print(r"{\scriptsize")
            print(r"\begin{verbatim}")
            self.grille_suivi.affiche_adverse(grille)

        self.add_message("Partie terminée en %d coups" % self.essais)
        self.affiche_messages(affiche=affiche)
        print(r"\end{verbatim}}\hrule")
        # On renvoie de temps de résolution de la grille pour les tests de performance
        return time()-start
#
#----------------------------------------------------------------------------------------------------------------
#

class PartieC(Partie):
    """Partie à deux joueurs en mode console"""
    def __init__(self, joueur=Joueur(), adversaire=Ordi(), cheat=False):
        Partie.__init__(self, joueur=joueur, adversaire=adversaire, cheat=cheat)


    def add_bateau_joueur(self, taille):
        """Ajoute un bateau pour le joueur"""
        print("Placement du bateau de taille %d" % taille)

        case = input("Case de départ : ")
        try :
            case = coord(case)
        except :
            print("Saisie invalide")
            print()
            return False

        print("Direction :")
        print("  H : Haut")
        print("  B : Bas")
        print("  D : Droite")
        print("  G : Gauche")
        d = input("Direction : ")
        if d.upper() == 'H' :
            direction = HAUT
        elif d.upper() == 'B' :
            direction = BAS
        elif d.upper() == 'D' :
            direction = DROITE
        elif d.upper() == 'G' :
            direction = GAUCHE

        bateau = Bateau(taille, case, direction)

        return self.joueur.add_bateau(taille, case, direction)

    def place_bateaux_joueur(self):
        """Place tous les bateaux du joueur"""
        rep = input("Voulez-vous un placement aléatoire ([o]|n) ? ")
        if rep.lower() == 'n' :
            for taille in self.joueur.grille_joueur.taille_bateaux[::-1] :
                clear()
                print(boite("Placement de vos bateaux", larg_fen=0))
                self.joueur.grille_joueur.affiche_adverse()
                while not self.add_bateau_joueur(taille):
                    print("Le bateau de taille %d ne convient pas" % taille)
                    print()
        else :
            self.joueur.grille_joueur.init_bateaux_alea()

        for case in self.joueur.grille_joueur.etat :
            if self.joueur.grille_joueur.etat[case] == -1 :
                self.joueur.grille_joueur.etat[case] = 0

    #
    # Lancement de la partie -------------------------------------------
    #
    def affiche_grilles(self, fin=False):
        """Affiche les deux grilles cote à cote,
        avec les noms des joueurs"""
        clear()
        grille1 = self.joueur.chaine_nom
        # En fin de partie on affiche en gras les bateaux de l'adversaire
        # cheat permet de tricher en affichant les bateaux de l'adversaire (pour les tests)
        if fin or self.cheat :
            grille1 += self.joueur.grille_suivi.make_chaine_adverse(self.adversaire.grille_joueur)
        else :
            grille1 += self.joueur.grille_suivi.make_chaine()

        grille2 = self.adversaire.chaine_nom
        grille2 += self.adversaire.grille_suivi.make_chaine_adverse(self.joueur.grille_joueur)

        print(fusionne(grille1, grille2))

    def lance_partie(self):
        """Lance une partie à deux joueurs"""
        # Placement des bateaux
        self.place_bateaux_joueur()
        self.get_bateaux_adverse()
        self.adversaire.grille_adverse = self.joueur.grille_joueur
        clear()
        print(boite("Votre grille de jeu", larg_fen=0))
        self.joueur.grille_joueur.affiche_adverse()

        # Détermination du joueur qui commence
        joueur_en_cours = rand.randint(0,1)
        if  joueur_en_cours == 0 :
            print(boite("Vous allez commencer", larg_fen=0))
        else :
            print(boite("%s va commencer" % self.adversaire.nom, larg_fen=0))
        print()
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
        print()
        if self.joueur.grille_suivi.fini():
            print(boite("Bravo !! Vous avez gagné en %d coups" % self.joueur.essais))
        else :
            print(boite("%s a gagné en %d coups" % (self.adversaire.nom, self.adversaire.essais)))

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
    def get_niveau(self):
        """Demande le niveau de l'ordinateur"""
        ok = False
        while not ok :
            try :
                niveau = input("Niveau de l'algorithme (1|2|3|4|[5]|6) : ")
                if niveau not in ['1', '2', '3', '4', '5', '6'] or niveau == '':
                    niveau = 5
                else :
                    niveau = int(niveau)
                ok = True
            except :
                    print("Saisie invalide\n")
                    ok = False
        return niveau

    def get_nb_echantillons(self, niveau):
        """Pour le niveau 4, demande la taille des échantillons"""
        if niveau == 4 :
            ok = False
            while not ok :
                try :
                    nb_echantillons = int(input("Taille des échantillons : "))
                    ok = True
                except :
                    print("Saisie invalide\n")
                    ok = False
            return nb_echantillons
        else :
            return 100 # Cette valeur n'a aucune importance

    def get_seuil(self, niveau):
        """Pour le niveau 6, demande le seuil"""
        if niveau == 6 :
            ok = False
            while not ok :
                try :
                    seuil = int(input("Seuil : "))
                    ok = True
                except :
                    print("Saisie invalide\n")
                    ok = False
            return seuil
        else :
            return 20 # Cette valeur n'a aucune importance

    def jeu_ordi(self, affiche=True, xmax=10, ymax=10, taille_bateaux=[5,4,3,3,2], niveau=5, nb_echantillons=100, seuil=20):
        """Résolution d'une grille par l'ordinateur"""
        # Initialisation de la partie
        grille = GrilleJoueurC(xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        grille.init_bateaux_alea()
        ordi = OrdiC(niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)
        ordi.grille_adverse = grille
        ordi.grille_suivi = GrilleSuiviC(xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        ordi.grille_suivi.reinit()

        temps = ordi.resolution(affiche=affiche, grille=grille)
        return (ordi.essais, temps) # Pour les tests de performance

    def jeu_solo(self, cheat=False):
        """Jeu solo sur une grille aléatoire"""
        # Initialisation de la partie
        grille = GrilleJoueurC()
        grille.init_bateaux_alea()
        joueur = JoueurC()
        joueur.grille_adverse = grille
        joueur.jeu_solo(cheat=cheat)

    def jeu_contre_ordi(self, cheat=False, nom="Joueur"):
        """Partie en duel contre l'ordinateur"""
        # Initialisation de la partie
        joueur = JoueurC(nom)
        niveau = self.get_niveau()
        nb_echantillons = self.get_nb_echantillons(niveau)
        ordi = OrdiC(niveau=niveau, nb_echantillons=nb_echantillons)
        partie = PartieC(joueur, ordi, cheat=cheat)

    def test_algo(self, n=1000, xmax=10, ymax=10, taille_bateaux=[5,4,3,3,2], niveau=4, nb_echantillons=100, seuil=20):
        """Test de l'agorithme de résolution sur n parties
        et affichage des statistiques"""
        # Lancement de la simulation
        temps_resolution = 0
        distrib = [0]*(xmax*ymax+1)
        print("Lancement de la simulation : %s" % (strftime("%d/%m/%Y %H:%M:%S",localtime(time()))))
        start = time()
        for k in range(n):
            (essais, temps) = self.jeu_ordi(affiche=False, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux, niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)
            temps_resolution += temps
            distrib[essais] += 1
            # Affichage de l'avancement de la simulation
            if k==0 :
                print("Temps pour la 1ère simulation : %.2f seconde" % (time()-start))
                t_estime = (n-1)*(time()-start)
                print("Temps total estimé : %.2f secondes (%s)" % (t_estime, strftime("%d/%m/%Y %H:%M:%S",localtime(time()+t_estime))))
                print("(CTRL+C pour annuler la simulation)")
            if (k+1) % (n/10) == 0 :
                t_restant = (n-k-1)*(time()-start)/(k+1)
                print("Avancement : %d%% (Temps restant estimé : %.2f secondes (%s))" % (100*(k+1)//n, t_restant,strftime("%d/%m/%Y %H:%M:%S",localtime(time()+t_restant)) ))

        # Résultats de la simulation
        # --------------------------
        tmoy = temps_resolution/n

        # Nom de la simulation
        if niveau == 4 :
            niveau_str = "4(%d)" % nb_echantillons
        elif niveau == 6 :
            niveau_str = "6(%d)" % seuil
        else:
            niveau_str = "%d" % niveau
        filename = "distrib_HAL_niveau=%s_n=%d" % (niveau_str, n)

        # Calcul et affichage des statistiques
        stats = Stats(data=distrib, filename=filename, tmoy=tmoy, param_grille={'xmax':xmax, 'ymax':ymax, 'taille_bateaux':taille_bateaux}, niveau_str=niveau_str)

        print()
        print(boite("Résultats de la simulation", larg_fen=0))
        print()
        print("Dimensions de la grille : %d*%d" % (xmax , ymax))
        print("Liste des bateaux : %s" % str(taille_bateaux))
        print("Niveau de l'algorithme : %s" % niveau_str)
        print("Nombre de parties : %d" % n)
        print()
        print("Mini : %d" % stats.mini)
        print("Q1 : %d" % stats.quartiles[0])
        print("Med : %d" % stats.quartiles[1])
        print("Q3 : %d" % stats.quartiles[2])
        print("Maxi : %d" % stats.maxi)
        print()
        print("Mode : %d" % stats.mode)
        print()
        print("Moyenne : %.2f" % stats.moyenne)
        print("Sigma : %.2f" % stats.sigma)
        print()
        print("Temps moyen par partie : %.5f secondes" % (temps_resolution/n))
        print("Temps total            : %.2f secondes" % (time()-start))
        print()

        stats.save_data()
        stats.histogramme(save=True)

        return distrib # Pour tests futurs

    def launch_test_algo(self):
        """Lancement de la procédure de test
        de l'algorithme de résolution"""
        clear()
        xmax = ymax = 10
        taille_bateaux = [5, 4, 3, 3, 2]
        print(boite("Test de l'algorithme de résolution", larg_fen=0))
        print()
        # Paramètres des parties à simuler
        print("Paramètres par défaut : xmax=%d, ymax=%d, bateaux=%s" % (xmax, ymax, taille_bateaux))
        rep = input("Voulez-vous changer ces paramètres ? [o|[n]] ")
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
                    print("Saisie invalide\n")
                    ok = False
        niveau = self.get_niveau()
        nb_echantillons = self.get_nb_echantillons(niveau)
        seuil = self.get_seuil(niveau)

        ok = False
        while not ok :
            try :
                n = int(input("Nombre de parties : "))
                ok = True
            except :
                print("Saisie invalide\n")
                ok = False
        # Lancement du test
        self.test_algo(n=n, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux, niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)

    #
    # Menu de lancement ------------------------------------------------
    #
    def launch_menu(self):
        """Menu de lancement """
        defaut = self.launch_test_algo

        enter_to_continue()
        clear()

        print(TITRE)

        print()

        while True :
            enter_to_continue()
            clear()
            print(boite("Choix du jeu", larg_fen=0))
            print("""  J : Jeu contre l'ordinateur
  S : Jeu en solo sur une grille aléatoire
  O : Résolution d'une grille par l'ordinateur
  T : Test des performances de l'algorithme de résolution
  Q : Quitter
      """)
            choix = input("Votre choix (j|s|o|[t]|q) : ")

            if choix.lower() == 's' :
                rep = input("Activer le mode triche (o|[n]) ? ")
                if rep.lower() == 'o' :
                    self.jeu_solo(cheat=True)
                else :
                    self.jeu_solo(cheat=False)

            elif choix.lower() == 't' :
                self.launch_test_algo()

            elif choix.lower() == 'o' :
                niveau = self.get_niveau()
                nb_echantillons = self.get_nb_echantillons(niveau)
                seuil = self.get_seuil(niveau)
                self.jeu_ordi(niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)

            elif choix.lower() == 'j' :
                nom = input("Votre nom [Joueur] : ")
                if nom == '' :
                    nom = "Joueur"
                rep = input("Activer le mode triche (o|[n]) ? ")
                if rep.lower() == 'o' :
                    self.jeu_contre_ordi(cheat=True, nom=nom)
                else :
                    self.jeu_contre_ordi(cheat=False, nom=nom)

            elif choix.lower() == 'q' :
                print()
                print("Au revoir...")
                quit()

            # Par défaut
            else :
                defaut()

if __name__ == "__main__" :
    app = MainConsole()
