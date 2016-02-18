#!/usr/bin/python3

from random import *
import os
import cgi
import shelve

from bn_grille import *
from bn_joueur import *

nom_joueur = "Joueur"
nom_ordi = "HAL"

# Initialisation de la page et de la session
# ------------------------------------------
html_header = """<!DOCTYPE html>

<html>
<head>
<title>Bataille navale</title>
<meta charset="UTF-8">
\n"""


# Récupération des paramètres cgi
form = cgi.FieldStorage()

# Récupération du mode de jeu
# 0 : solo
# 1 : duo contre l'ordi
# 2 : ordi seul
try :
	mode = int(cgi.escape(form['mode'].value))
except :
	mode = 0

# Feuille de style en fonction du mode (solo ou duo)
if mode != 1 :
	html_header += """<link rel="stylesheet" type="text/css" href="../css/style_solo.css">\n"""
else :
	html_header += """<link rel="stylesheet" type="text/css" href="../css/style_duo.css">\n"""
	
# Récupération de l'ID ou initialisation de la partie
try :
	sessionID = cgi.escape(form['id'].value)
	noID = False
except :
	noID = True

if sessionID=='0' or noID or not os.path.isfile(os.path.join("sessions", "session_%s" % sessionID)):
	first = True
	ID = str(randint(1,1000000000))
else:
	ID = sessionID
	first = False
html_header += "<script>var sessionID=%s;</script>\n" % ID
html_header += "</head>\n\n"

# Case jouée
if 'jx' in form :
	jx = int(cgi.escape(form['jx'].value))
else :
	jx = None
if 'jy' in form :
	jy = int(cgi.escape(form['jy'].value))
else :
	jy = None

# Gestion de la session
sh = shelve.open(os.path.join("sessions", "session_%s" % ID))
if first :
	# 1er lancement, on crée la partie
	try :
		#~ ordi=Ordi()
		#~ grilleo = GrilleJoueur()
		#~ grilleo.init_bateaux_alea()
		#~ ordi.grille_adverse = grilleo
		#~ sh['ordi']=ordi
		#~ 
		#~ joueur=Joueur()
		#~ grillej = GrilleJoueur()
		#~ grillej.init_bateaux_alea()
		#~ joueur.grille_adverse = grillej
		#~ joueur.grille_joueur = grilleo
		#~ sh['joueur'] = joueur
		
		# Cration des joueurs
		ordi = Ordi()
		joueur = Joueur()
		
		# Initialisation des grilles de chacun
		grille_ordi = GrilleJoueur()
		grille_ordi.init_bateaux_alea()
		grille_joueur = GrilleJoueur()
		grille_joueur.init_bateaux_alea()
		
		ordi.grille_joueur = grille_ordi
		ordi.grille_adverse = grille_joueur
		
		joueur.grille_joueur = grille_joueur
		joueur.grille_adverse = grille_ordi
		
		# Sauvegarde des joueurs
		sh['ordi']=ordi
		sh['joueur'] = joueur
	finally :
		sh.close
else :
	# Sinon on charge la partie à partir du fichier de session
	try :
		joueur = sh['joueur']
		ordi=sh['ordi']
	finally :
		sh.close 

# Coup suivant
fini = False
if mode == 0 :
	if jx!=None and jy!=None :
		joueur.tire((jx,jy))
		if joueur.grille_suivi.fini() :
			joueur.add_message("Bravo ! Vous avez terminé en %d coups" % joueur.essais)
			fini = True
elif mode == 1 :
	if jx!=None and jy!=None :
		ok = joueur.grille_suivi.test_case((jx,jy))
		joueur.tire((jx,jy))
		if joueur.grille_suivi.fini() :
			joueur.add_message("Bravo ! Vous avez gagné en %d coups" % joueur.essais)
			gagnant = 0
			fini = True
		else :
			if ok :
				ordi.coup_suivant()
				if ordi.grille_suivi.fini():
					ordi.add_message("L'ordinateur a gagné en %d coups" % ordi.essais)
					gagnant = 1
					fini = True
elif mode == 2 :
	if not first :
		ordi.coup_suivant()
	if ordi.grille_suivi.fini() :
		ordi.add_message("Partie terminée en %d coups" % ordi.essais)
		fini = True

# Création du body de la page
# ---------------------------
html_body = "<body>\n"

# Titre
html_body += """<div id="titre">
	<button class="boutton" style="float:left;" name="index" onclick='window.location="../index.html"'>Retour</button>
	<h1>%s</h1>
	</div>
	""" % (["Partie solo", "Partie contre l'ordinateur", "Résolution automatique"][mode])

# Création du canvas et des fonctions javascript associées
html_body += """<div id="game">\n"""

if mode == 0 :		# Grille du joueur
	html_body += """
		<canvas id="myCanvas1" width="430" height="430"></canvas> 
	"""
elif mode ==2 :		# Grille de l'ordinateur
	 html_body += """
		<canvas id="myCanvas2" width="430" height="430"></canvas> 
	"""
else :			# Deux grilles
	html_body += """<div class="grille">
			<p class="nom">%s</p>
			<canvas id="myCanvas1" width="430" height="430"></canvas> 
		</div>
		<div class="grille">
			<p class="nom">%s</p>
			<canvas id="myCanvas2" width="430" height="430"></canvas> 
		</div>\n"""%(nom_joueur, nom_ordi)

# Javascript pour gérer le canvas
html_body += "<script>\n"
if mode <= 1 :		# Grille du joueur
	html_body += """
		var canvas1 = document.getElementById("myCanvas1");
		var ctx1 = canvas1.getContext("2d");
		"""
if mode >= 1 :		# Grille de l'ordinateur
	html_body += """var canvas2 = document.getElementById("myCanvas2");
		var ctx2 = canvas2.getContext("2d");
		"""
		
html_body += """
		// Marges
		var margeLeft=30;
		var margeTop=30;
		// Largeur des cases
		var largCase=40;

		// Gestion des cases
			// Conversion des coordonnées
		function case2coord(i,j){
			// Récupère les coordonnées graphiques du coin en haut à gauche de la case
			return {'x':margeLeft+i*largCase, 'y':margeTop+j*largCase};
		}

		function coord2case(x,y){
			// Récupère les coordonnées d'une case	
			return {'i':Math.floor((x-margeLeft)/largCase), 'j':Math.floor((y-margeTop)/largCase)};
		}
			// Marquage des cases
		function marqueCase(ctx,i,j,etat){
			// Marque une case suivant son état
			if (etat=='touche'){
				ctx.fillStyle = "#DD4444";
			} else if (etat=='manque'){
				ctx.fillStyle = "#44DD44";
			} else if (etat=='bateau'){
				ctx.fillStyle = "#44DDDD";
			} else {
				ctx.fillStyle = "#FFFFFF";
			}
			x = case2coord(i,j).x;
			y = case2coord(i,j).y;
			ctx.fillRect(x+1,y+1,largCase-2,largCase-2);
		}
		"""

if mode <= 1 :		# Grille du joueur
	html_body += """
		// Dessin de la grille 1
			ctx1.font = "20px Arial";
			ctx1.textAlign = "center";
				// Lignes
			for(var i=0;i<10;i++){
				ctx1.fillText(String.fromCharCode(65+i),margeLeft+largCase/2+largCase*i,margeTop-5);
				//~ ctx1.fillText(i,margeLeft+largCase/2+largCase*i,margeTop-5);
			}
			for(var i=0;i<=10;i++){	
				ctx1.moveTo(margeLeft,margeLeft+largCase*i);
				ctx1.lineTo(margeLeft+10*largCase, margeLeft+largCase*i);
				ctx1.stroke();
			}
				// Colonnes
			for(var i=0;i<10;i++){		
				ctx1.fillText(i,margeLeft-15,margeTop+largCase/2+5+largCase*i);
			}
			for(var i=0;i<=10;i++){	
				ctx1.moveTo(margeLeft+largCase*i,margeTop);
				ctx1.lineTo(margeLeft+largCase*i,margeTop+10*largCase);
				ctx1.stroke();
			}
			"""
if mode >= 1 :		# Grille de l'ordinateur
	html_body += """
			// Dessin de la grille 2
			ctx2.font = "20px Arial";
			ctx2.textAlign = "center";
				// Lignes
			for(var i=0;i<10;i++){
				ctx2.fillText(String.fromCharCode(65+i),margeLeft+largCase/2+largCase*i,margeTop-5);
				//~ ctx2.fillText(i,margeLeft+largCase/2+largCase*i,margeTop-5);
			}
			for(var i=0;i<=10;i++){	
				ctx2.moveTo(margeLeft,margeLeft+largCase*i);
				ctx2.lineTo(margeLeft+10*largCase, margeLeft+largCase*i);
				ctx2.stroke();
			}
				// Colonnes
			for(var i=0;i<10;i++){		
				ctx2.fillText(i,margeLeft-15,margeTop+largCase/2+5+largCase*i);
			}
			for(var i=0;i<=10;i++){	
				ctx2.moveTo(margeLeft+largCase*i,margeTop);
				ctx2.lineTo(margeLeft+largCase*i,margeTop+10*largCase);
				ctx2.stroke();
			}
		"""

# Coloriage des cases
if mode >= 1 :
	for i in range(joueur.grille_joueur.xmax):
		for j in range(joueur.grille_joueur.ymax):
			if joueur.grille_joueur.etat[(i,j)] == 1 :
				html_body += "marqueCase(ctx2,%d,%d,'bateau');\n"%(i,j)
	for i in range(ordi.grille_suivi.xmax):
		for j in range(ordi.grille_suivi.ymax):
			if ordi.grille_suivi.etat[(i,j)] == 1 :
				html_body += "marqueCase(ctx2,%d,%d,'touche');\n"%(i,j)
			elif ordi.grille_suivi.etat[(i,j)] == -1 :
				html_body += "marqueCase(ctx2,%d,%d,'manque');\n"%(i,j)

if mode <= 1 :
	for i in range(joueur.grille_suivi.xmax):
		for j in range(joueur.grille_suivi.ymax):
			if joueur.grille_suivi.etat[(i,j)] == 1 :
				html_body += "marqueCase(ctx1,%d,%d,'touche');\n"%(i,j)
			elif joueur.grille_suivi.etat[(i,j)] == -1 :
				html_body += "marqueCase(ctx1,%d,%d,'manque');\n"%(i,j)

# Fin du script
html_body += "</script>\n"

# Informations de partie
html_body += '<p id="infos">\n'
if first :
	html_body += "C'est parti !"
while joueur.messages :
	mess = joueur.messages.pop(0)
	if mode !=1 or (mode == 1 and ("Touché" in mess or "Manqué" in mess or "déjà" in mess.lower() or "gagné" in mess)) :
		html_body += "&lt%s&gt "% nom_joueur + mess
		html_body += "<br>"
while ordi.messages :
	mess = ordi.messages.pop(0)
	if mode !=1 or (mode == 1 and ("Touché" in mess or "Manqué" in mess  or "gagné" in mess)) :
		html_body += "&lt%s&gt " % nom_ordi + mess
		html_body += "<br>"
html_body += "</p>\n"
html_body += "</div>\n"

# Fin de la partie ou coup suivant
if fini :
	# Nouvelle partie
	html_body += """<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="bn_cgi.py?id=0&mode=%d"'>
		Nouvelle partie
		</button>
		""" % mode
	if mode == 0 or (mode == 1 and gagnant == 0) :
		html_body += """<script>alert("Bravo ! Vous avez gagné en %d coups.")</script>\n""" % joueur.essais
	elif mode == 2 or (mode == 1 and gagnant == 1) :
		html_body += """<script>alert("%s a gagné en %d coups.")</script>\n""" % (nom_ordi, ordi.essais)
	os.remove(os.path.join("sessions", "session_%s" % ID))
else :
	if mode <= 1 :
	# Récupération des événements souris
		html_body += """<script>
		// Événements souris
			var elem = document.getElementById('myCanvas1'),
				elemLeft = elem.offsetLeft,
				elemTop = elem.offsetTop;
			elem.addEventListener('click', function(event) {
				var x = event.pageX - elemLeft-12,
					y = event.pageY - elemTop-12;
				//~ alert(x+','+y);
				if (x<margeLeft||x>margeLeft+10*largCase||y<margeTop||y>margeTop+10*largCase){
					return null;
				}
				jx=coord2case(x,y).i;
				jy=coord2case(x,y).j;
				window.location="bn_cgi.py?id="+sessionID+"&mode=%s"+"&jx="+jx+"&jy="+jy;
			});
		</script>""" % mode
	else :
		# Boutton "Coup suivant"
		html_body += """<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="bn_cgi.py?id="+sessionID+"&mode=%d"'>
	Coup suivant
	</button>
	""" % mode
	
	# Sauvegarde de l'état de la partie
	sh = shelve.open(os.path.join("sessions", "session_%s" % ID))
	try :
		sh['joueur']=joueur
		sh['ordi']=ordi
	finally :
		sh.close

html_body += "</body>\n"
html_body += "</html>"

# Affichage de la page
print(html_header)
print(html_body)

