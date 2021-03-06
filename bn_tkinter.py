#!/usr/bin/env python3

"""Module bn_tkinter

Interface de jeu en mode graphique

Auteur : Frédéric Muller

Licence CC BY-NC-SA

Version 0.1.0"""

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from bn_utiles import *
from bn_grille import *
from bn_joueur import *

# Constantes de couleur (pas très esthétique mais facilement modifiable)
# ----------------------------------------------------------------------
COLOR_FOND     = "white"      # Fond de la frame principale
COLOR_NOIRE    = "#F8F8F8"    # Case "noire"
COLOR_BOAT     = "cyan"       # Case occupée par un bateau
COLOR_CURS     = "#D0D0D0"    # Case sous le curseur
COLOR_OK       = "#00FF00"    # Case valide
COLOR_NO       = "#FF0000"    # Case non valide
COLOR_QUEUE_M  = "yellow"     # File d'attente manqué
COLOR_QUEUE_T  = "orange"     # File d'attente touché
COLOR_COURANTE = "#FF00FF"    # Case courante

#~ FONT = "Helvetica"
FONT = "Verdana"

#
#----------------------------------------------------------------------------------------------------------------
#

class GrilleTK(Grille, Frame):
    """Crée un widget pour afficher et gérer les grilles"""
    def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2], parent=None, cursor="arrow"):
        Grille.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        Frame.__init__(self, parent)

        self.marge_left = 30
        self.marge_top = 30
        self.largeur_case = 40
        self.can_width = 1.5*self.marge_left+self.xmax*self.largeur_case
        self.can_height = height=1.5*self.marge_top+self.ymax*self.largeur_case
        self.canvas = Canvas(self, width=self.can_width, height=self.can_height, bg="white", highlightthickness=0, cursor=cursor)
        self.canvas.pack()

    def coord2case(self, x, y) :
        """Convertit les coordonnées graphiques en coordonées de cases"""
        return (int((x-self.marge_left)//self.largeur_case), int((y-self.marge_top)//self.largeur_case))

    def case2coord(self,case):
        """Convertit les coordonnées de cases en coordonées de graphiques"""
        return (self.marge_left+case[0]*self.largeur_case, self.marge_top+case[1]*self.largeur_case)

    def init_canvas(self):
        """Dessin initial de la grille"""
        for i in range(self.xmax+1) :
            self.canvas.create_line(self.marge_left, self.marge_top+i*self.largeur_case, self.marge_left+self.xmax*self.largeur_case, self.marge_top+i*self.largeur_case)
        for i in range(self.ymax+1) :
            self.canvas.create_line(self.marge_left+i*self.largeur_case, self.marge_top, self.marge_left+i*self.largeur_case, self.marge_top+self.ymax*self.largeur_case)
        for i in range(self.xmax):
            self.canvas.create_text(self.marge_left/2, self.marge_top+i*self.largeur_case+self.largeur_case/2, text=str(i), font=(FONT, 12))
        for i in range(self.xmax):
            self.canvas.create_text(self.marge_left+i*self.largeur_case+self.largeur_case/2, self.marge_top/2, text=chr(i+65), font=(FONT, 12))

    def clear_canvas(self):
        """Réinitialise le canvas"""
        self.canvas.delete("all")
        self.init_canvas()
        
    def text_case(self, case, symbole):
        """Met un symbole dans une case"""
        (x, y) = self.case2coord(case)
        self.canvas.create_text(x+self.largeur_case/2, y+self.largeur_case/2, text=symbole, font=(FONT, 12))

    def marque_case(self, case) :
        """Marque une case touchée ou manquée"""
        (x, y) = self.case2coord(case)
        a = 0.3
        if self.etat[case] == 1 :
            self.canvas.create_line(x+a*self.largeur_case, y+a*self.largeur_case, x+(1-a)*self.largeur_case, y+(1-a)*self.largeur_case, width=2)
            self.canvas.create_line(x+a*self.largeur_case, y+(1-a)*self.largeur_case, x+(1-a)*self.largeur_case, y+a*self.largeur_case, width=2)
        elif self.etat[case] == -1 :
            self.canvas.create_oval(x+a*self.largeur_case, y+a*self.largeur_case, x+(1-a)*self.largeur_case, y+(1-a)*self.largeur_case, width=2)

    def color_case(self, case, couleur):
        """Colorie une case"""
        (x, y) = self.case2coord(case)
        self.canvas.create_rectangle(x+1, y+1, x+self.largeur_case, y+self.largeur_case, width=0, fill=couleur)

    def color_noires(self) :
        """Colorie une case sur deux"""
        for i in range(self.xmax):
            for j in range(self.ymax):
                if (i+j) % 2 == 0 :
                    self.color_case((i, j), COLOR_NOIRE)

    def color_bateaux_adverse(self, grille=None) :
        """Colorie les bateaux adverse sur la grille"""
        if not grille :
            grille = self
        for i in range(self.xmax):
            for j in range(self.ymax):
                if grille.etat[(i,j)] == 1 :
                    self.color_case((i, j), COLOR_BOAT)

    def color_bateaux_coules(self, coules=[]):
        """Colorie les cases des bateaux coulés"""
        for case in coules :
            self.color_case(case, COLOR_BOAT)

    def marque_cases(self):
        """Marque toutes les cases de la grille suvant leur état"""
        for i in range(self.xmax):
            for j in range(self.ymax):
                self.marque_case((i, j))

    def affiche(self, coules=[]):
        """Affiche le canvas"""
        self.clear_canvas()
        self.color_noires()
        self.color_bateaux_coules(coules)
        self.marque_cases()

    def affiche_adverse(self, grille=None) :
        """Affiche le canvas en coloriant les bateaux adverses"""
        self.clear_canvas()
        self.color_noires()
        self.color_bateaux_adverse(grille)
        self.marque_cases()

#
#----------------------------------------------------------------------------------------------------------------
#

class GrilleJoueurTK(GrilleJoueur, GrilleTK):
    def __init__(self, xmax=10, ymax=10, taille_bateaux=[5, 4, 3, 3, 2], parent=None, cursor="arrow"):
        GrilleJoueur.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        GrilleTK.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux, parent=parent, cursor=cursor)

#
#----------------------------------------------------------------------------------------------------------------
#

class GrilleSuiviTK(GrilleSuivi, GrilleTK):
    def __init__(self, xmax=10, ymax=10, taille_bateaux=[5, 4, 3, 3, 2], parent=None, cursor="arrow"):
        GrilleSuivi.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
        GrilleTK.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux, parent=parent, cursor=cursor)

#
#----------------------------------------------------------------------------------------------------------------
#

class JoueurTK(Joueur):
    """Joueur en mode tkinter"""
    def __init__(self, nom='Joueur', parent=None, cursor="arrow"):
        Joueur.__init__(self, nom=nom)
        # Container où afficher les grilles
        self.parent = parent
        self.grille_joueur = GrilleJoueurTK(parent=parent, cursor=cursor)
        self.grille_adverse = GrilleJoueurTK(parent=parent, cursor=cursor)
        self.grille_suivi = GrilleSuiviTK(parent=parent, cursor=cursor)

        self.turn = True        # Si c'est au tour de joueur de jouer (pour une évolution à deux joueurs humains)
        self.playable = True    # Si c'est possible de jouer

        try :
            self.info = self.parent.children["info"]
        except :
            pass

        self.grille_suivi.canvas.bind("<Button-1>", self.click_grille)
        self.grille_suivi.canvas.bind("<Motion>", self.move_on_grille)

    def click_grille(self, event):
        """Quand on clique sur la grille, joue un coup"""
        x, y = self.grille_suivi.canvas.canvasx(event.x), self.grille_suivi.canvas.canvasy(event.y)
        (i, j) = self.grille_suivi.coord2case(x, y)
        if self.playable and self.turn and self.grille_suivi.test_case((i,j)):
            self.joue_coup(i,j)
            self.grille_suivi.marque_case((i, j))

    def move_on_grille(self, event):
        """Quand le curseur se déplace sur la grille, coloration de la case survolée"""
        if self.playable :
            x, y = self.grille_suivi.canvas.canvasx(event.x), self.grille_suivi.canvas.canvasy(event.y)
            (i, j) = self.grille_suivi.coord2case(x, y)
            # Effaçage de la précédente case surlignée
            self.grille_suivi.affiche(self.coules)
            # Coloriage de la case survolée
            if self.grille_suivi.test_case((i,j)):
                self.grille_suivi.color_case((i, j), COLOR_CURS)
                self.grille_suivi.marque_case((i, j))

    def joue_coup(self, i, j):
        """Joue un coup"""
        if 0 <= i < self.grille_suivi.xmax and 0 <= j < self.grille_suivi.ymax :
            self.tire((i,j))
            self.grille_suivi.affiche(self.coules)
            self.affiche_messages()
            if self.grille_suivi.fini() :
                self.playable = False
                self.info.insert(END, "Partie terminée en %d coups" % self.essais )
                self.grille_suivi.affiche_adverse(self.grille_adverse)
                messagebox.showinfo("Fin de partie", "Partie terminée en %d coups" % self.essais)

    def affiche_messages(self, filtre=False):
        """Affiche la liste des messages"""
        if filtre :
            self.filtre_messages()
        self.info.delete('1.0', END)
        while self.messages :
            self.info.insert(END, self.messages.pop(0)+'\n')

    def place_bateaux(self) :
        """Place les bateaux du joueur"""
        place_win = PlaceWindow(self.parent)
        place_win.window.transient(self.parent)
        place_win.window.grab_set()
        self.parent.wait_window(place_win.window)
        if place_win.termine :
            for bateau in place_win.bateaux :
                self.grille_joueur.add_bateau(bateau)
        else :
            messagebox.showinfo("", "Placement aléatoire de vos bateaux")
            self.grille_joueur.init_bateaux_alea()

#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiTK(Ordi, JoueurTK):
    """Ordinateur en mode tkinter"""
    def __init__(self, nom='HAL', niveau=5, nb_echantillons=100, seuil=20, parent=None, cursor="arrow"):
        Ordi.__init__(self, nom=nom, niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)
        JoueurTK.__init__(self, nom=nom, parent=parent, cursor=cursor)

        self.playable = False
        try:
            self.info = self.parent.master.children["info"]
        except:
            pass

    def get_niveau(self) :
        """Règlage du niveau de l'algorithme"""
        level_win = LevelWindow(self.parent)
        level_win.window.transient(self.parent)
        level_win.window.grab_set()
        self.parent.wait_window(level_win.window)
        self.niveau = level_win.lv_param['niveau']
        self.seuil = level_win.lv_param['seuil']
        self.nb_echantillons = level_win.lv_param['échantillons']
        if self.niveau == 4 :
            self.niveau_str = "4(%d)" % self.nb_echantillons
        elif self.niveau == 6 :
            self.niveau_str = "6(%d)" % self.seuil
        else :
            self.niveau_str = "%d" % self.niveau

    def click_suivant(self, event=None) :
        """Quand on clic pour le coup suivant"""
        if self.turn :
            self.coup_suivant()
            self.grille_suivi.affiche_adverse(self.grille_adverse)
            # Colorie les cases de la file d'attente
            k = 1
            for case in self.queue :
                if self.grille_adverse.etat[case] == 1 :
                    self.grille_suivi.color_case(case, COLOR_QUEUE_T)
                else :
                    self.grille_suivi.color_case(case, COLOR_QUEUE_M)
                self.grille_suivi.text_case(case, str(k))
                k += 1
                  
            self.grille_suivi.color_case(self.case_courante, COLOR_COURANTE)
            self.grille_suivi.marque_case(self.case_courante)
            self.affiche_messages()
            if self.grille_suivi.fini() :
                self.info.insert(END, "Partie terminée en %d coups" % self.essais )
                messagebox.showinfo("Fin de partie", "Partie terminée en %d coups" % self.essais)
                self.grille_suivi.affiche_adverse(self.grille_adverse)
                self.turn = False

#
#----------------------------------------------------------------------------------------------------------------
#

# Non utilisé
#~ class PartieTK(Partie):
    #~ def __init__(self, joueur=Joueur(), adversaire=Ordi(), cheat=False, parent=None):
        #~ Partie.__init__(self, joueur=joueur, adversaire=adversaire, cheat=cheat)
        #~ self.parent = parent

#----------------------------------------------------------------------------------------------------------------
#                               Fenêtres graphiques
#----------------------------------------------------------------------------------------------------------------

class LevelWindow(object):
    """Fenêtre de configuration du niveau de l'algorithme"""
    def __init__(self, parent):
        # Dictionnaire contenant les paramètres
        self.lv_param={}
        self.lv_param['niveau'] = 5
        self.lv_param['seuil'] = 60
        self.lv_param['échantillons'] = 100

        # Initialisation et création de la fenêtre
        self.window = Toplevel(parent)
        self.window.geometry("580x160")
        self.window.title("Paramètres")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.valide)
        self.window.bind("<Return>", self.valide)

        Label(self.window,text="Niveau de l'algorithme",font=(FONT, 16)).pack(pady=5)

        self.frame_param = Frame(self.window)
        self.frame_param.pack(fill=BOTH, padx=10, pady=10)

        # Choix du niveau
        self.cb_lv = Combobox(self.frame_param, values=["Niveau 1", "Niveau 2", "Niveau 3", "Niveau 4", "Niveau 5", "Niveau 6"], state="readonly")
        self.cb_lv.pack(side=LEFT)
        self.cb_lv.current(4)
        self.cb_lv.bind("<<ComboboxSelected>>", self.on_cb_change)

        # Paramètres supplémentaires
        self.lb_param = Label(self.frame_param, text="")
        self.txt_param = Text(self.frame_param, height=1, width=6)
        self.txt_param.insert(END, "0")

        # Informations sur les niveaux
        self.infos_niveaux = ["Niveau 1 : Que des tirs aléatoires uniformes sans file d'attente",
                              "Niveau 2 : Tirs aléatoires uniformes et file d'attente",
                              "Niveau 3 : Tirs aléatoires sur les cases noires et file d'attente",
                              "Niveau 4 : Optimisation par des échantillons",
                              "Niveau 5 : Optimisation par nombre de bateaux local",
                              "Niveau 6 : Optimisation par énumération de tous les arrangements à partir d'un seuil"]
        frame_infos = Frame(self.window)
        frame_infos.pack(fill=X)
        self.lb_info = Label(frame_infos, justify=LEFT,  pady=5)
        self.lb_info['text'] = self.infos_niveaux[self.cb_lv.current()]
        self.lb_info.pack(side=LEFT, padx=10)

        Button(self.window, text="Valider", command=self.valide).pack(side=BOTTOM, pady=5)

    def on_cb_change(self, event=None) :
        """Quand on change le niveau"""
        self.cb_lv.selection_clear()
        niveau = self.cb_lv.current()+1
        self.lv_param['niveau'] = niveau
        self.lb_info['text'] = self.infos_niveaux[self.cb_lv.current()]

        # Pour les niveaux 4 et 6, paramètres supplémentaires
        if niveau == 4 :
            self.lb_param['text'] = "Échantillons : "
            self.txt_param.delete('1.0', END)
            self.txt_param.insert(END, "100")
            self.lb_param.pack(side=LEFT, padx=10)
            self.txt_param.pack(side=LEFT)
        elif niveau == 6 :
            self.lb_param['text'] = "Seuil : "
            self.txt_param.delete('1.0', END)
            self.txt_param.insert(END, "60")
            self.lb_param.pack(side=LEFT, padx=10)
            self.txt_param.pack(side=LEFT)
        else :
            self.lb_param.pack_forget()
            self.txt_param.pack_forget()

    def valide(self, event=None):
        """Validation des paramètres"""
        self.lv_param['seuil'] = int(self.txt_param.get('1.0', END)[:-1])
        self.lv_param['échantillons'] = int(self.txt_param.get('1.0', END)[:-1])
        self.window.destroy()

#
#----------------------------------------------------------------------------------------------------------------
#

class PlaceWindow(object):
    """Fenêtre de placement des bateaux"""
    def __init__(self, parent, taille_bateaux=[5, 4, 3, 3, 2]):
        self.parent = parent
        self.window = Toplevel(self.parent, bg="white")
        self.window.title("Placement de vos bateaux")
        self.window.resizable(False, False)
        self.lb_titre = Label(self.window, text="", bg="white", font=(FONT, 16))
        self.lb_titre.pack(fill=X)

        self.bateaux = []
        self.taille_bateaux = taille_bateaux[:]

        joueur = JoueurTK(parent=self.parent)
        self.grille = GrilleJoueurTK(parent=self.window)
        self.grille.pack()
        self.grille.affiche()

        self.bt_close = Button(self.window, text="Fermer cette fenêtre et \nplacer les bateaux aléatoirement", command = self.window.destroy)
        self.bt_close.pack(padx=10, pady=10)

        self.next_bateau()

        self.grille.canvas.bind("<Button-1>", self.on_clic)
        self.grille.canvas.bind("<Motion>", self.on_move)

        self.termine = False        # Si tous les bateaux ont été placés
        self.first_clic = True     # Clique au départ du bateau

    def test_case_depart(self, case):
        """Teste si le bateau en cours est plaçable à partir de cette case"""
        if not self.grille.test_case(case) :
            return False
        for sens in [HAUT, BAS, GAUCHE, DROITE] :
            if self.grille.test_bateau(Bateau(self.current_taille, case, sens)) :
                return True
        return False

    def next_bateau(self) :
        """Place le bateau suivant ou quitte"""
        if self.taille_bateaux :
            self.current_taille = self.taille_bateaux.pop(0)
            self.lb_titre['text'] = "Placement du bateau de taille %d" % self.current_taille
        else :
            self.termine = True
            self.window.destroy()

    def on_clic(self, event) :
        """Quand on clique sur une case"""
        x, y = self.grille.canvas.canvasx(event.x), self.grille.canvas.canvasy(event.y)
        (i, j) = self.grille.coord2case(x, y)
        # Premier clic, on marque la case de départ
        if self.first_clic :
            self.case_depart = (i,j)
            self.end_possibles = []
            if self.test_case_depart((i,j)) :
                self.grille.color_case((i, j), COLOR_BOAT)
                for sens in [HAUT, BAS, GAUCHE, DROITE] :
                    bateau = Bateau(self.current_taille, (i,j), sens)
                    if self.grille.test_bateau(bateau) :
                        self.end_possibles.append(bateau.end)
                        self.grille.color_case(bateau.end, COLOR_OK)
                self.first_clic = False
        # Deuxième clic, on crée le bateau
        else :
            if (i,j) not in self.end_possibles :
                return
            if   i>self.case_depart[0] and j==self.case_depart[1] : sens = DROITE
            elif i<self.case_depart[0] and j==self.case_depart[1] : sens = GAUCHE
            elif j>self.case_depart[1] and i==self.case_depart[0] : sens = BAS
            elif j<self.case_depart[1] and i==self.case_depart[0] : sens = HAUT

            bateau = Bateau(self.current_taille, self.case_depart, sens)
            self.bateaux.append(bateau)
            self.grille.add_bateau(bateau)
            self.grille.affiche_adverse()
            self.next_bateau()

            self.first_clic = True

    def on_move(self, event):
        """Déplacement du curseur sur la grille"""
        x, y = self.grille.canvas.canvasx(event.x), self.grille.canvas.canvasy(event.y)
        (i, j) = self.grille.coord2case(x, y)
        if 0 <= i < self.grille.xmax and 0 <= j < self.grille.ymax :
            # Pas de bateau en cours de création, on colorie les cases possibles ou non
            if self.first_clic :
                self.grille.affiche_adverse()
                if self.test_case_depart((i,j)) :
                    couleur = COLOR_OK
                else :
                    couleur = COLOR_NO
                self.grille.color_case((i, j), couleur)
                self.grille.marque_case((i, j))
            # Case de fin du bateau, on crée un apperçu
            else :
                if   i>self.case_depart[0] and j==self.case_depart[1] : sens = DROITE
                elif i<self.case_depart[0] and j==self.case_depart[1] : sens = GAUCHE
                elif j>self.case_depart[1] and i==self.case_depart[0] : sens = BAS
                elif j<self.case_depart[1] and i==self.case_depart[0] : sens = HAUT
                if (i,j) in self.end_possibles :
                    bateau = Bateau(self.current_taille, self.case_depart, sens)
                    for case in bateau.cases :
                        self.grille.color_case(case, COLOR_BOAT)
                else :
                    self.grille.affiche_adverse()
                    self.grille.color_case(self.case_depart, COLOR_BOAT)
                    for case in self.end_possibles :
                        self.grille.color_case(case, COLOR_OK)
        # Si on bouge en dehors de la grille
        else :
            self.grille.affiche_adverse()
            if not self.first_clic :
                self.grille.color_case(self.case_depart, COLOR_BOAT)
                for case in self.end_possibles :
                    self.grille.color_case(case, COLOR_OK)

#
#----------------------------------------------------------------------------------------------------------------
#

class MainTK(Frame):
    """Fenêtre principale"""
    def __init__(self):
        # Initialisation de la fenêtre principale
        root = Tk()
        self.parent = root
        Frame.__init__(self, self.parent, bg="white")
        self.parent.title("Bataille navale")
        self.parent.resizable(False, False)
        self.parent.geometry("980x490")
        self.pack()

        # Barre de menu
        self.menubar = Menu(self)
        self.newmenu = Menu(self.menubar, tearoff=0)
        self.newmenu.add_command(label="Partie solo", command=self.jeu_solo)
        self.newmenu.add_command(label="Résolution automatique", command=self.jeu_ordi)
        self.newmenu.add_command(label="Partie contre l'ordinateur", command=self.jeu_contre_ordi)
        self.newmenu.add_separator()
        self.newmenu.add_command(label="Quitter", command=self.quit)
        self.menubar.add_cascade(label="Nouvelle partie", menu=self.newmenu)

        self.parent.config(menu=self.menubar)

        # Frame principale
        self.main_frame = Frame(self.parent, name="main_frame", bg=COLOR_FOND)
        self.main_frame.pack(fill=BOTH, expand=1)
        self.main_frame.update()

        # Fond d'écran avant le lancement d'une partie (on pourrait mettre une image)
        width_main_frame, height_main_frame = self.main_frame.winfo_width(), self.main_frame.winfo_height()
        can_fond = Canvas(self.main_frame, width=width_main_frame, height=height_main_frame, bg="white")
        can_fond.pack(fill=BOTH)
        can_fond.create_text(width_main_frame//2, height_main_frame//2,
            text=TITRE, font=("Courier", 10))

        root.mainloop()

    def clear_widgets(self):
        """Vide tous les widgets de la frame principale"""
        for widj in self.main_frame.pack_slaves() :
            widj.destroy()

    def jeu_solo(self) :
        """Lance une partie solo"""
        # Création de la frame principale
        self.parent.title("Bataille navale - Partie solo")
        self.parent.geometry("980x490")
        self.clear_widgets()

        info = Text(self.main_frame, name="info", wrap=WORD,  bd=5, relief=RIDGE, padx=5)

        joueur = JoueurTK(parent=self.main_frame)
        joueur.grille_adverse.init_bateaux_alea()
        joueur.grille_suivi.pack(side=LEFT, padx=10, pady=10)
        joueur.grille_suivi.affiche()

        info.pack(side=RIGHT, fill=Y, padx=10, pady=10)
        info.insert(END, "C'est parti !\n")

    def jeu_ordi(self) :
        """Lance une résolution automatique"""
        # Création de la frame principale
        self.parent.geometry("980x490")
        self.clear_widgets()
        frame_grille = Frame(self.main_frame, bg=COLOR_FOND)
        frame_grille.pack(side=LEFT, fill=Y, padx=10, pady=5)

        info = Text(self.main_frame, name="info", wrap=WORD, bd=5, relief=RIDGE, padx=5)
        info.pack(side=RIGHT, fill=Y, padx=10, pady=10)

        ordi = OrdiTK(parent=frame_grille)
        ordi.grille_adverse.init_bateaux_alea()
        ordi.grille_suivi.pack(side=TOP)
        ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)

        bt_next = Button(frame_grille, text="Coup suivant")
        bt_next.pack(side=BOTTOM)
        bt_next.bind("<Button-1>", ordi.click_suivant)
        self.parent.bind("<Return>", ordi.click_suivant)

        ordi.get_niveau()
        self.parent.title("Bataille navale - Résolution automatique - Niveau " + ordi.niveau_str)

        info.insert(END, "C'est parti !\n")

    def jeu_contre_ordi(self):
        """Lance une partie contre l'ordinateur"""
        def click_grille(event):
            """Déroulement du jeu, quand on clique sur la grille"""
            fini = False
            x, y = joueur.grille_suivi.canvas.canvasx(event.x), joueur.grille_suivi.canvas.canvasy(event.y)
            (i, j) = joueur.grille_suivi.coord2case(x,y)
            if joueur.turn and joueur.playable and joueur.grille_suivi.test_case((i,j)):
                joueur.tire((i,j))
                joueur.grille_suivi.affiche(coules=joueur.coules)
                if joueur.grille_suivi.fini() :
                    gagnant = 0
                    fini = True
                else :
                    ordi.coup_suivant()
                    ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
                    if ordi.grille_suivi.fini():
                        gagnant = 1
                        fini = True

                # Affichage des messages
                info.delete('1.0', END)
                joueur.filtre_messages()
                while joueur.messages :
                    info.insert(END, "<%s> %s\n" % (joueur.nom, joueur.messages.pop(0)))
                ordi.filtre_messages()
                while ordi.messages :
                    info.insert(END, "<%s> %s\n" % (ordi.nom, ordi.messages.pop(0)))

                # Fin de partie
                if fini :
                    # On ne peut plus cliquer sur la grille
                    joueur.playable = False
                    # Affichage de la solution
                    joueur.grille_suivi.affiche_adverse(ordi.grille_joueur)
                    ordi.grille_suivi.affiche_adverse(joueur.grille_joueur)
                    # Annoce du gagnant
                    if gagnant == 0 :
                        info.insert(END, "Bravo ! Vous avez gagné en %d coups" % joueur.essais)
                        joueur.turn = False
                        messagebox.showinfo("Fin de partie", "Bravo ! Vous avez gagné en %d coups" % joueur.essais)
                    else :
                        info.insert(END, "L'ordinateur a gagné en %d coups" % ordi.essais)
                        ordi.turn = False
                        messagebox.showinfo("Fin de partie", "L'ordinateur a gagné en %d coups" % ordi.essais)

        # -------------------------------
        # Création de la frame principale
        # -------------------------------
        self.parent.geometry("980x620")
        self.clear_widgets()

        frame_grilles = Frame(self.main_frame, bg=COLOR_FOND)
        frame_grille1 = Frame(frame_grilles, bg=COLOR_FOND)
        frame_grille1.pack(side=LEFT, padx=10, pady=5)
        frame_grille2 = Frame(frame_grilles, bg=COLOR_FOND)
        frame_grille2.pack(side=RIGHT, padx=10, pady=5)
        frame_grilles.pack(fill=X)

        info = Text(self.main_frame, name="info", wrap=WORD, bd=5, relief=RIDGE, padx=5)

        joueur = JoueurTK(parent=frame_grille1)
        ordi = OrdiTK(parent=frame_grille2)

        Label(frame_grille1, text=joueur.nom, bg="white",font=(FONT, 16) , padx=10, pady=5).pack()
        Label(frame_grille2, text=ordi.nom, bg="white",font=(FONT, 16) , padx=10, pady=5).pack()
        joueur.grille_suivi.pack(padx=10, pady=10)
        ordi.grille_suivi.pack(padx=10, pady=10)

        info.pack(side=BOTTOM, fill=X, padx=10, pady=10)

        joueur.grille_suivi.affiche()
        ordi.grille_suivi.affiche()

        # ------------------------------------
        # Initialisation des paramètres de jeu
        # ------------------------------------
        ordi.get_niveau()
        self.parent.title("Bataille navale - Partie contre l'ordinateur - Niveau " + ordi.niveau_str)

        joueur.place_bateaux()

        ordi.grille_joueur.init_bateaux_alea()
        ordi.grille_adverse = joueur.grille_joueur
        joueur.grille_adverse = ordi.grille_joueur

        joueur.grille_suivi.affiche()
        ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)

        joueur.grille_suivi.canvas.bind("<Button-1>", click_grille)

        # ----------------------
        # Lancement de la partie
        # ----------------------
        info.insert(END, "C'est parti !\n")
        # Le joueur commence
        if rand.randint(0,1) == 0 :
            messagebox.showinfo("Début de partie", "Vous allez commencer")
        # L'ordinateur commence
        else :
            messagebox.showinfo("Début de partie", "%s  va commencer" % ordi.nom)
            ordi.coup_suivant()
            ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
            ordi.filtre_messages()
            while ordi.messages :
                info.insert(END, "<%s> %s\n" % (ordi.nom, ordi.messages.pop(0)))

if __name__ == "__main__":
    app = MainTK()

