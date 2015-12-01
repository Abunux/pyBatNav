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
# Dernière màj : 01/12/2015
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
	def jeu_ordi(affiche=True):
		"""Résolution d'une grille par l'ordinateur"""
		# Initialisation de la partie
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		ordi = Ordi()
		ordi.grille_adverse = grille
		
		temps = ordi.resolution(affiche=affiche)
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
	def jeu_contre_ordi():
		"""Partie en duel contre l'ordi"""
		joueur = Joueur("Toto")
		ordi = Ordi()
		partie = Partie(joueur, ordi)

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
  J : Jeu contre l'ordinateur
  T : Test algo
  """)
	choix = input("--> [S|O|T|[J]] ")
	
	if choix.lower() == 's' :
		jeu_solo()
		
	elif choix.lower() == 't' :
		print()
		n = int(input("Nombre de répétitions : "))
		temps_total = 0
		liste_essais = []
		mini = 100
		maxi = 0
		for k in range(n):
			(essais,temps) = jeu_ordi(affiche=False)
			temps_total += temps
			liste_essais.append(essais)
			
		print()
		print("Résultats de la simulation :")
		print()
		print("Nombre de coups moyen : %.2f coups" % (sum(liste_essais)/n))
		print("Nombre de coups minimum : %.2f coups" % min(liste_essais))
		print("Nombre de coups maximum : %.2f coups" % max(liste_essais))
		print()
		print("Temps moyen par partie : %.5f secondes"%(temps_total/n))
		
	elif choix.lower() == 'o' :
		jeu_ordi()
		
	else :
		jeu_contre_ordi()
