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

if sessionID=='0' or noID or not os.path.isfile(os.path.join("sessions","session_%s"% sessionID)):
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
sh = shelve.open(os.path.join("sessions","session_%s"% ID))
if first :
	# 1er lancement, on crée la partie
	try :
		joueur=Joueur()
		joueur.add_message("C'est parti !")
		grille = GrilleJoueur()
		grille.init_bateaux_alea()
		joueur.grille_adverse = grille
		sh['joueur'] = joueur
	finally :
		sh.close
else :
	# Sinon on charge la partie à partir du fichier de session
	try :
		joueur = sh['joueur']
	#~ except:
		#~ print("""<script>window.location="solo.py?id=0"</script>""")
		#~ quit()
	finally :
		sh.close 

fini = False
if jx!=None and jy!=None :
	joueur.tire((jx,jy))
	if joueur.grille_suivi.fini() :
		joueur.add_message("Bravo ! Vous avez terminé en %d coups" % joueur.essais)
		fini = True
		
# Création de la page
print(html_header)
print("<body>")
print("""<div id="titre">
	<button class="boutton" style="float:left;" name="index" onclick='window.location="../index.html"'>Retour</button>
	<h1>Partie solo</h1>
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

for i in range(joueur.grille_suivi.xmax):
	for j in range(joueur.grille_suivi.ymax):
		if joueur.grille_suivi.etat[(i,j)] == 1 :
			print("marqueCase(%d,%d,'touche');\n"%(i,j))
		elif joueur.grille_suivi.etat[(i,j)] == -1 :
			print("marqueCase(%d,%d,'manque');\n"%(i,j))

print("</script>")
print('<p id="infos">')
while joueur.messages :
	print(joueur.messages.pop(0).replace("<","&lt").replace(">","&gt"))
	print("<br>")
print("</p>")
print("</div>")
if fini :
	print("""<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="solo.py?id=0"'>
		Nouvelle partie
		</button>'
		""")
	os.remove(os.path.join("sessions","session_%s"% ID))
else :
	print("""<script>
	// Événements souris
		var elem = document.getElementById('myCanvas'),
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
			window.location="solo.py?id="+sessionID+"&jx="+jx+"&jy="+jy;
		});
	</script>""")
	# Sauvegarde de l'état de la partie
	sh = shelve.open(os.path.join("sessions","session_%s"% ID))
	try :
		sh['joueur']=joueur
	finally :
		sh.close

print("</body>")
print("</html>")
