# Version 0.0.0

from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import *

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
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2], master=None):
		Grille.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		Frame.__init__(self, master)
		
		self.margeLeft = 30
		self.margeTop = 30
		self.largCase = 40
		self.can_width = 1.5*self.margeLeft+self.xmax*self.largCase
		self.can_height = height=1.5*self.margeTop+self.ymax*self.largCase
		self.canvas = Canvas(self, width=self.can_width, height=self.can_height)
		self.canvas.pack()
		
		
	def init_canvas(self):
		for i in range(self.xmax+1) :
			self.canvas.create_line(self.margeLeft, self.margeTop+i*self.largCase, self.margeLeft+self.xmax*self.largCase, self.margeTop+i*self.largCase)
		for i in range(self.ymax+1) :
			self.canvas.create_line(self.margeLeft+i*self.largCase, self.margeTop, self.margeLeft+i*self.largCase, self.margeTop+self.ymax*self.largCase)
		for i in range(self.xmax):
			self.canvas.create_text(self.margeLeft/2, self.margeTop+i*self.largCase+self.largCase/2, text=str(i), font=("Helvetica",12))
		for i in range(self.xmax):
			self.canvas.create_text(self.margeLeft+i*self.largCase+self.largCase/2, self.margeTop/2, text=chr(i+65), font=("Helvetica",12))
			
	def coord2case(self, x, y) :
		return (int((x-self.margeLeft)//self.largCase), int((y-self.margeTop)//self.largCase))
		
	def case2coord(self, i, j):
		return (self.margeLeft+i*self.largCase, self.margeTop+j*self.largCase)
	
	def color_case(self, i, j, couleur):
		(x, y) = self.case2coord(i,j) 
		self.canvas.create_rectangle(x+1, y+1, x+self.largCase-1, y+self.largCase-1, fill=couleur)
	
	def marque_case(self, i, j, etat) :
		(x, y) = self.case2coord(i,j) 
		if etat == 1 :
			symbole = "X"
		elif etat == -1 :
			symbole = "O"
		else :
			symbole = ""
		self.canvas.create_text(x+self.largCase/2, y+self.largCase/2, text=symbole, font=("Helvetica",12))
	
	def clear_canvas(self):
		self.canvas.delete("all")
	
	def affiche(self):
		self.clear_canvas()
		self.init_canvas()
		for i in range(self.xmax):
			for j in range(self.ymax):
				self.marque_case(i, j, self.etat[(i,j)])
		
	def affiche_adverse(self, grille=None) :
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
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleJoueur.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		GrilleTK.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuiviTK(GrilleSuivi, GrilleTK):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleSuivi.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
		GrilleTK.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)
#
#----------------------------------------------------------------------------------------------------------------
#



class JoueurTK(Joueur):
	def __init__(self, nom='Joueur', master=None):
		Joueur.__init__(self, nom=nom)
		self.grille_joueur = GrilleJoueurTK()
		self.grille_adverse = GrilleJoueurTK()
		self.grille_suivi = GrilleSuiviTK()
		self.master = master
		self.turn = True
		
		#~ self.grille_suivi.canvas.bind("<Button-1>", self.joue_coup)
		
	# Voilà un exemple de surcharge
	def affiche_messages(self, affiche = True):
		#~ if affiche :
			#~ while self.messages :
				#~ for widj in self.master.pack_slaves() :
					#~ if isinstance(widj, "tkinter.Frame") :
						#~ widj.insert(self.messages.pop(0))
		if affiche :
			for widj in self.master.pack_slaves() :
				if isinstance(widj, Frame) :
					for w in widj.pack_slaves():
					#~ print(widj.pack_slaves())
						if isinstance(w, ScrolledText):
					#~ while self.messages :
							w.insert(END,self.messages.pop(0)+'\n')
						#~ widj.insert("test")
				#~ print(self.messages.pop(0))
				
	def joue_coup(self, event):
		x, y = self.grille_suivi.canvas.canvasx(event.x), self.grille_suivi.canvas.canvasy(event.y)
		(i, j) = self.grille_suivi.coord2case(x,y)
		#~ print(i,j)
		if self.turn :
			#~ print(i,j)
			self.tire((i,j))
			#~ self.affiche_messages()
			#~ print(self.master.pack_slaves())
			#~ print(self.master.children.values())
			self.grille_suivi.affiche_adverse(self.grille_adverse)
			if self.grille_suivi.fini() :
				messagebox.showinfo("","Partie terminée en %d coups" % self.essais)
				self.turn = False

#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiTK(Ordi, JoueurTK):
	def __init__(self, nom='HAL', master=None):
		Ordi.__init__(self, nom=nom)
		JoueurTK.__init__(self, nom=nom, master=master)



class MainTK(Frame):
	def __init__(self, parent):
		self.parent = parent
		Frame.__init__(self, parent)
		parent.title("Bataille navale")
		parent.resizable(False, False)
		self.pack()
		
		self.menubar = Menu(self)
		self.newmenu = Menu(self.menubar, tearoff=0)		
		self.newmenu.add_command(label="Partie solo", command=self.jeu_solo)
		self.newmenu.add_command(label="Résolution automatique", command=self.jeu_ordi)		
		self.newmenu.add_separator()
		self.newmenu.add_command(label="Quitter", command=self.quit)
		self.menubar.add_cascade(label="Nouvelle partie", menu=self.newmenu)
		#~ self.aboutmenu = Menu(self.menubar, tearoff=0)
		#~ self.aboutmenu.add_command(label
		
		
		self.parent.config(menu=self.menubar)
		
		#~ self.solo()
		#~ self.jeu_ordi()
	
		grille1 = GrilleTK(master=self.parent)
		grille2 = GrilleTK(master=self.parent)
		info = ScrolledText(master=self.parent)
		
		grille1.pack(side=LEFT)
		grille2.pack(side=RIGHT)
		
		grille1.affiche()
		grille2.affiche()
		
	def clear_widgets(self):
		for widj in self.parent.pack_slaves() :
			if not isinstance(widj, MainTK) :
				widj.destroy()
	
	def jeu_solo(self):
		def click_solo(event):
			x, y = joueur.grille_suivi.canvas.canvasx(event.x), joueur.grille_suivi.canvas.canvasy(event.y)
			(i, j) = joueur.grille_suivi.coord2case(x,y)
			if joueur.turn and 0<=i<joueur.grille_suivi.xmax and 0<=j<joueur.grille_suivi.ymax :
				joueur.tire((i,j))
				info.delete('1.0', END)
				while joueur.messages :
					info.insert(END, joueur.messages.pop(0)+'\n')
				joueur.grille_suivi.affiche_adverse(joueur.grille_adverse)
				if joueur.grille_suivi.fini() :
					messagebox.showinfo("","Partie terminée en %d coups" % joueur.essais)
					joueur.turn = False
		
		self.clear_widgets()
		grille = GrilleTK(master=self.parent)
		grille.init_bateaux_alea()
		joueur = JoueurTK(master=self.parent)
		joueur.grille_adverse = grille
		joueur.grille_suivi.pack(side=LEFT)
		joueur.grille_suivi.affiche_adverse(joueur.grille_adverse)
		
		joueur.grille_suivi.canvas.bind("<Button-1>", click_solo)
		
		info = ScrolledText(master=self.parent)
		info.pack(side=RIGHT)
			
	def jeu_ordi(self) :
		def suivant(event) :
			if ordi.turn :
				ordi.coup_suivant()
				info.delete('1.0', END)
				while ordi.messages :
					info.insert(END, ordi.messages.pop(0)+'\n')
				ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
				if ordi.grille_suivi.fini() :
					messagebox.showinfo("","Partie terminée en %d coups" % ordi.essais)
					ordi.turn = False
		
		self.clear_widgets()
		grille = GrilleTK(master=self.parent)
		grille.init_bateaux_alea()
		ordi = OrdiTK()
		ordi.grille_adverse = grille
		ordi.grille_suivi.pack(side=LEFT)
		ordi.grille_suivi.affiche_adverse(ordi.grille_adverse)
		
		info = ScrolledText(master=self.parent)
		info.pack(side=RIGHT)
		
		bt_next = Button(text="Next")
		bt_next.pack(side=BOTTOM)
		bt_next.bind("<Button-1>", suivant)
		
		


# ---------------------------------------------------------------------------------------------------------------
# Interface graphique
# ---------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
	root = Tk()
	#~ grille = GrilleTK(master=root)
	#~ grille.init_bateaux_alea()
	#~ 
	#~ debug = ScrolledText(master=root)
	#~ debug.pack(side=RIGHT)
	#~ 
	#~ joueur = JoueurTK(master=root)
	#~ joueur.grille_adverse = grille
	#~ joueur.grille_suivi.pack(side=LEFT)
	#~ joueur.grille_suivi.affiche_adverse(joueur.grille_adverse)
	
	
	app = MainTK(root)
	
	root.mainloop()
