#!/usr/bin/python3

from random import *
import os
import cgi
import shelve

from bn_grille import *
from bn_joueur import *

html_header = """<!DOCTYPE html>

<html>
<head>
<title>Bataille navale</title>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="../css/style_game.css">
\n"""


form = cgi.FieldStorage()
# Récupération de l'ID ou initialisation de la partie
try :
	sessionID = cgi.escape(form['id'].value)
	noID = False
except :
	noID = True

if noID or sessionID=='0' or not os.path.isfile(os.path.join("sessions","session_%s"% sessionID)):
	first = True
	ID = str(randint(1,1000000000))
else:
	ID = sessionID
	first = False
html_header += "<script>var sessionID=%s;</script>\n" % ID
html_header += "</head>\n\n"


# Gestion de la session
sh = shelve.open(os.path.join("sessions","session_%s"% ID))
if first :
	# 1er lancement, on crée la partie
	try :
		ordi=Ordi()
		ordi.add_message("C'est parti !")
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		ordi.grille_adverse = grille
		sh['ordi']=ordi
	finally :
		sh.close
else :
	# Sinon on charge la partie à partir du fichier de session
	try :
		ordi = sh['ordi']
		ordi.coup_suivant()
	#~ except:
		#~ print("""<script>window.location="solo.py?id=0"</script>""")
		#~ quit()
	finally :
		sh.close 

fini = False
if ordi.grille_suivi.fini() :
		ordi.add_message("Partie terminée en %d coups" % ordi.essais)
		fini = True
		
# Création de la page
print(html_header)
print("<body>")

print("""<div id="titre">
	<button class="boutton" style="float:left;" name="index" onclick='window.location="../index.html"'>Retour</button>
	<h1>Résolution automatique</h1>
	</div>
	""")

print(r"""
	<div id="game">
	<canvas id="myCanvas" width="430" height="430">
	</canvas> 

	<script>
		var canvas = document.getElementById("myCanvas");
		var ctx = canvas.getContext("2d");
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
		function marqueCase(i,j,etat){
			// Marque une case suivant son état
			if (etat=='touche'){
				ctx.fillStyle = "#DD4444";
			} else if (etat=='manque'){
				ctx.fillStyle = "#44DD44";
			} else if (etat=='bateau'){
				ctx.fillStyle = "#00FFFF";
			} else {
				ctx.fillStyle = "#FFFFFF";
			}
			x = case2coord(i,j).x;
			y = case2coord(i,j).y;
			ctx.fillRect(x+1,y+1,largCase-2,largCase-2);
		}

		// Dessin de la grille
		ctx.font = "20px Arial";
		ctx.textAlign = "center";
			// Lignes
		for(var i=0;i<10;i++){
			ctx.fillText(String.fromCharCode(65+i),margeLeft+largCase/2+largCase*i,margeTop-5);
			//~ ctx.fillText(i,margeLeft+largCase/2+largCase*i,margeTop-5);
		}
		for(var i=0;i<=10;i++){	
			ctx.moveTo(margeLeft,margeLeft+largCase*i);
			ctx.lineTo(margeLeft+10*largCase, margeLeft+largCase*i);
			ctx.stroke();
		}
			// Colonnes
		for(var i=0;i<10;i++){		
			ctx.fillText(i,margeLeft-15,margeTop+largCase/2+5+largCase*i);
		}
		for(var i=0;i<=10;i++){	
			ctx.moveTo(margeLeft+largCase*i,margeTop);
			ctx.lineTo(margeLeft+largCase*i,margeTop+10*largCase);
			ctx.stroke();
		}
		""")

for i in range(ordi.grille_suivi.xmax):
	for j in range(ordi.grille_suivi.ymax):
		if ordi.grille_suivi.etat[(i,j)] == 1 :
			print("marqueCase(%d,%d,'touche');\n"%(i,j))
		elif ordi.grille_suivi.etat[(i,j)] == -1 :
			print("marqueCase(%d,%d,'manque');\n"%(i,j))
			

print("</script>")
print('<p id="infos">')
while ordi.messages :
	print(ordi.messages.pop(0).replace("<","&lt").replace(">","&gt"))
	print("<br>")
print("</p>")
print("</div>")

if  fini :
	print("""<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="ordi.py?id=0"' autofocus>
	Nouvelle partie
	</button>'
	""")
	os.remove(os.path.join("sessions","session_%s"% ID))
else :
	print("""<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="ordi.py?id="+sessionID'>
	Coup suivant
	</button>'
	""")
	sh = shelve.open(os.path.join("sessions","session_%s"% ID))
	try :
		sh['ordi']=ordi
	finally :
		sh.close

print("</body>")
print("</html>")
