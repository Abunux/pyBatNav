# Version 0.0.0

from tkinter import *

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
		
		self.create_canvas()
		
		self.marque_case(2,3,1)
		
	def create_canvas(self):
		self.margeLeft = 30
		self.margeTop = 30
		self.largCase = 40
		self.can_width = 1.5*self.margeLeft+self.xmax*self.largCase
		self.can_height = height=1.5*self.margeTop+self.ymax*self.largCase
		#~ self.canvas = Canvas(self, width=1.5*self.margeLeft+self.xmax*self.largCase, height=1.5*self.margeTop+self.ymax*self.largCase)
		self.canvas = Canvas(self, width=self.can_width, height=self.can_height)
		self.canvas.pack()
		for i in range(self.xmax+1) :
			self.canvas.create_line(self.margeLeft, self.margeTop+i*self.largCase, self.margeLeft+self.xmax*self.largCase, self.margeTop+i*self.largCase)
		for i in range(self.ymax+1) :
			self.canvas.create_line(self.margeLeft+i*self.largCase, self.margeTop, self.margeLeft+i*self.largCase, self.margeTop+self.ymax*self.largCase)
			
		for i in range(self.xmax):
			self.canvas.create_text(self.margeLeft/2, self.margeTop+i*self.largCase+self.largCase/2, text=str(i), font=("Helvetica",12))
		for i in range(self.xmax):
			self.canvas.create_text(self.margeLeft+i*self.largCase+self.largCase/2, self.margeTop/2, text=chr(i+65), font=("Helvetica",12))
			
	def coord2case(self, x, y) :
		return ((x-self.margeLeft)//self.largCase, (y-self.margeTop)//self.largCase)
		
	def case2coord(self, i, j):
		return (self.margeLeft+i*self.largCase, self.margeTop+j*self.largCase)
	
	def marque_case(self, i, j, etat):
		(x, y) = self.case2coord(i,j) 
		if etat == 1 :
			couleur = "red"
		self.canvas.create_rectangle(x+1, y+1, x+self.largCase-1, y+self.largCase-1, fill=couleur)
#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleJoueurTK(GrilleJoueur, GrilleTK):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleJoueur.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuiviTK(GrilleSuivi, GrilleTK):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleSuivi.__init__(self, xmax=xmax, ymax=ymax, taille_bateaux=taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class JoueurTK(Joueur):
	def __init__(self, nom='Joueur'):
		Joueur.__init__(self, nom=nom)
		self.grille_joueur = GrilleJoueurTK()
		self.grille_adverse = GrilleJoueurTK()
		self.grille_suivi = GrilleSuiviTK()
	
	# Voilà un exemple de surcharge
	def affiche_messages(self, affiche = True):
		if affiche :
			while self.messages :
				# À adapter pour la fenêtre de débug
				print(self.messages.pop(0))

#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiTK(Ordi, JoueurTK):
	def __init__(self, nom='HAL'):
		Ordi.__init__(self, nom=nom)



# ---------------------------------------------------------------------------------------------------------------
# Interface graphique
# ---------------------------------------------------------------------------------------------------------------


# Mets ton code Tkinter ici


if __name__ == "__main__":
	root = Tk()
	grille = GrilleTK(master=root)
	grille.pack()
	root.mainloop()
