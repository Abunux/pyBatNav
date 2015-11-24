#
# Projet de bataille navale
# dans le cadre de la formation ISN
#
# Auteurs : Frédéric Muller et Lionel Reboul
#
# Projet démarré le 14/11/2015
# Dernière màj : 23/11/2015
# v 0.0.12
#
# Licence CC BY-NC-SA
#

import random as rand
import os
from math import * 
from time import *

#
#----------------------------------------------------------------------------------------------------------------
#
class Bateau :
    """Classe pour définir les bateaux"""
    # Constantes pour le sens (très pratiques)
    DROITE = (1, 0)
    GAUCHE = (-1, 0)
    BAS = (0, 1)
    HAUT = (0, -1)

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
        
        # Récupération des casses occupées par le bateau
        self.cases = []
        for k in range(taille) :
            self.cases.append((self.start[0]+k*self.sens[0] , self.start[1]+k*self.sens[1]))
        
        # Récupération des cases adjacentes
        self.cases_adj = []
        self.cases_adj.append((self.start[0]-self.sens[0] , self.start[1]-self.sens[1]))
        self.cases_adj.append((self.end[0]+self.sens[0] , self.end[1]+self.sens[1]))
        for k in range(taille) :
            self.cases_adj.append((self.cases[k][0]+self.sens[1] , self.cases[k][1]+self.sens[0]))
            self.cases_adj.append((self.cases[k][0]-self.sens[1] , self.cases[k][1]-self.sens[0]))
#
#----------------------------------------------------------------------------------------------------------------
#
class Grille(object):
    """Classe pour définir lea grille de jeu"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
        """Initialisation de la grille de jeu
        Les cases sont numérotées de 0 à (x|y)max-1"""
        # Liste des bateaux
        self.taille_bateaux = taille_bateaux[:]
        # Taille du plus grand et du plus petit bateau
        self.get_taille_max()
        self.get_taille_min()
        # Nombre de cases totales à toucher
        self.somme_tailles = sum(self.taille_bateaux)
        
        # Dimensions de la grille
        self.xmax = xmax
        self.ymax = ymax
        
        # État de chaque case : dictionnaire self.etat[case], où case = (i,j)
        #   1  : Contient un bateau
        #   -1 : Ne peut pas contenir de bateau, ou déjà joué et manqué
        #   0  : Case vide
        # Intérêts d'un dictionnaire par rapport à une liste double :
        #   - Plus facile à manipuler
        #   - Recherche plus efficace (table de hachage, donc recherche en O(1))
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
                
    def update_vides(self) :
        """Met à jour la liste des cases vides"""
        self.vides = []
        for i in range(self.xmax):
            for j in range(self.ymax):
                if self.etat[(i,j)] == 0 :
                    self.vides.append((i,j))
        
    def update(self):
        """Met à jour les paramètres de la grille"""
        self.update_vides()
        self.get_taille_max()
        self.get_taille_min()
    
    def fini(self):
        """Renvoie True si tous les bateaux ont été coulés"""
        somme_touches = 0
        for case in self.etat :
            if self.etat[case] == 1 :
                somme_touches += 1
        return somme_touches == self.somme_tailles
    
    #
    # Gestion des cases ------------------------------------------------
    #
    def test_case(self, case):
        """Test si une case est valide (dans la grille) et vide"""
        return 0 <= case[0] < self.xmax and 0 <= case[1] < self.ymax and self.etat[case] == 0
    
    def adjacent(self, case) :
        """Retourne la liste des cases vides adjacentes à case
        dans l'ordre : DROITE, GAUCHE, BAS, HAUT"""
        adj = []
        for d in [(1, 0), (-1, 0), (0, 1),  (0, -1)]:
            case_adj = (case[0]+d[0] , case[1]+d[1])
            if  self.test_case(case_adj):
                adj.append(case_adj)
        return adj
    
    def is_touche(self, case):
        """Test si la case contient un bateau"""
        return self.etat[case] == 1
    
    #
    # Gestion des espaces impossibles ----------------------------------
    #
    def elimine_cases(self):
        """Élimine les cases dans lesquelles le plus petit bateau ne peut pas rentrer"""
        self.get_taille_min()
        self.update_vides()
        for case in self.vides :
            if 0 < self.get_max_space(case) < self.taille_min :
                self.etat[case] = -1
        self.update_vides()

    def get_max_space_horizontal(self,case):
        """Renvoie la plus grande place vide horizontale sur cette case"""
        # Si la case contient déjà un bateau touché on le marque vide temporairement
        is_touchee = False
        if self.etat[case] == 1 :
            is_touchee = True
            self.etat[case] = 0
            
        m = 1
        # Comptage des cases à gauche
        x = case[0]
        while self.test_case((x-1,case[1])) :
            m += 1
            x -= 1
        # Comptage des cases à droite
        x = case[0]
        while self.test_case((x+1,case[1])) :
            m += 1
            x += 1
            
        if is_touchee :
            self.etat[case] = 1
        
        return m
    
    def get_max_space_vertical(self,case):
        """Renvoie la plus grande place vide horizontale sur cette case"""
        # Si la case contient déjà un bateau touché on le marque vide temporairement
        is_touchee = False
        if self.etat[case] == 1 :
            is_touchee = True
            self.etat[case] = 0
            
        m = 1
        # Comptage des cases en-dessous
        y = case[1]
        while self.test_case((case[0],y-1)) :
            m += 1
            y -= 1
        # Comptage des cases au-dessus
        y = case[1]
        while self.test_case((case[0],y+1)) :
            m += 1
            y += 1
        
        if is_touchee :
            self.etat[case] = 1
        
        return m
    
    def get_max_space(self,case):
        """Renvoie la plus grande place vide sur cette case"""
        return max(self.get_max_space_horizontal(case), self.get_max_space_vertical(case))
    
    #
    # Gestion des bateaux --------------------------------------------
    #
    def get_taille_max(self) :
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
    
    def test_bateau(self, bateau):
        """Test si le bateau est valide (rentre bien) dans la grille"""
        for case in bateau.cases :
            if not self.test_case(case) :
                return False
        return True
    
    def add_bateau(self,bateau):
        """Ajoute un bateau dans la grille
        et met à jour les état des cases adjacentes"""
        if self.test_bateau(bateau):
            for case in bateau.cases :
                self.etat[case] = 1
            for case in bateau.cases_adj :
                if self.test_case(case):
                    self.etat[case] = -1
                    
    def rem_bateau(self, taille):
        """Enlève le bateau de taille taille de la liste"""
        self.taille_bateaux.remove(taille)
        self.get_taille_max()
        self.get_taille_min()
        
    def make_bateau_alea(self, taille):
        """Crée un bateau aléatoire (pas forcément valide)"""
        x = rand.randint(0, self.xmax-1)
        y = rand.randint(0, self.ymax-1)
        sens = rand.choice([Bateau.DROITE, Bateau.GAUCHE, Bateau.HAUT, Bateau.BAS])
        bateau = Bateau(taille, (x,y), sens)
        return bateau
    
    def add_bateau_alea(self, taille):
        """Ajoute un bateau aléatoire (valide)"""
        bateau = self.make_bateau_alea(taille)
        while not self.test_bateau(bateau):
            bateau = self.make_bateau_alea(taille)
        self.add_bateau(bateau)
    
    def init_bateaux_alea(self):
        """Initialise une grille avec des bateaux aléatoires"""
        for taille in self.taille_bateaux :
            self.add_bateau_alea(taille)
    
    #
    # Affichage --------------------------------------------------------
    #
    def affiche(self):
        """Affiche la grille avec des caractère graphiques"""
        # Caractères pour faire la grille
        # -------------------------------
        # http://www.unicode.org/charts/
        # Traits
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
                print(' '+chr(i+65)+' ', end=CAR_V)
                #~ print(' '+str(i)+' ', end=CAR_V)
            else :
                print(' '+chr(i+65)+' '+CAR_V)
                #~ print(' '+str(i)+' '+CAR_V)
                
        #Ligne sous les lettres
        print(CAR_CHG+(CAR_H*3+CAR_CX)*self.xmax+CAR_H*3+CAR_TD)
        
        # Lignes suivantes
        for j in range(self.ymax):
            # 1ère colonne (chiffres des lignes)
            chaine = CAR_V+' '+str(j)+' '+CAR_V
            
            # Cases suivantes
            for i in range(self.xmax) :
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
    
    
#
#----------------------------------------------------------------------------------------------------------------
#
class Joueur:
    """Classe pour définir le joueur"""
    def __init__(self, nom=''):
        """Initialisation du joueur"""
        self.nom = nom
        self.grille_joueur = Grille()
        self.grille_adverse = Grille()
        self.grille_suivi = Grille()
        self.coups_joues = []
        self.essais = 0

    def tire(self, case):
        """Tire sur la case (x,y)
        Renvoie un tuple (booléen, string)
        où booléen = True si la case est touchée, False si non touché ou case invalide
        et la string est un message à afficher"""
        
        # Conversion de la colonne en lettre
        lettre = chr(case[0]+65)
        
        # Coup invalide
        if case in self.coups_joues :
            return (False, "%s%d : Déjà joué" %(lettre, case[1]))
        if not self.grille_suivi.test_case(case) :
            return (False, "%s%d : Coup invalide"%(lettre, case[1]))
            
        # Coup valide
        if self.grille_adverse.is_touche(case) :
            resultat = (True, "%s%d : Touché"%(lettre, case[1]))
            self.grille_suivi.etat[case] = 1
        else :
            resultat = (False, "%s%d : Manqué"%(lettre, case[1]))
            self.grille_suivi.etat[case] = -1
            
        # Mise à jour des paramètres du joueur et de la grille
        self.grille_suivi.update_vides()
        self.coups_joues.append(case)
        self.essais += 1
        
        return resultat
    

#
#----------------------------------------------------------------------------------------------------------------
#
if __name__== '__main__':
    """Programme principal"""
    #
    # Fonctions utiles -------------------------------------------------
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
#
#----------------------------------------------------------------------------------------------------------------
#
    def jeu_solo() :
        """Jeu solo sur une grille aléatoire"""
        # Initialisation de la partie
        grille = Grille()
        grille.init_bateaux_alea()
        joueur = Joueur()
        joueur.grille_adverse = grille
        message = "Début de partie"
        
        # Début de partie
        while not joueur.grille_suivi.fini():
            clear()
            joueur.grille_suivi.affiche()
            print(message)
            case = input('Coups (Entrée pour un coup aléatoire) : ')
            if case == '' :
                message = joueur.tire((rand.randint(0,joueur.grille_adverse.xmax-1), rand.randint(0,joueur.grille_adverse.ymax-1)))[1]
            else :
                try :
                    message = joueur.tire((ord(case[0])-65, int(case[1])))[1]
                except :
                    message = "%s : Coup invalide" % case

        # Fin de partie
        clear()
        joueur.grille_suivi.affiche()
        print("Bravo !! Partie terminée en %d coups" % joueur.essais)
#
#----------------------------------------------------------------------------------------------------------------
#
    def jeu_ordi(affiche = True) :
        """Résolution d'un grille aléatoire par l'ordinateur"""
        # --> Quelques améliorations possibles :
        #       - Tire au hasard : 
        #           - Tirer de manière plus large (suite à discrépence faible)
        #           - Utilisation de densités de probabilités sur chaque case pour cibler la case plus probable (hard)
        #
        # --> Encapsuler chaque étape dans une classe Ordi

        # Initialisation de la partie
        grille = Grille()
        grille.init_bateaux_alea()
        ordi = Joueur()
        ordi.grille_adverse = grille
        message = "Début de partie"
        
        # File d'attente des cases à tirer quand on touche une case
        queue = []
        # Liste des cases touchées sur un bateau
        liste_touches = []
        
        # Début de la partie
        while not ordi.grille_suivi.fini():
            # Affichages
            if affiche :
                clear()
                ordi.grille_suivi.affiche()
                info("Queue : ", queue)
                info("Liste touchés : ", liste_touches)
                info("Taille_bateaux : ", ordi.grille_suivi.taille_bateaux)
                info(message)
            
            # Si la queue est vide
            if not queue :
                # Si on vient de couler un bateau
                if liste_touches :
                    # On l'enlève de la liste des bateaux à couler
                    ordi.grille_suivi.rem_bateau(len(liste_touches))
                    # Mise à jour des cases adjacentes au bateau coulé (cases impossibles)
                    for case_touchee in liste_touches :
                        for case_impossible in ordi.grille_suivi.adjacent(case_touchee):
                            if ordi.grille_suivi.test_case(case_impossible) :
                                ordi.grille_suivi.etat[case_impossible] = -1
                    # Élimination des cases dans lesquelles le plus petit bateau restant ne peut pas rentrer
                    # et mise à jour de la grille
                    ordi.grille_suivi.elimine_cases()
                    
                # Pour l'instant, pas de case touchée
                liste_touches = []
                
                # Tire sur une case aléatoire : Une case sur 2 (cases noires de l'échiquier)
                #--> Points à améliorer :
                #   - Suite à discrépence faible (maximiser la surface couverte)
                #   - Utilisation de densités de probabilités sur chaque case pour cibler la plus probable
                case = rand.choice([(i,j) for (i,j) in ordi.grille_suivi.vides if (i+j)%2==0])
            
            # Si la queue n'est pas vide, on tire sur sa 1ère case qu'on enlève de la queue 
            else :
                case = queue.pop(0)
            
            # Tire sur la case
            (resultat, message) = ordi.tire(case)

            # Si on touche
            if resultat :
                # Si c'est la 1ère case du bateau
                if not liste_touches :
                    liste_touches = [case]
                    case_touchee = case # 1ère case touchée du bateau
                    
                    # On ajoute les case adjacentes possibles à la case, en ordre aléatoire :
                    # Récupération des cases adjacentes et de la taille du plus petit bateau restant
                    adj = ordi.grille_suivi.adjacent(case)
                    ordi.grille_suivi.get_taille_min()
                    # On teste si le bateau rentre horizontalement
                    if ordi.grille_suivi.get_max_space_horizontal(case) >= ordi.grille_suivi.taille_min :
                        for c in adj :
                            if c[1] == case[1] :
                                queue.append(c)
                    # On teste si le bateau rentre verticalement
                    if ordi.grille_suivi.get_max_space_vertical(case) >= ordi.grille_suivi.taille_min :
                        for c in adj :
                            if c[0] == case[0] :
                                queue.append(c)
                                
                    # On mélange la file d'attente pour ne pas que l'algo soit prévisible
                    rand.shuffle(queue)
                    
                # Sinon on détermine le sens du bateau et on met à jour la queue avec ses cases adjacentes
                # en enlevant celles qui ne sont pas dans la bonne direction
                else :
                    # Bateau horizontal :
                    if case[1] == case_touchee[1] :
                        # On enlève les cases en haut et en bas de la 1ére case touchée
                        if (case_touchee[0], case_touchee[1]-1) in queue :
                            queue.remove((case_touchee[0], case_touchee[1]-1))
                        if (case_touchee[0], case_touchee[1]+1) in queue :
                            queue.remove((case_touchee[0], case_touchee[1]+1))
                            
                        # Case adjacente à la nouvelle case touchée
                        # signe(case[0]-case_touchee[0]) permet savoir si la case adjacente est à droite ou à gauche
                        nv_case = (int(case[0] + signe(case[0]-case_touchee[0])) , case[1])
                        if ordi.grille_suivi.test_case(nv_case) :
                            queue.append(nv_case)
                            
                    # Bateau vertical :
                    if case[0] == case_touchee[0] :
                        # On enlève les cases à droite et à gauche de la 1ére case touchée
                        if (case_touchee[0]-1, case_touchee[1]) in queue :
                            queue.remove((case_touchee[0]-1, case_touchee[1]))
                        if (case_touchee[0]+1, case_touchee[1]) in queue :
                            queue.remove((case_touchee[0]+1, case_touchee[1]))
                            
                        # Case adjacente à la nouvelle case touchée
                        # signe(case[0]-case_touchee[0]) permet savoir si la case adjacente est en haut ou en bas
                        nv_case = (case[0] , int(case[1] + signe(case[1]-case_touchee[1])))
                        if ordi.grille_suivi.test_case(nv_case) :
                            queue.append(nv_case)
                            
                    # Mise à jour de la liste des cases touchées sur ce bateau
                    liste_touches.append(case)
                    
                # Si la taille du bateau qu'on est entrain de couler est la taille max des bateaux sur la grille, on arrête
                if len(liste_touches) == ordi.grille_suivi.taille_max :
                    queue = []
            
            # Si on a manqué et qu'on n'est pas entrain de couler un bateau,
            # on élimine les cases dans lesquelles le plus petit bateau restant
            # ne peut pas rentrer
            if not resultat and not queue :
                ordi.grille_suivi.elimine_cases()
            
            if affiche :
                input("Entrée pour continuer")
            
        # Fin de la partie
        if affiche :
            clear()
            ordi.grille_suivi.affiche()
            info("Partie terminée en %d coups" % ordi.essais)
            info("Grille de l'adversaire :")
            ordi.grille_adverse.affiche()
        return ordi.essais
#
#----------------------------------------------------------------------------------------------------------------
#

# Menu de lancement 
    print("""Choix du jeu :
  S : Solo
  O : Ordi 
  T : Test algo""")
    choix = input("--> [O|s|t] ")
    if choix.lower() == 's' :
        jeu_solo()
    elif choix.lower() == 't' :
        n = int(input("Nombre de répétitions : "))
        start = time()
        s = 0
        for k in range(n) :
            e = jeu_ordi(affiche=False)
            s += e
        print("Moyenne : %.2f"%(s/n))
        print("Temps moyen : %.5f secondes"%((time()-start)/n))
    else :
        jeu_ordi()
