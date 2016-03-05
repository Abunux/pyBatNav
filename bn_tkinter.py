#!/usr/bin/python3

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

# Constantes de couleur :
#~ COLOR_OK = "green"
COLOR_OK = "#00FF00"
#~ COLOR_NO = "red"
COLOR_NO = "#FF0000"
COLOR_BOAT = "cyan"
COLOR_CURS = "#E8E8E8"

# ---------------------------------------------------------------------------------------------------------------
# Classes héritées de celles de bn_grille et bn_joueur
# pour ajouter des fonctions graphiques ou modifier des fonctions existantes
# ---------------------------------------------------------------------------------------------------------------


class BateauTK(Bateau):
	def __init__(self, taille, start, sens):
		Bateau.__init__(self, taille, start, sens)
#
#----------------------------------------------------------------------------------------------------------------
#

class GrilleTK(Grille, Frame):
	"""Crée un widget pour afficher et gérer les grilles"""
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2], parent=None, cursor="arrow"):
		Grille.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		Frame.__init__(self, parent)
		
		self.margeLeft = 30
		self.margeTop = 30
		self.largCase = 40
		self.can_width = 1.5*self.margeLeft+self.xmax*self.largCase
		self.can_height = height=1.5*self.margeTop+self.ymax*self.largCase
		self.canvas = Canvas(self, width=self.can_width, height=self.can_height, bg="white", cursor=cursor)
		self.canvas.pack()
		
		
	def init_canvas(self):
		"""Dessin initial de la grille"""
		for i in range(self.xmax+1) :
			self.canvas.create_line(self.margeLeft, self.margeTop+i*self.largCase, self.margeLeft+self.xmax*self.largCase, self.margeTop+i*self.largCase)
		for i in range(self.ymax+1) :
			self.canvas.create_line(self.margeLeft+i*self.largCase, self.margeTop, self.margeLeft+i*self.largCase, self.margeTop+self.ymax*self.largCase)
		for i in range(self.xmax):
			self.canvas.create_text(self.margeLeft/2, self.margeTop+i*self.largCase+self.largCase/2, text=str(i), font=("Helvetica", 12))
		for i in range(self.xmax):
			self.canvas.create_text(self.margeLeft+i*self.largCase+self.largCase/2, self.margeTop/2, text=chr(i+65), font=("Helvetica", 12))
			
	def coord2case(self, x, y) :
		"""Convertit les coordonnées graphiques en coordonées de cases"""
		return (int((x-self.margeLeft)//self.largCase), int((y-self.margeTop)//self.largCase))
		
	def case2coord(self,case):
		"""Convertit les coordonnées de cases en coordonées de graphiques"""
		return (self.margeLeft+case[0]*self.largCase, self.margeTop+case[1]*self.largCase)
	
	def color_case(self, case, couleur):
		"""Colorie une case"""
		(x, y) = self.case2coord(case) 
		self.canvas.create_rectangle(x+1, y+1, x+self.largCase, y+self.largCase, width=0, fill=couleur)
	
	def marque_case(self, case, etat) :
		"""Marque une case touchée ou manquée"""
		(x, y) = self.case2coord(case) 
		if etat == 1 :
			symbole = "X"
		elif etat == -1 :
			symbole = "O"
		else :
			symbole = ""
		self.canvas.create_text(x+self.largCase/2, y+self.largCase/2, text=symbole, font=("Helvetica", 12))
	
	def clear_canvas(self):
		"""Efface le canvas"""
		self.canvas.delete("all")
	
	def affiche(self):
		"""Affiche le canvas"""
		self.clear_canvas()
		self.init_canvas()
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.marque_case((i, j), self.etat[(i,j)])
		
	def affiche_adverse(self, grille=None) :
		"""Affiche le canvas en coloriant les bateaux adverses""" 
		if not grille :
			grille = self
		self.clear_canvas()
		self.init_canvas()
		for i in range(self.xmax):
			for j in range(self.ymax):
				if grille.etat[(i,j)] == 1 :
					self.color_case((i, j), COLOR_BOAT)
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.marque_case((i, j), self.etat[(i,j)])
	
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
		
		self.turn = True		# Si c'est au tour de joueur de jouer
		self.playable = True	# Si c'est possible de jouer
		
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
		if self.playable and self.turn :
			self.joue_coup(i,j)
			self.grille_suivi.color_case((i, j), COLOR_CURS)
			self.grille_suivi.marque_case((i, j), self.grille_suivi.etat[(i,j)])
	
	def move_on_grille(self, event):
		"""Quand le curseur se déplace sur la grille, coloration de la case survolée"""
		if self.playable :
			x, y = self.grille_suivi.canvas.canvasx(event.x), self.grille_suivi.canvas.canvasy(event.y)
			(i, j) = self.grille_suivi.coord2case(x, y)
			self.grille_suivi.affiche()
			if  0 <= i < self.grille_suivi.xmax and 0 <= j < self.grille_suivi.ymax :
				self.grille_suivi.color_case((i, j), COLOR_CURS)
				self.grille_suivi.marque_case((i, j), self.grille_suivi.etat[(i,j)])
	
	def joue_coup(self, i, j):
		"""Joue un coup"""
		if 0 <= i < self.grille_suivi.xmax and 0 <= j < self.grille_suivi.ymax :
			self.tire((i,j))
			self.grille_suivi.affiche()
			self.affiche_messages()
			if self.grille_suivi.fini() :
				self.info.insert(END, "Partie terminée en %d coups" % self.essais )
				messagebox.showinfo("Fin de partie", "Partie terminée en %d coups" % self.essais)
				self.playable = False
		
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
			messagebox.showerror("Erreur", "Vous n'avez pas placé tous vos bateaux.\nPlacement aléatoire.")
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
		try :
			self.info = self.parent.master.children["info"]
		except :
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
		
	def click_suivant(self, event=None) :
		"""Quand on clic pour le coup suivant"""
		if self.turn :
			self.coup_suivant()
			self.grille_suivi.affiche_adverse(self.grille_adverse)
			self.affiche_messages()
			if self.grille_suivi.fini() :
				self.info.insert(END, "Partie terminée en %d coups" % self.essais )
				messagebox.showinfo("Fin de partie", "Partie terminée en %d coups" % self.essais)
				self.turn = False
	
#
#----------------------------------------------------------------------------------------------------------------
#

class PartieTK(Partie):
	def __init__(self, joueur=Joueur(), adversaire=Ordi(), cheat=False, parent=None):
		Partie.__init__(self, joueur=joueur, adversaire=adversaire, cheat=cheat)
		self.parent = parent
		
		


#----------------------------------------------------------------------------------------------------------------
#								Fenêtres graphiques
#----------------------------------------------------------------------------------------------------------------


class LevelWindow(object):
	"""Fenêtre de configuration du niveau de l'algorithme"""
	def __init__(self, parent):
		# Dictionnaire contenant les paramètres
		self.lv_param={}
		self.lv_param['niveau'] = 5
		self.lv_param['seuil'] = 0
		self.lv_param['échantillons'] = 100
		
		# Initialisation et création de la fenêtre
		self.window = Toplevel(parent)
		self.window.title("Paramètres")
		self.window.bind("<Return>", self.valide)
		
		Label(self.window,text="Paramètres de l'algorithme",font=("Helvetica", 16)).pack()
		
		self.frame_param = Frame(self.window)
		self.frame_param.pack(fill=BOTH, padx=10, pady=10)
		
		self.cb_lv = Combobox(self.frame_param, values=["Niveau 1", "Niveau 2", "Niveau 3", "Niveau 4", "Niveau 5", "Niveau 6"], state="readonly")
		self.cb_lv.pack(side=LEFT)
		self.cb_lv.current(4)
		self.cb_lv.bind("<<ComboboxSelected>>", self.on_cb_change)
		
		self.lb_param = Label(self.frame_param, text="")
		self.txt_param = Text(self.frame_param, height=1, width=6)
		self.txt_param.insert(END, "0")
		
		Label(self.window, bg="white", justify=LEFT, bd = 5, padx=5, pady=5, relief=RIDGE,
				text="""Niveau 1 : Que des tirs aléatoires uniformes sans file d'attente
Niveau 2 : Tirs aléatoires uniformes et file d'attente
Niveau 3 : Tirs aléatoires sur les cases noires et file d'attente
Niveau 4 : Optimisation par des échantillons
Niveau 5 : Optimisation par nombre de bateaux local
Niveau 6 : Optimisation par énumération de tous les arrangements à partir d'un seuil""").pack(padx=10, pady=10)
		
		Button(self.window, text="OK", command=self.valide).pack()
	
	def on_cb_change(self, event=None) :
		"""Quand on change le niveau"""
		niveau = self.cb_lv.current()+1
		self.lv_param['niveau'] = niveau
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

class PlaceWindow(object):
	"""Fenêtre de placement des bateaux"""
	def __init__(self, parent, taille_bateaux=[5, 4, 3, 3, 2]):
		self.parent = parent
		self.window = Toplevel(self.parent)
		self.window.title("Placement de vos bateaux")
		
		self.lb_titre = Label(self.window, text="", bg="white", font=("Helvetica", 16))
		self.lb_titre.pack(fill=X)
		
		self.bateaux = []
		self.taille_bateaux = taille_bateaux[:]
		
		joueur = JoueurTK(parent=self.parent)
		self.grille = GrilleJoueurTK(parent=self.window)
		self.grille.pack()
		self.grille.affiche()
		
		self.next_bateau()
		
		self.grille.canvas.bind("<Button-1>", self.on_click)
		self.grille.canvas.bind("<Motion>", self.on_move)
		
		self.termine = False		# Si tous les bateaux ont été placés
		self.first_click = True		# Clique au départ du bateau
		
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
		
	def on_click(self, event) :
		"""Quand on clique sur une case"""
		x, y = self.grille.canvas.canvasx(event.x), self.grille.canvas.canvasy(event.y)
		(i, j) = self.grille.coord2case(x, y)
		# Premier clic, on marque la case de départ
		if self.first_click :
			self.case_depart = (i,j)
			self.end_possibles = [] 
			if self.test_case_depart((i,j)) :
				self.grille.color_case((i, j), COLOR_BOAT)
				for sens in [HAUT, BAS, GAUCHE, DROITE] :
					bateau = Bateau(self.current_taille, (i,j), sens)
					if self.grille.test_bateau(bateau) :
						self.end_possibles.append(bateau.end)
						self.grille.color_case(bateau.end, COLOR_OK)
				self.first_click = False
		# Deuxième clic, on crée le bateau
		else :
			if (i,j) not in self.end_possibles :
				return
			if   i>self.case_depart[0] : sens = DROITE
			elif i<self.case_depart[0] : sens = GAUCHE
			elif j>self.case_depart[1] : sens = BAS
			elif j<self.case_depart[1] : sens = HAUT
			
			bateau = Bateau(self.current_taille, self.case_depart, sens)
			self.bateaux.append(bateau)
			self.grille.add_bateau(bateau)
			self.grille.affiche_adverse()
			self.next_bateau()
				
			self.first_click = True
				
	def on_move(self, event):
		"""Déplacement du curseur sur la grille"""
		x, y = self.grille.canvas.canvasx(event.x), self.grille.canvas.canvasy(event.y)
		(i, j) = self.grille.coord2case(x, y)
		if 0 <= i < self.grille.xmax and 0 <= j < self.grille.ymax :
			# Pas de bateau en cours de création, on colorie les cases possibles ou non
			if self.first_click : 
				self.grille.affiche_adverse()
				if self.test_case_depart((i,j)) :
					couleur = COLOR_OK
				else :
					couleur = COLOR_NO
				self.grille.color_case((i, j), couleur)
				self.grille.marque_case((i, j), self.grille.etat[(i,j)])
			# Case de fin du bateau, on crée un apperçu
			else :
				if   i>self.case_depart[0] : sens = DROITE
				elif i<self.case_depart[0] : sens = GAUCHE
				elif j>self.case_depart[1] : sens = BAS
				elif j<self.case_depart[1] : sens = HAUT
				if (i,j) in self.end_possibles :
					bateau = Bateau(self.current_taille, self.case_depart, sens)
					for case in bateau.cases :
						self.grille.color_case(case, COLOR_BOAT)
				else :
					self.grille.affiche_adverse()
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
		#~ self.aboutmenu = Menu(self.menubar, tearoff=0)
		#~ self.aboutmenu.add_command(label
			
		self.parent.config(menu=self.menubar)
		
		# Frame principale
		self.main_frame = Frame(self.parent, name="main_frame", bg="black")
		self.main_frame.pack(fill=BOTH, expand=1)
		self.main_frame.update()
		
		# Fond d'écran avant le lancement d'une partie
		width_main_frame, height_main_frame = self.main_frame.winfo_width(), self.main_frame.winfo_height()
		can_fond = Canvas(self.main_frame, width=width_main_frame, height=height_main_frame, bg="white")
		can_fond.pack(fill=BOTH)
		can_fond.create_text(width_main_frame//2, height_main_frame//2, 
			text="""     ╔══════════════════════════════════════════════════════════════════╗
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
                Licence Creative Common CC BY-NC-SA
                Projet démarré le 14/11/2015
		""", 
			font=("Courier", 10))
		
		root.mainloop()

	def clear_widgets(self):
		"""Vide tous les widgets de la frame principale"""
		for widj in self.main_frame.pack_slaves() :
			widj.destroy()

	def jeu_solo(self) :
		"""Lance une partie solo"""
		self.parent.title("Bataille navale - Partie solo")
		self.parent.geometry("980x490")
		self.clear_widgets()
		info = Text(self.main_frame, name="info", wrap=WORD, padx=5, relief=RIDGE)
		joueur = JoueurTK(parent=self.main_frame)#, cursor="X_cursor")
		joueur.grille_adverse.init_bateaux_alea()
		joueur.grille_suivi.pack(side=LEFT, padx=10, pady=10)
		joueur.grille_suivi.affiche()
		info.pack(side=RIGHT, fill=Y, padx=10, pady=10)
		info.insert(END, "C'est parti !\n")

	def jeu_ordi(self) :
		"""Lance une résolution automatique"""
		self.parent.geometry("980x490")
		self.clear_widgets()
		frame_grille = Frame(self.main_frame, bg="black")
		frame_grille.pack(side=LEFT, fill=Y, padx=10, pady=5)
		
		info = Text(self.main_frame, name="info", wrap=WORD, padx=5)
		
		ordi = OrdiTK(parent=frame_grille)
		ordi.grille_adverse.init_bateaux_alea()
		ordi.grille_suivi.pack(side=TOP)
		ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
		
		info.pack(side=RIGHT, fill=Y, padx=10, pady=10)
		
		bt_next = Button(frame_grille, text="Coup suivant")
		bt_next.pack(side=BOTTOM)
		bt_next.bind("<Button-1>", ordi.click_suivant)
		self.parent.bind("<Return>", ordi.click_suivant)
		
		ordi.get_niveau()		
		titre = "Bataille navale - Résolution automatique - Niveau "
		if ordi.niveau == 4 :
			titre += "4(%d)" % ordi.nb_echantillons
		elif ordi.niveau == 6 :
			titre += "6(%d)" % ordi.seuil
		else :
			titre += "%d" % ordi.niveau
		self.parent.title(titre)
		
		info.insert(END, "C'est parti !\n")
		
	def jeu_contre_ordi(self):
		"""Lance une partie contre l'ordinateur"""
		def click_grille(event):
			"""Déroulement du jeu, quand on clique sur la grille"""
			fini = False
			x, y = joueur.grille_suivi.canvas.canvasx(event.x), joueur.grille_suivi.canvas.canvasy(event.y)
			(i, j) = joueur.grille_suivi.coord2case(x,y)
			ok = joueur.grille_suivi.test_case( (i, j) )
			if joueur.turn and joueur.playable and 0 <= i < joueur.grille_suivi.xmax and 0 <= j < joueur.grille_suivi.ymax :
				joueur.tire((i,j))
				info.delete('1.0', END)
				joueur.grille_suivi.affiche()
				if joueur.grille_suivi.fini() :
					gagnant = 0
					fini = True	
					joueur.add_message("Bravo ! Vous avez gagné en %d coups" % joueur.essais)
					joueur.turn = False
					joueur.playable = False
					joueur.grille_suivi.affiche_adverse(ordi.grille_joueur)
					ordi.grille_suivi.affiche_adverse(joueur.grille_joueur)
				else :
					if ok :
						ordi.coup_suivant()
						ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
						if ordi.grille_suivi.fini():
							gagnant = 1
							fini = True
							ordi.add_message("L'ordinateur a gagné en %d coups" % ordi.essais)
							ordi.turn = False
							joueur.playable = False
							joueur.grille_suivi.affiche_adverse(ordi.grille_joueur)
							ordi.grille_suivi.affiche_adverse(joueur.grille_joueur)
				joueur.filtre_messages()
				while joueur.messages :
					info.insert(END, "<%s> %s\n" % (joueur.nom, joueur.messages.pop(0)))
				ordi.filtre_messages()
				while ordi.messages :
					info.insert(END, "<%s> %s\n" % (ordi.nom, ordi.messages.pop(0)))
				if fini and gagnant == 0 :
					messagebox.showinfo("Fin de partie", "Bravo ! Vous avez gagné en %d coups" % joueur.essais)
				elif fini and gagnant == 1 :
					messagebox.showinfo("Fin de partie", "L'ordinateur a gagné en %d coups" % ordi.essais)
		
		self.parent.geometry("980x620")
		self.clear_widgets()
		
		frame_grilles = Frame(self.main_frame, bg="black")
		frame_grille1 = Frame(frame_grilles, bg="black")
		frame_grille1.pack(side=LEFT, padx=10, pady=5)
		frame_grille2 = Frame(frame_grilles, bg="black")
		frame_grille2.pack(side=RIGHT, padx=10, pady=5)
		frame_grilles.pack(fill=X)
		
		info = Text(self.main_frame, name="info", wrap=WORD, padx=5)
		
		joueur = JoueurTK(parent=frame_grille1)
		ordi = OrdiTK(parent=frame_grille2)
		
		Label(frame_grille1, text=joueur.nom, bg="white",font=("Helvetica", 16) ,relief=RIDGE, padx=10, pady=5).pack(pady=10)
		Label(frame_grille2, text=ordi.nom, bg="white",font=("Helvetica", 16) ,relief=RIDGE, padx=10, pady=5).pack(pady=10)
		joueur.grille_suivi.pack(padx=10, pady=10)
		ordi.grille_suivi.pack(padx=10, pady=10)
		
		info.pack(side=BOTTOM, fill=X, padx=10, pady=10)
		
		joueur.grille_suivi.affiche()
		ordi.grille_suivi.affiche()
		
		ordi.get_niveau()
		titre = "Bataille navale - Partie contre l'ordinateur - Niveau "
		if ordi.niveau == 4 :
			titre += "4(%d)" % ordi.nb_echantillons
		elif ordi.niveau == 6 :
			titre += "6(%d)" % ordi.seuil
		else :
			titre += "%d" % ordi.niveau
		self.parent.title(titre)
			
		joueur.place_bateaux()
		
		ordi.grille_joueur.init_bateaux_alea()
		ordi.grille_adverse = joueur.grille_joueur
		joueur.grille_adverse = ordi.grille_joueur
		
		joueur.grille_suivi.affiche()
		ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
		
		joueur.grille_suivi.canvas.bind("<Button-1>", click_grille)
		
		info.insert(END, "C'est parti !\n")
		
		if rand.randint(0,1) == 0 :
			#~ joueur.turn = True
			messagebox.showinfo("Début de partie", "Vous allez commencer")
		else :
			#~ joueur.turn = False
			messagebox.showinfo("Début de partie", "%s  va commencer" % ordi.nom)
			ordi.coup_suivant()
			ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
			ordi.filtre_messages()
			while ordi.messages :
				info.insert(END, "<%s> %s\n" % (ordi.nom, ordi.messages.pop(0)))
		
if __name__ == "__main__":
	app = MainTK()
	
