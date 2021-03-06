#!/usr/bin/env python3

"""Module bn_grille

Implémente les classes :
    - Bateau : modélise un bateau
    - Grille : classe de base pour une grille
        - GrilleJoueur : dérivée de Grille, la grille où on place ses bateaux
        - GrilleSuivi : dérivée de Grille, la grille de suivi des coups

Auteur : Frédéric Muller

Licence CC BY-NC-SA

Version 0.1.0"""

import random as rand
from time import *

from bn_utiles import *

#
#----------------------------------------------------------------------------------------------------------------
#
class Bateau(object):
    """Classe pour définir les bateaux"""
    def __init__(self, taille, start, sens):
        """Un bateau est défini par :
            - Sa taille
            - Son point de départ (start)
            - Son sens (DROITE, GAUCHE, BAS, HAUT)
        On récupère les cases occupées par le bateau
        ainsi que les cases adjacentes"""

        self.taille = taille
        self.start = start
        self.sens = sens
        self.end = (self.start[0]+(self.taille-1)*self.sens[0] , self.start[1]+(self.taille-1)*self.sens[1])

        # Récupération des cases occupées par le bateau
        self.cases = []
        for k in range(taille):
            self.cases.append((self.start[0]+k*self.sens[0] , self.start[1]+k*self.sens[1]))

        # Récupération des cases adjacentes
        self.cases_adj = []
        self.cases_adj.append((self.start[0]-self.sens[0] , self.start[1]-self.sens[1]))
        self.cases_adj.append((self.end[0]+self.sens[0] , self.end[1]+self.sens[1]))
        for k in range(taille):
            self.cases_adj.append((self.cases[k][0]+self.sens[1] , self.cases[k][1]+self.sens[0]))
            self.cases_adj.append((self.cases[k][0]-self.sens[1] , self.cases[k][1]-self.sens[0]))
#
#----------------------------------------------------------------------------------------------------------------
#
class Grille(object):
    """Classe pour définir la grille de jeu"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        """Initialisation de la grille de jeu
        Les cases sont numérotées de 0 à (x|y)max-1"""
        # Liste des bateaux
        self.taille_bateaux_init = taille_bateaux[:]
        self.taille_bateaux = taille_bateaux[:]
        # Taille du plus grand et du plus petit bateau
        self.get_taille_max()
        self.get_taille_min()
        # Nombre de cases totales à toucher
        self.somme_tailles = sum(self.taille_bateaux)

        # Dimensions de la grille
        self.xmax = xmax
        self.ymax = ymax
        self.dimensions = (self.xmax, self.ymax)

        # État de chaque case : dictionnaire self.etat[case], où case = (i,j)
        #   1  : Contient un bateau
        #   -1 : Ne peut pas contenir de bateau, ou déjà joué et manqué
        #   0  : Case vide
        self.etat = {}

        # Liste des cases vides
        self.vides = []

        # Initialisation de la grille
        self.reinit()

    #
    # Gestion de la grille ---------------------------------------------
    #
    def reinit(self):
        """Réinitialisation de la grille"""
        self.etat = {}
        self.vide = []
        for i in range(self.xmax):
            for j in range(self.ymax):
                self.etat[(i,j)] = 0
                self.vides.append((i,j))

    def update_vides(self):
        """Met à jour la liste des cases vides"""
        self.vides = []
        for case in self.etat :
            if self.etat[case] == 0 :
                self.vides.append(case)

    def update(self):
        """Met à jour les paramètres de la grille"""
        self.update_vides()
        self.get_taille_max()
        self.get_taille_min()

    #
    # Gestion des cases ------------------------------------------------
    #
    def test_case(self, case):
        """Teste si une case est valide (dans la grille) et vide"""
        return 0 <= case[0] < self.xmax and 0 <= case[1] < self.ymax and self.etat[case] == 0

    def is_touche(self, case):
        """Teste si la case contient un bateau"""
        return self.etat[case] == 1

    def adjacent(self, case):
        """Retourne la liste des cases vides adjacentes à case
        dans l'ordre : DROITE, GAUCHE, HAUT, BAS"""
        adj = []
        for direction in [DROITE, GAUCHE, HAUT, BAS]:
            case_adj = (case[0]+direction[0] , case[1]+direction[1])
            if  self.test_case(case_adj):
                adj.append(case_adj)
        return adj

    def copie_grille_tmp(self):
        """Crée une copie temporaire de la grille"""
        grille_tmp = Grille(xmax=self.xmax, ymax=self.ymax, taille_bateaux=self.taille_bateaux)
        for case in self.etat :
            grille_tmp.etat[case] = self.etat[case]
        grille_tmp.taille_bateaux = self.taille_bateaux[:]
        grille_tmp.vides = self.vides
        return grille_tmp

    #
    # Gestion des espaces impossibles ----------------------------------
    #
    def get_max_space(self, case, direction=TOUTES_DIR, face=True):
        """Renvoie la plus grande place possible sur cette case
        dans une direction"""
        # face=False : ne compte qu'à droite ou en bas (pour l'IA)
        # car DROITE=HORIZONTAL et BAS=VERTICAL, donc obligé de spécifier
        if direction == TOUTES_DIR:
            return max(self.get_max_space(case, HORIZONTAL), self.get_max_space(case, VERTICAL))

        m = 1
        # Comptage des cases libres dans un seul sens
        x = case[0]
        y = case[1]
        while self.test_case((x+direction[0], y+direction[1])):
            m += 1
            x += direction[0]
            y += direction[1]
        if  face:
            # Comptage des cases libres sur toute une direction
            x = case[0]
            y = case[1]
            while self.test_case((x-direction[0], y-direction[1])):
                m += 1
                x -= direction[0]
                y -= direction[1]
        return m

    def elimine_cases(self):
        """Élimine les cases dans lesquelles
        le plus petit bateau ne peut pas rentrer"""
        self.get_taille_min()
        self.update_vides()
        cases_eliminees = []
        for case in self.vides :
            if 0 < self.get_max_space(case) < self.taille_min :
                self.etat[case] = -1
                cases_eliminees.append(case)
        self.update_vides()
        return cases_eliminees

    def elimine_cases_joueur(self):
        """Élimine les cases dans lesquelles
        le plus petit bateau ne peut pas rentrer
        Version pour le joueur"""
        # Dans la version pour le joueur on est obligé de marquer
        # temporairement les cases déjà touchées comme vides.
        # Ce problème n'apparaît pas dans la version pour l'algorithme
        # de résolution car il gère une file d'attente (les cases
        # touchées successives sont toujours adjacentes)
        # Dans la mesure où cette opération prend un petit peu de temps
        # elle n'est implémentée que pour le joueur
        self.get_taille_min()
        self.update_vides()
        cases_eliminees = []
        # On marque temporairement les cases touchées comme vides
        tmp_touchees = []
        for case in self.etat :
            if self.etat[case] == 1 :
                tmp_touchees.append(case)
                self.etat[case] = 0
        for case in self.vides :
            if 0 < self.get_max_space(case) < self.taille_min :
                self.etat[case] = -1
                cases_eliminees.append(case)
        # On remet les case touchées à leur état d'origine
        for case in tmp_touchees :
            self.etat[case] = 1
        self.update_vides()
        return cases_eliminees

    #
    # Gestion des tailles des bateaux ----------------------------------
    #
    def get_taille_max(self):
        """Met à jour la taille du bateau le plus grand restant"""
        if self.taille_bateaux :
            self.taille_max = max(self.taille_bateaux)
        else :
            self.taille_max = 0

    def get_taille_min(self):
        """Met à jour la taille du bateau le plus petit restant"""
        if self.taille_bateaux :
            self.taille_min = min(self.taille_bateaux)
        else :
            self.taille_min = 0

    def rem_bateau(self, taille):
        """Enlève le bateau de taille taille de la liste"""
        self.taille_bateaux.remove(taille)
        self.get_taille_max()
        self.get_taille_min()

    #
    # Gestion des bateaux sur la grille ------------------------------------
    #
    def test_bateau(self, bateau):
        """Test si le bateau est valide (rentre bien) dans la grille"""
        for case in bateau.cases :
            if not self.test_case(case):
                return False
        return True

    def get_possibles(self, affiche=False, tri=False):
        """Crée la liste des bateaux possibles démarrant sur chaque case
        ainsi que la liste des cases et directions possibles pour
        chaque bateau"""
        # tri : Trie les listes, pour les tests (mais perd un peu de temps)
        self.update_vides()

        # Liste des bateaux et sens possibles démarrant sur chaque case
        # Par ex {(0,0):[(5,(1,0)), (5,(0,1)),...], (0,1):...}
        self.possibles_case = {}
        for i in range(self.xmax):
            for j in range(self.ymax):
                self.possibles_case[(i,j)] = []

        # Récupère les éléments une seule fois de self.taille_bateaux,
        # triés en ordre décroissant si besoin
        if tri :
            tmp_taille_bateaux = sorted(list(set(self.taille_bateaux)), reverse=True)
        else :
            tmp_taille_bateaux = list(set(self.taille_bateaux))

        # Regarde pour chaque case vide la taille maxi d'un bateau dans chaque direction
        for case in self.vides :
            for direction in [DROITE, BAS] :
                tmax = self.get_max_space(case, direction=direction, face=0)
                self.possibles_case[case] += [(taille, direction) for taille in tmp_taille_bateaux if taille <= tmax]

        # Liste des cases de départ et sens possibles pour chaque bateau
        # Par ex : {5:[((0,0), (1,0)), ((0,0), (0,1)), ((1,0), (1,0)),...], 4:...}
        self.possibles = {}
        for taille in tmp_taille_bateaux :
            self.possibles[taille] = []
        for case in self.possibles_case :
            for placement in self.possibles_case[case]:
                self.possibles[placement[0]].append((case, placement[1]))
        if tri :
            for taille in self.taille_bateaux :
                self.possibles[taille].sort()

        if affiche : # Pour les tests
            for case in grille.vides :
                print(case,grille.possibles_case[case])
            print()
            for taille in grille.possibles :
                print("Taille %d :" % taille)
                print("-----------")
                i=1
                for pos in grille.possibles[taille] :
                    print(i,pos[0], pos[1])
                    i+=1
                print()

    def add_bateau(self, bateau):
        """Ajoute un bateau dans la grille
        et met à jour les états des cases adjacentes"""
        if self.test_bateau(bateau):
            for case in bateau.cases :
                self.etat[case] = 1
            for case in bateau.cases_adj:
                if self.test_case(case):
                    self.etat[case] = -1

    def add_bateau_alea(self, taille):
        """Ajoute un bateau aléatoire de taille donnée"""
        self.get_possibles()
        if not self.possibles[taille] :
            return False
        else :
            (case, direction) = rand.choice(self.possibles[taille])
            self.add_bateau(Bateau(taille, case, direction))
            return True

    def init_bateaux_alea(self):
        """Initialise une grille avec des bateaux aléatoires"""
        nb_bateaux = 0
        while nb_bateaux < len(self.taille_bateaux) :
            nb_bateaux = 0
            # Crée une grille temporaire sur laquelle on va essayer de placer les bateaux
            gtmp = self.copie_grille_tmp()
            for taille in self.taille_bateaux :
                if not gtmp.add_bateau_alea(taille) :
                    break # On est bloqué
                else :
                    gtmp.rem_bateau(taille)
                    nb_bateaux += 1
        self.etat = gtmp.etat

    #
    # Calculs de probabilités ------------------------------------------
    #
    def case_max_echantillons(self, nb_echantillons=100, affiche=False):
        """Calcul des probabilités sur chaque case vide de contenir
        un bateau. Retourne la case la plus probable en essayant
        différents arrangements des bateaux restants"""
        start=time()

        # Dictionnaire contenant les probas de chaque case
        self.probas = {}
        for i in range(self.xmax):
            for j in range(self.ymax):
                self.probas[(i,j)] = 0

        # On crée différents arrangements aléatoires de bateaux
        for k in range(nb_echantillons):
            # On utilise une grille temporaire, copiée à partir de la grille_suivi courante
            grille_tmp = self.copie_grille_tmp()
            # Arrangement aléatoire de bateaux et récupération des cases occupées
            grille_tmp.init_bateaux_alea()
            for case in grille_tmp.etat :
                if self.etat[case] == 0 and grille_tmp.etat[case] == 1 :
                    self.probas[case] += 1

        # Détermination de la case la plus probable
        case_max = (0,0)
        pmax = 0
        for case in self.probas :
            if self.probas[case] > pmax :
                pmax = self.probas[case]
                case_max = case

        # Affichages pour les tests
        if affiche :
            for j in range(self.ymax):
                for i in range(self.xmax-1):
                    print("%.4f"%(self.probas[(i,j)]), end=' ')
                print("%.4f"%self.probas[(self.xmax-1,j)])

            print()
            print("Échantillon de taille %d" % nb_echantillons)
            print("Temps : %.4f secondes" % (time()-start))
            print("Case max :", case_max)
            print("Proba max : %.5f" % pmax)

        # Retourne la case la plus probable et sa proba
        return (case_max, pmax)

    def case_max(self, affiche=False):
        """Détermine la case qui contient le plus de bateaux et
        regardant sur chaque case le nombre de bateaux possibles"""

        # Dictionnaire contenant les probas de chaque case
        self.probas = {}
        for i in range(self.xmax):
            for j in range(self.ymax):
                self.probas[(i,j)] = 0

        self.get_possibles()

        for taille in self.taille_bateaux :
            for (case, direction) in self.possibles[taille] :
                for k in range(taille) :
                    self.probas[(case[0]+k*direction[0], case[1]+k*direction[1])] += 1

        # Détermination de la case la plus probable
        self.case_proba = (0,0)
        self.pmax = 0
        for case in self.probas :
            if self.probas[case] > self.pmax :
                self.pmax = self.probas[case]
                self.case_proba = case

        # Affichages pour les tests
        if affiche :
            for j in range(self.ymax):
                for i in range(self.xmax-1):
                    print("%.4f"%(self.probas[(i,j)]), end=' ')
                print("%.4f"%self.probas[(self.xmax-1,j)])

            print()
            print("Temps : %.4f secondes" % (time()-start))
            print("Case max :", self.case_proba)
            print("Proba max : %.5f" % self.pmax)

        # Retourne la case la plus probable et sa proba
        return (self.case_proba, self.pmax)

    def case_max_touchee(self, case_touchee):
        """Retourne le nombre de bateaux possibles
        sur chaque case adjacentes à case (qui vient d'être touchée)"""
        # Sera appelé dans Ordi.shuffle_queue() pour trier la file quand on touche

        # On marque temporairement la case comme vide pour pouvoir tester si on peut y placer des bateaux
        self.etat[case_touchee] = 0

        self.get_possibles()
        probas = {}
        for case in self.adjacent(case_touchee) :
            probas[case] = 0

        for taille in self.taille_bateaux :
            for direction in [HORIZONTAL, VERTICAL] :
                # Bateau qui se termine sur case_touchee
                # On ajoute 1 à sa case à gauche, ou au-dessus
                if case_touchee[direction[1]]-(taille-1)*direction[direction[1]] >= 0 and \
                    ((case_touchee[0]-(taille-1)*direction[0], case_touchee[1]-(taille-1)*direction[1]), direction) in self.possibles[taille]:
                        probas[(case_touchee[0]-direction[0], case_touchee[1]-direction[1])] += 1
                # Bateau à cheval strictement sur case_touchee
                # On ajoute 1 à gauche et à droite, ou au-desus et en-dessous
                for k in range(1, taille-1) :
                    if case_touchee[direction[1]]-k*direction[direction[1]] >= 0 and \
                        ((case_touchee[0]-k*direction[0], case_touchee[1]-k*direction[1]), direction) in self.possibles[taille]:
                        probas[(case_touchee[0]-direction[0], case_touchee[1]-direction[1])] += 1
                        probas[(case_touchee[0]+direction[0], case_touchee[1]+direction[1])] += 1
                # Bateau qui démarre sur case_touchee
                # On ajoute 1 à droite, ou en-dessous
                if ((case_touchee[0], case_touchee[1]), direction) in self.possibles[taille]:
                        probas[(case_touchee[0]+direction[0], case_touchee[1]+direction[1])] += 1

        # On remet la case comme touchée
        self.etat[case_touchee] = 1

        # Retour des probas (en fait juste le nombre de bateaux possibles)
        probas_liste = [(case, probas[case]) for case in probas]
        return sorted(probas_liste, key=lambda proba: proba[1], reverse = True)

    def case_max_all(self, affiche_all=False):
        """Détermination de la case optimale par énumération de
        toutes les répartitions possibles de bateaux"""
        self.probas_all = {}
        for i in range(self.xmax):
            for j in range(self.ymax):
                self.probas_all[(i,j)] = 0

        gtmp = self.copie_grille_tmp()
        self.nb_repart = 0
        global start_iter, n_iter # Pour les tests
        start_iter = time()
        n_iter = 0
        self.make_all(gtmp, affiche_all)

        # Détermination de la case la plus probable
        case_max = (0,0)
        pmax = 0
        for case in self.probas_all :
            if self.probas_all[case] > pmax :
                pmax = self.probas_all[case]
                case_max = case

        return (case_max, pmax)

    def make_all(self, gtmp, affiche_all=False):
        """Crée toutes les répartitions possibles de bateaux
        de manière récursive"""
        # affiche_all : affiche toutes les grilles pendant leur création
        global start_iter, n_iter
        if len(gtmp.taille_bateaux) == 0 :
            self.nb_repart += 1
            if affiche_all :
                gtmp.affiche()
            for case in self.probas_all :
                if self.etat[case] == 0 and gtmp.etat[case] == 1 :
                    self.probas_all[case] +=1
            return

        if affiche_all :
            gtmp.get_possibles(tri=True)
        else :
            gtmp.get_possibles()

        taille = gtmp.taille_bateaux[0]
        for (case, direction) in gtmp.possibles[taille]:
            n_iter += 1
            #~ if n_iter % 10000 == 0 :
                #~ print(n_iter, time()-start_iter)
            gtmp2 = gtmp.copie_grille_tmp()
            gtmp2.add_bateau(Bateau(taille, case, direction))
            gtmp2.rem_bateau(taille)
            self.make_all(gtmp2, affiche_all)

    #
    # Fin de partie ----------------------------------------------------
    #
    def fini(self):
        """Renvoie True si tous les bateaux ont été coulés"""
        somme_touches = 0
        for case in self.etat :
            if self.etat[case] == 1 :
                somme_touches += 1
        return somme_touches == self.somme_tailles

    #
    # Affichage --------------------------------------------------------
    #

    def affiche(self):
        """Affiche la grille"""
        # Méthode à surcharger suivant l'interface
        # mais laissée ici pour les tests

        CAR_H=u'\u2500'     # Trait Horizontal
        CAR_V=u'\u2502'     # Trait Vertical
        # Coins
        CAR_CHG=u'\u250C'   # Coin Haut Gauche
        CAR_CHD=u'\u2510'   # Coin Haut Droite
        CAR_CBG=u'\u2514'   # Coin Bas Gauche
        CAR_CBD=u'\u2518'   # Coin Bas Droite
        # T
        CAR_TH=u'\u252C'    # T Haut
        CAR_TB=u'\u2534'    # T Bas
        CAR_TG=u'\u251C'    # T Gauche
        CAR_TD=u'\u2524'    # T Droite
        # +
        CAR_CX=u'\u253C'    # Croix centrale
        # Touché / Manqué
        CAR_TOUCH = u'\u2716' # ou u'\u2737', u'\u3718'
        CAR_MANQ = u'\u25EF'

        # Ligne du haut
        print('    '+CAR_CHG+(CAR_H*3+CAR_TH)*(self.xmax-1)+CAR_H*3+CAR_CHD)

        # Ligne des lettres des colonnes
        print('    '+CAR_V, end='')
        for i in range(self.xmax):
            if i!=self.xmax-1 :
                print(' '+str(i)+' ', end=CAR_V)
            else :
                print(' '+str(i)+' '+CAR_V)

        #Ligne sous les lettres
        print(CAR_CHG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)

        # Lignes suivantes
        for j in range(self.ymax):
            # 1ère colonne (chiffres des lignes)
            chaine = CAR_V+' '+str(j)+' '+CAR_V

            # Cases suivantes
            for i in range(self.xmax):
                if self.etat[(i,j)] == 1 :
                    symbole = CAR_TOUCH
                elif self.etat[(i,j)] == -1 :
                    symbole = CAR_MANQ
                else :
                    symbole = ' '
                chaine += ' '+symbole+' '+CAR_V
            print(chaine)

            # Sépartion lignes intermédiaires
            if j!=self.ymax-1 :
                print(CAR_TG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)

            # Dernière ligne
            else :
                print(CAR_CBG+(CAR_H*3+CAR_TB)*self.xmax+CAR_H*3+CAR_CBD)


# ---------------------------------------------------------------------------------------------------------------------------
# Les deux clases suivantes, héritées de Grille ont pour rôle de distinguer les fonctions spécifiques à chaque type de grille
# (Non utilisé pour l'instant)
# ---------------------------------------------------------------------------------------------------------------------------

class GrilleJoueur(Grille):
    """La grille sur laquelle chaque joueur place ses bateaux"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuivi(Grille):
    """La grille de suivi des coups joués"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#

# Différents tests
if __name__ == "__main__" :
    # Test de toutes les répartitions possibles de bateaux sur la grille
    grille = Grille(xmax=4, ymax=3, taille_bateaux=[2,3])

    launch_time = strftime("%d/%m/%Y %H:%M:%S",localtime(time()))
    print(launch_time)
    start = time()

    grille.case_max_all(affiche_all=True)

    print()
    print("Temps : %.2f seconde" % (time()-start))
    print("Nombre d'itérations : %d " % n_iter)
    print("Nombre de répartitions : %d " % grille.nb_repart)
    print()
    print("Début :", launch_time)
    print("Fin :", strftime("%d/%m/%Y %H:%M:%S",localtime(time())))
    print()
    for j in range(grille.ymax) :
        for i in range(grille.xmax-1):
            print(grille.probas_all[(i,j)], end=' ')
        i = grille.xmax-1
        print(grille.probas_all[(i,j)])
