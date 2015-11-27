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

class GrilleTK(Grille):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		Grille.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleJoueurTK(Grille):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleJoueur.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class GrilleSuiviTK(Grille):
	def __init__(self, xmax=10, ymax=10, taille_bateaux = [5, 4, 3, 3, 2]):
		GrilleSuivi.__init__(self, xmax, ymax, taille_bateaux)

#
#----------------------------------------------------------------------------------------------------------------
#
class JoueurTK(Joueur):
	def __init__(self, nom='Joueur'):
		Joueur.__init__(self, nom)
		self.grille_joueur = GrilleJoueurTK()
		self.grille_adverse = GrilleJoueurTK()
		self.grille_suivi = GrilleSuiviTK()
	
	# voilà un exemple de surcharge
	def affiche_messages(self, affiche = True):
		if affiche :
			while self.messages :
				# À adapter pour la fenêtre de débug
				print(self.messages.pop(0))

#
#----------------------------------------------------------------------------------------------------------------
#

class OrdiTK(Ordi):
	def __init__(self, nom='HAL'):
		Ordi.__init__(self, nom)



# ---------------------------------------------------------------------------------------------------------------
# Interface graphique
# ---------------------------------------------------------------------------------------------------------------


# Mets ton code Tkinter ici
