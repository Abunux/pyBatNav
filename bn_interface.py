# Version 0.0.0

from tkinter import *
from tkinter import messagebox
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
		
		self.turn = True
		
		self.grille_suivi.canvas.bind("<Button-1>", self.joue_coup)
		
	# Voilà un exemple de surcharge
	def affiche_messages(self, affiche = True):
		if affiche :
			while self.messages :
				# À adapter pour la fenêtre de débug
				print(self.messages.pop(0))
				
	def joue_coup(self, event):
		x, y = self.grille_suivi.canvas.canvasx(event.x), self.grille_suivi.canvas.canvasy(event.y)
		(i, j) = self.grille_suivi.coord2case(x,y)
		#~ print(i,j)
		if self.turn :
			#~ print(i,j)
			self.tire((i,j))
			self.grille_suivi.affiche_adverse(self.grille_adverse)
			if self.grille_suivi.fini() :
				messagebox.showinfo("","Partie terminée en %d coups" % self.essais)
				self.turn = False

#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiTK(Ordi, JoueurTK):
	def __init__(self, nom='HAL'):
		Ordi.__init__(self, nom=nom)



# ---------------------------------------------------------------------------------------------------------------
# Interface graphique
# ---------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":
	root = Tk()
	grille = GrilleTK(master=root)
	#~ grille.pack()
	grille.init_bateaux_alea()
	#~ grille.affiche_adverse()
	#~ grille2 = GrilleTK(master=root)
	#~ grille2.pack()
	#~ 
	
	joueur = JoueurTK()
	joueur.grille_adverse = grille
	joueur.grille_suivi.pack()
	joueur.grille_suivi.affiche_adverse(joueur.grille_adverse)
	
	
	
	root.mainloop()
