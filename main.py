#
# Projet de bataille navale
# dans le cadre de la formation ISN
#
# Programme principal
#
# Auteurs : Frédéric Muller et Lionel Reboul
#
# Licence CC BY-NC-SA
#
# Projet démarré le 14/11/2015
# Dernière màj : 28/11/2015
# Version 0.1.0
#

from bn_utiles import *
from bn_grille import *
from bn_joueur import *
from bn_interface import *

if __name__== '__main__' :
	"""Programme principal"""

#
#----------------------------------------------------------------------------------------------------------------
#

	def jeu_ordi(affiche = True):
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		ordi = Ordi()
		ordi.grille_adverse = grille
		temps = ordi.joue(affiche = affiche)
		return (ordi.essais, temps) # Pour les tests de performance

#
#----------------------------------------------------------------------------------------------------------------
#

	def jeu_solo():
		"""Jeu solo sur une grille aléatoire"""
		# Initialisation de la partie
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		joueur = Joueur()
		joueur.grille_adverse = grille
		joueur.jeu_solo()
		
#	
#----------------------------------------------------------------------------------------------------------------
#

# Menu de lancement 
	clear()
	print("--------------------")
	print("| Bataille navalle |")
	print("--------------------")
	print("(Il est conseillé de passer en mode plein écran)")
	print()
	print("""Choix du jeu :
--------------
  S : Solo
  O : Ordi 
  T : Test algo""")
	choix = input("--> [O|s|t] ")
	if choix.lower() == 's' :
		jeu_solo()
	elif choix.lower() == 't' :
		n = int(input("Nombre de répétitions : "))
		temps = 0
		s = 0
		for k in range(n):
			(e,t) = jeu_ordi(affiche=False)
			s += e
			temps += t
		print("Nombre de coups moyen : %.2f coups"%(s/n))
		print("Temps moyen : %.5f secondes"%(temps/n))
	else :
		jeu_ordi()
