#!/usr/bin/python3

"""Module bn_tkinter

Interface de jeu en mode graphique

Auteur : Frédéric Muller

Licence CC BY-NC-SA

Version 0.1.0"""

from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *
from tkinter.ttk import Combobox

from bn_utiles import *
from bn_grille import *
from bn_joueur import *

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
		
	def case2coord(self, i, j):
		"""Convertit les coordonnées de cases en coordonées de graphiques"""
		return (self.margeLeft+i*self.largCase, self.margeTop+j*self.largCase)
	
	def color_case(self, i, j, couleur):
		"""Colorie une case"""
		(x, y) = self.case2coord(i,j) 
		self.canvas.create_rectangle(x+1, y+1, x+self.largCase-1, y+self.largCase-1, fill=couleur)
	
	def marque_case(self, i, j, etat) :
		"""Marque une case touchée ou manquée"""
		(x, y) = self.case2coord(i,j) 
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
				self.marque_case(i, j, self.etat[(i,j)])
		
	def affiche_adverse(self, grille=None) :
		"""Affiche le canvas en coloriant les bateaux adverses""" 
		if not grille :
			grille = self
		self.clear_canvas()
		self.init_canvas()
		for i in range(self.xmax):
			for j in range(self.ymax):
				if grille.etat[(i,j)] == 1 :
					self.color_case(i, j, "cyan")
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.marque_case(i, j, self.etat[(i,j)])
	
	
#		
#----------------------------------------------------------------------------------------------------------------
#
class GrilleJoueurTK(GrilleJoueur, GrilleTK):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2], parent=None, cursor="arrow"):
		GrilleJoueur.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		GrilleTK.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux, parent=parent, cursor=cursor)
#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuiviTK(GrilleSuivi, GrilleTK):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2], parent=None, cursor="arrow"):
		GrilleSuivi.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		GrilleTK.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux, parent=parent, cursor=cursor)
#
#----------------------------------------------------------------------------------------------------------------
#



class JoueurTK(Joueur):
	def __init__(self, nom='Joueur', parent=None, cursor="arrow"):
		Joueur.__init__(self, nom=nom)
		self.grille_joueur = GrilleJoueurTK(parent=parent, cursor=cursor)
		self.grille_adverse = GrilleJoueurTK(parent=parent, cursor=cursor)
		self.grille_suivi = GrilleSuiviTK(parent=parent, cursor=cursor)
		self.parent = parent
		self.turn = True
		


#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiTK(Ordi, JoueurTK):
	def __init__(self, nom='HAL', niveau=5, nb_echantillons=100, seuil=20, parent=None, cursor="arrow"):
		Ordi.__init__(self, nom=nom, niveau=niveau, nb_echantillons=nb_echantillons, seuil=seuil)
		JoueurTK.__init__(self, nom=nom, parent=parent, cursor=cursor)

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
Niveau 2 : Tirs aléatoires uniforme et file d'attente
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
		self.parent.geometry("800x490")
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
		self.main_frame = Frame(self.parent, bg="black")
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
	
	def jeu_solo(self):
		def click_grille_solo(event):
			x, y = joueur.grille_suivi.canvas.canvasx(event.x), joueur.grille_suivi.canvas.canvasy(event.y)
			(i, j) = joueur.grille_suivi.coord2case(x,y)
			if joueur.turn and 0 <= i < joueur.grille_suivi.xmax and 0 <= j < joueur.grille_suivi.ymax :
				joueur.tire((i,j))
				info.delete('1.0', END)
				while joueur.messages :
					info.insert(END, joueur.messages.pop(0)+'\n')
				joueur.grille_suivi.affiche()
				if joueur.grille_suivi.fini() :
					info.insert(END, "Partie terminée en %d coups" % joueur.essais )
					messagebox.showinfo("Fin de partie", "Partie terminée en %d coups" % joueur.essais)
					joueur.turn = False
					
		self.parent.title("Bataille navale - Partie solo")
		self.parent.geometry("800x490")
		self.clear_widgets()
		
		grille = GrilleJoueurTK()
		grille.init_bateaux_alea()
		joueur = JoueurTK(parent=self.main_frame, cursor="X_cursor")
		joueur.grille_adverse = grille
		joueur.grille_suivi.pack(side=LEFT, padx=10, pady=10)
		joueur.grille_suivi.affiche()
		
		joueur.grille_suivi.canvas.bind("<Button-1>", click_grille_solo)
		
		info = ScrolledText(self.main_frame, wrap=WORD, padx=5, relief=RIDGE)
		info.pack(side=RIGHT, fill=Y, padx=10, pady=10)
		info.insert(END, "C'est parti !")
			
	def jeu_ordi(self) :
		def suivant(event) :
			if ordi.turn :
				ordi.coup_suivant()
				info.delete('1.0', END)
				while ordi.messages :
					info.insert(END, ordi.messages.pop(0)+'\n')
				ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
				if ordi.grille_suivi.fini() :
					info.insert(END, "Partie terminée en %d coups" % ordi.essais )
					messagebox.showinfo("Fin de partie", "Partie terminée en %d coups" % ordi.essais)
					ordi.turn = False
		
		level_win = LevelWindow(self.parent)
		self.parent.wait_window(level_win.window)
		niveau = level_win.lv_param['niveau']
		seuil = level_win.lv_param['seuil']
		nb_echantillons = level_win.lv_param['échantillons']
		titre = "Bataille navale - Résolution automatique - Niveau "
		if niveau == 4 :
			titre += "4(%d)" % nb_echantillons
		elif niveau == 6 :
			titre += "6(%d)" % seuil
		else :
			titre += "%d" % niveau
		self.parent.title(titre)
		self.parent.geometry("800x490")
		self.clear_widgets()
		frame_grille = Frame(self.main_frame, bg="black")
		frame_grille.pack(side=LEFT, fill=Y, padx=10, pady=5)
		
		grille = GrilleJoueurTK()
		grille.init_bateaux_alea()
		ordi = OrdiTK(parent=frame_grille, niveau=niveau, seuil=seuil, nb_echantillons=nb_echantillons)
		ordi.grille_adverse = grille
		ordi.grille_suivi.pack(side=TOP)
		ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
		
		info = ScrolledText(self.main_frame, wrap=WORD, padx=5)
		info.pack(side=RIGHT, fill=Y, padx=10, pady=10)
		info.insert(END, "C'est parti !")
		
		bt_next = Button(frame_grille, text="Coup suivant")
		bt_next.pack(side=BOTTOM)
		bt_next.bind("<Button-1>", suivant)
		self.parent.bind("<Return>", suivant)
		
	def jeu_contre_ordi(self):
		def click_grille(event):
			fini = False
			x, y = joueur.grille_suivi.canvas.canvasx(event.x), joueur.grille_suivi.canvas.canvasy(event.y)
			(i, j) = joueur.grille_suivi.coord2case(x,y)
			ok = joueur.grille_suivi.test_case( (i, j) )
			if joueur.turn and 0 <= i < joueur.grille_suivi.xmax and 0 <= j < joueur.grille_suivi.ymax :
				joueur.tire((i,j))
				info.delete('1.0', END)
				joueur.grille_suivi.affiche()
				if joueur.grille_suivi.fini() :
					gagnant = 0
					fini = True	
					joueur.add_message("Bravo ! Vous avez gagné en %d coups" % joueur.essais)
					joueur.turn = False
				else :
					if ok :
						ordi.coup_suivant()
						ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
						if ordi.grille_suivi.fini():
							ordi.add_message("L'ordinateur a gagné en %d coups" % ordi.essais)
							ordi.turn = False
							gagnant = 1
							fini = True
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
		
		
		level_win = LevelWindow(self.parent)
		self.parent.wait_window(level_win.window)
		niveau = level_win.lv_param['niveau']
		seuil = level_win.lv_param['seuil']
		nb_echantillons = level_win.lv_param['échantillons']
		titre = "Bataille navale - Partie contre l'ordinateur - Niveau "
		if niveau == 4 :
			titre += "4(%d)" % nb_echantillons
		elif niveau == 6 :
			titre += "6(%d)" % seuil
		else :
			titre += "%d" % niveau
		self.parent.title(titre)
		
		self.parent.geometry("980x620")
		self.clear_widgets()
		frame_grilles = Frame(self.main_frame, bg="black")
		frame_grille1 = Frame(frame_grilles, bg="black")
		frame_grille1.pack(side=LEFT, padx=10, pady=5)
		frame_grille2 = Frame(frame_grilles, bg="black")
		frame_grille2.pack(side=RIGHT, padx=10, pady=5)
		frame_grilles.pack(fill=X)
		
		grille_ordi = GrilleJoueurTK()
		grille_ordi.init_bateaux_alea()
		grille_joueur = GrilleJoueurTK()
		grille_joueur.init_bateaux_alea()
		
		joueur = JoueurTK(parent=frame_grille1, cursor="X_cursor")
		ordi = OrdiTK(parent=frame_grille2, niveau=niveau, seuil=seuil, nb_echantillons=nb_echantillons)
		
		ordi.grille_joueur = grille_ordi
		ordi.grille_adverse = grille_joueur
		joueur.grille_joueur = grille_joueur
		joueur.grille_adverse = grille_ordi
		
		Label(frame_grille1, text=joueur.nom, bg="white",font=("Helvetica", 16) ,relief=RIDGE, padx=10, pady=5).pack(pady=10)
		Label(frame_grille2, text=ordi.nom, bg="white",font=("Helvetica", 16) ,relief=RIDGE, padx=10, pady=5).pack(pady=10)
		
		joueur.grille_suivi.pack(padx=10, pady=10)
		ordi.grille_suivi.pack(padx=10, pady=10)
		joueur.grille_suivi.affiche()
		ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
		
		joueur.grille_suivi.canvas.bind("<Button-1>", click_grille)
		
		info = ScrolledText(self.main_frame, wrap=WORD, padx=5)
		info.pack(side=BOTTOM, fill=X, padx=10, pady=10)
		info.insert(END, "C'est parti !")
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

if __name__ == "__main__":
	#~ root = Tk()
	
	#~ grille = GrilleTK(parent=root)
	#~ grille.init_bateaux_alea()
	#~ 
	#~ debug = ScrolledText(master=root)
	#~ debug.pack(side=RIGHT)
	#~ 
	#~ joueur = JoueurTK(parent=root)
	#~ joueur.grille_adverse = grille
	#~ joueur.grille_suivi.pack(side=LEFT)
	#~ joueur.grille_suivi.affiche_adverse(joueur.grille_adverse)
	
	
	#~ app = MainTK(root)
	app = MainTK()
	
	#~ root.mainloop()
