#!/usr/bin/python3

from random import *
import os
import cgi
import shelve

from bn_grille import *
from bn_joueur import *

nom_joueur = "Joueur"
nom_ordi = "HAL"


html_header = """<!DOCTYPE html>

<html>
<head>
<title>Bataille navale</title>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="../css/style_duo.css">
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
		ordi=Ordi()
		#~ ordi.add_message("C'est parti !")
		grilleo = GrilleJoueur()
		grilleo.init_bateaux_alea()
		ordi.grille_adverse = grilleo
		sh['ordi']=ordi
		
		joueur=Joueur()
		joueur.add_message("C'est parti !")
		grillej = GrilleJoueur()
		grillej.init_bateaux_alea()
		joueur.grille_adverse = grillej
		joueur.grille_joueur = grilleo
		sh['joueur'] = joueur
		
		
	finally :
		sh.close
else :
	# Sinon on charge la partie à partir du fichier de session
	try :
		joueur = sh['joueur']
		ordi=sh['ordi']
	#~ except:
		#~ print("""<script>window.location="solo.py?id=0"</script>""")
		#~ quit()
	finally :
		sh.close 

fini = False
if jx!=None and jy!=None :
	joueur.tire((jx,jy))
	if joueur.grille_suivi.fini() :
		joueur.add_message("Bravo ! Vous avez gagné en %d coups" % joueur.essais)
		fini = True
	else :
		ordi.coup_suivant()
		if ordi.grille_suivi.fini():
			ordi.add_message("L'ordinateur a gagné en %d coups" % ordi.essais)
			fini = True
		
# Création de la page
print(html_header)
print("<body>")
print("""<div id="titre">
	<button class="boutton" style="float:left;" name="index" onclick='window.location="../index.html"'>Retour</button>
	<h1>Partie contre l'ordinateur</h1>
	</div>
	""")

print(r"""
	<div id="game">
		<div class="grille">
			<p class="nom">Joueur</p>
			<canvas id="myCanvas1" width="430" height="430"></canvas> 
		</div>
		<div class="grille">
			<p class="nom">HAL</p>
			<canvas id="myCanvas2" width="430" height="430"></canvas> 
		</div>
	<script>
		var canvas1 = document.getElementById("myCanvas1");
		var ctx1 = canvas1.getContext("2d");
		var canvas2 = document.getElementById("myCanvas2");
		var ctx2 = canvas2.getContext("2d");
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

		// Dessin de la grille
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
			
			// Dessin de la grille
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
		""")

for i in range(joueur.grille_joueur.xmax):
	for j in range(joueur.grille_joueur.ymax):
		if joueur.grille_joueur.etat[(i,j)] == 1 :
			print("marqueCase(ctx2,%d,%d,'bateau');\n"%(i,j))


for i in range(joueur.grille_suivi.xmax):
	for j in range(joueur.grille_suivi.ymax):
		if joueur.grille_suivi.etat[(i,j)] == 1 :
			print("marqueCase(ctx1,%d,%d,'touche');\n"%(i,j))
		elif joueur.grille_suivi.etat[(i,j)] == -1 :
			print("marqueCase(ctx1,%d,%d,'manque');\n"%(i,j))

for i in range(ordi.grille_suivi.xmax):
	for j in range(ordi.grille_suivi.ymax):
		if ordi.grille_suivi.etat[(i,j)] == 1 :
			print("marqueCase(ctx2,%d,%d,'touche');\n"%(i,j))
		elif ordi.grille_suivi.etat[(i,j)] == -1 :
			print("marqueCase(ctx2,%d,%d,'manque');\n"%(i,j))

print("</script>")
print('<p id="infos">')
if first :
	print("C'est parti !")
while joueur.messages :
	mess = joueur.messages.pop(0)
	if "Touché" in mess or "Manqué" in mess or "gagné" in mess :
		print("&ltJoueur&gt " + mess)
		print("<br>")
while ordi.messages :
	mess = ordi.messages.pop(0)
	if "Touché" in mess or "Manqué" in mess  or "gagné" in mess :
		print("&ltHAL&gt " + mess)
		print("<br>")


print("</p>")
print("</div>")
if fini :
	print("""<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="duo_ordi.py?id=0"'>
		Nouvelle partie
		</button>'
		""")
	os.remove(os.path.join("sessions","session_%s"% ID))
else :
	print("""<script>
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
			window.location="duo_ordi.py?id="+sessionID+"&jx="+jx+"&jy="+jy;
		});
	</script>""")
	# Sauvegarde de l'état de la partie
	sh = shelve.open(os.path.join("sessions","session_%s"% ID))
	try :
		sh['joueur']=joueur
		sh['ordi']=ordi
	finally :
		sh.close

print("</body>")
print("</html>")

