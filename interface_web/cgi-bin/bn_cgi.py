#!/usr/bin/env python3

"""Module bn_cgi

Crée un interface web à l'aide d'un script cgi

Lancer le fichier bn_webserver.py et aller sur http://localhost:8000/index.html

La session est suvegardée dans un fichier ./sessions/session_ID de la racine web

Les paramètres suivants sont passés en cgi :
    - session : l'ID de la session
    - mode : mode de jeu (solo, ordi seul ou partie contre l'ordi)
    - jx, jy : les coordonnées cliquées

Auteur : Frédéric Muller

Licence CC BY-NC-SA

Version 0.1.0"""

from random import *
import os
import cgi
import shelve

from bn_grille import *
from bn_joueur import *

# Initialisation de la page et de la session
# ------------------------------------------
nom_joueur = "Joueur"
nom_ordi = "HAL"

# Récupération des paramètres cgi
form = cgi.FieldStorage()

# Récupération du mode de jeu
    # 0 : solo
    # 1 : joueur contre l'ordi
    # 2 : ordi seul
    # mode <= 1 : il y a un joueur
    # mode >= 1 : il y a un ordi
    # mode != 1 : un seul joueur
try :
    mode = int(cgi.escape(form['mode'].value))
except :
    mode = 0
if mode > 2 or mode < 0:
    mode = 0
titre = ["Partie solo", "Partie contre l'ordinateur", "Résolution automatique"][mode]

# Création du <header> de la page
# (note : sauter une ligne avant le doctype)
html_header = """
<!DOCTYPE html>

<html>
    <head>
        <title>%s</title>
        <meta charset="UTF-8">\n""" % titre

# Feuille de style en fonction du mode (solo ou duo)
if mode != 1 :
    html_header += """      <link rel="stylesheet" type="text/css" href="../css/style_solo.css">\n"""
else :
    html_header += """      <link rel="stylesheet" type="text/css" href="../css/style_duo.css">\n"""

# Récupération ou création de l'ID de session
try :
    sessionID = cgi.escape(form['id'].value)
    noID = False
except :
    noID = True

if sessionID=='0' or noID :
    first = True
    ID = str(randint(1,1000000000))
else:
    ID = sessionID
    first = False

# Sauvegarde de l'ID de session dans la page et fin du header
html_header += "        <script>var sessionID=%s;</script>\n" % ID
html_header += "    </head>\n\n"

# Gestion de la session
try :
    sh = shelve.open(os.path.join("sessions", "session_%s" % ID))
except :
    first = True

if first :
    # Si 1er lancement, on crée la partie
    try :
        # Création des joueurs
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
        sh['ordi'] = ordi
        sh['joueur'] = joueur
    finally :
        sh.close
else :
    # Sinon on charge la partie à partir du fichier de session
    try :
        joueur = sh['joueur']
        ordi = sh['ordi']
    finally :
        sh.close

# Déroulement de la partie
# ------------------------
# Case jouée
if 'jx' in form :
    jx = int(cgi.escape(form['jx'].value))
else :
    jx = None
if 'jy' in form :
    jy = int(cgi.escape(form['jy'].value))
else :
    jy = None

# Coup suivant ou fin de partie
fini = False
if mode == 0 :
    if jx != None and jy != None :
        joueur.tire( (jx, jy) )
        if joueur.grille_suivi.fini() :
            joueur.add_message("Bravo ! Vous avez terminé en %d coups" % joueur.essais)
            fini = True
elif mode == 1 :
    if jx!=None and jy!=None :
        ok = joueur.grille_suivi.test_case( (jx, jy) )
        joueur.tire( (jx, jy) )
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

# Création du <body> de la page
# -----------------------------
html_body = "   <body>\n"

# Titre de la page
html_body += """        <div id="titre">
            <button class="boutton" style="float:left;" name="index" onclick='window.location="../index.html"'>Retour</button>
            <h1>%s</h1>
        </div>\n""" % titre

# Création du canvas et des fonctions javascript associées
html_body += """        <div id="game">\n"""

if mode == 0 :      # Grille du joueur
    html_body += """            <canvas id="canvasJoueur" width="430" height="430"></canvas>\n"""
elif mode ==2 :     # Grille de l'ordinateur
     html_body += """           <canvas id="canvasOrdi" width="430" height="430"></canvas>\n"""
else :          # Deux grilles
    html_body += """            <div class="grille">
                <p class="nom">%s</p>
                <canvas id="canvasJoueur" width="430" height="430"></canvas>
            </div>
            <div class="grille">
                <p class="nom">%s</p>
                <canvas id="canvasOrdi" width="430" height="430"></canvas>
            </div>\n\n""" % (nom_joueur, nom_ordi)

# Javascript pour gérer le canvas
html_body += "          <script>\n"
if mode <= 1 :      # Grille du joueur
    html_body += """                var canvas1 = document.getElementById("canvasJoueur");
                var ctx1 = canvas1.getContext("2d");\n"""
if mode >= 1 :      # Grille de l'ordinateur
    html_body += """                var canvas2 = document.getElementById("canvasOrdi");
                var ctx2 = canvas2.getContext("2d");\n"""

html_body += """
                // Marges pour les lettres et les chiffres
                var margeLeft = 30;
                var margeTop = 30;
                // Largeur des cases
                var largCase = 40;

                // Conversion des coordonnées
                function case2coord(i, j){
                    // Récupère les coordonnées graphiques du coin en haut à gauche de la case
                    return {'x':margeLeft+i*largCase, 'y':margeTop+j*largCase};
                }

                function coord2case(x, y){
                    // Récupère les coordonnées d'une case
                    return {'i':Math.floor((x-margeLeft)/largCase), 'j':Math.floor((y-margeTop)/largCase)};
                }

                // Marquage des cases
                function marqueCase(ctx, i, j, etat){
                    // Marque la case (i,j) de la grille ctx suivant son état
                    if (etat == 'touche'){
                        ctx.fillStyle = "#DD4444";
                    } else if (etat == 'manque'){
                        ctx.fillStyle = "#44DD44";
                    } else if (etat == 'bateau'){
                        ctx.fillStyle = "#44DDDD";
                    } else {
                        ctx.fillStyle = "#FFFFFF";
                    }
                    x = case2coord(i,j).x;
                    y = case2coord(i,j).y;
                    ctx.fillRect(x+1, y+1, largCase-2, largCase-2);
                }
"""

if mode <= 1 :      # Grille du joueur
    html_body += """
                // Dessin de la grille 1
                ctx1.font = "20px Arial";
                ctx1.textAlign = "center";
                    // Lignes
                for(var i=0; i<10; i++){
                    ctx1.fillText(String.fromCharCode(65+i), margeLeft+largCase/2+largCase*i, margeTop-5);
                }
                for(var i=0; i<=10; i++){
                    ctx1.moveTo(margeLeft, margeLeft+largCase*i);
                    ctx1.lineTo(margeLeft+10*largCase, margeLeft+largCase*i);
                    ctx1.stroke();
                }
                    // Colonnes
                for(var i=0; i<10; i++){
                    ctx1.fillText(i, margeLeft-15, margeTop+largCase/2+5+largCase*i);
                }
                for(var i=0; i<=10; i++){
                    ctx1.moveTo(margeLeft+largCase*i, margeTop);
                    ctx1.lineTo(margeLeft+largCase*i, margeTop+10*largCase);
                    ctx1.stroke();
                }\n
"""
if mode >= 1 :      # Grille de l'ordinateur
    html_body += """
                // Dessin de la grille 2
                ctx2.font = "20px Arial";
                ctx2.textAlign = "center";
                    // Lignes
                for(var i=0; i<10; i++){
                    ctx2.fillText(String.fromCharCode(65+i), margeLeft+largCase/2+largCase*i, margeTop-5);
                }
                for(var i=0; i<=10; i++){
                    ctx2.moveTo(margeLeft, margeLeft+largCase*i);
                    ctx2.lineTo(margeLeft+10*largCase, margeLeft+largCase*i);
                    ctx2.stroke();
                }
                    // Colonnes
                for(var i=0; i<10; i++){
                    ctx2.fillText(i, margeLeft-15, margeTop+largCase/2+5+largCase*i);
                }
                for(var i=0; i<=10; i++){
                    ctx2.moveTo(margeLeft+largCase*i, margeTop);
                    ctx2.lineTo(margeLeft+largCase*i, margeTop+10*largCase);
                    ctx2.stroke();
                }\n
"""

# Coloriage des cases
if mode >= 1 :
    for i in range(joueur.grille_joueur.xmax):
        for j in range(joueur.grille_joueur.ymax):
            if joueur.grille_joueur.etat[(i,j)] == 1 :
                html_body += "                  marqueCase(ctx2, %d, %d, 'bateau');\n"%(i,j)
    for i in range(ordi.grille_suivi.xmax):
        for j in range(ordi.grille_suivi.ymax):
            if ordi.grille_suivi.etat[(i,j)] == 1 :
                html_body += "                  marqueCase(ctx2, %d, %d, 'touche');\n"%(i,j)
            elif ordi.grille_suivi.etat[(i,j)] == -1 :
                html_body += "                  marqueCase(ctx2, %d, %d, 'manque');\n"%(i,j)

if mode <= 1 :
    for i in range(joueur.grille_suivi.xmax):
        for j in range(joueur.grille_suivi.ymax):
            if joueur.grille_suivi.etat[(i,j)] == 1 :
                html_body += "              marqueCase(ctx1, %d, %d, 'touche');\n"%(i,j)
            elif joueur.grille_suivi.etat[(i,j)] == -1 :
                html_body += "              marqueCase(ctx1, %d, %d, 'manque');\n"%(i,j)

# Fin du script
html_body += "          </script>\n"

# Informations de partie
html_body += '          <p id="infos">\n'
if first :
    html_body += "              C'est parti !\n"
# Dans le mode 1, à deux joueurs, on ne fait apparaître que les infos essentielles
if mode == 1 :
    joueur.filtre_messages()
    ordi.filtre_messages()
while joueur.messages :
    mess = joueur.messages.pop(0)
    html_body += "              &lt%s&gt "% nom_joueur + mess + " <br>\n"
while ordi.messages :
    mess = ordi.messages.pop(0)
    html_body += "          &lt%s&gt " % nom_ordi + mess + " <br>\n"
html_body += "          </p>\n"
html_body += "      </div>\n"

# Fin de la partie ou coup suivant
if fini :
    # Boutton "Nouvelle partie"
    html_body += """<button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="bn_cgi.py?id=0&mode=%d"'>
        Nouvelle partie
        </button>
        """ % mode
    # Affichage de la boîte du gagnant
    if mode == 0 or (mode == 1 and gagnant == 0) :
        html_body += """<script>alert("Bravo ! Vous avez fini en %d coups.")</script>\n""" % joueur.essais
    elif mode == 2 or (mode == 1 and gagnant == 1) :
        html_body += """<script>alert("%s a fini en %d coups.")</script>\n""" % (nom_ordi, ordi.essais)

    # Suppression de la session
    # (sous windows, les .bak et .dir ne sont pas effacés, c'est totalement incompréhensible...)
    for ext in ["", ".dat", ".bak", ".dir"] :
        try :
            os.remove(os.path.join("sessions", "session_%s%s" % (ID, ext)))
        except :
            pass

else :
    if mode <= 1 :
        # Récupération des événements souris
        html_body += """        <script>
            // Événements souris
            // Inspiré de : http://stackoverflow.com/questions/9880279/how-do-i-add-a-simple-onclick-event-handler-to-a-canvas-element
            var elem = document.getElementById('canvasJoueur'),
                elemLeft = elem.offsetLeft,
                elemTop = elem.offsetTop;
            elem.addEventListener('click', function(event) {
                var x = event.pageX - elemLeft - 12,
                    y = event.pageY - elemTop - 12;
                if (x<margeLeft || x>margeLeft+10*largCase || y<margeTop || y>margeTop+10*largCase){
                    return null;
                }
                jx = coord2case(x,y).i;
                jy = coord2case(x,y).j;
                window.location="bn_cgi.py?id="+sessionID+"&mode=%s"+"&jx="+jx+"&jy="+jy;
            });
        </script>\n""" % mode
    else :
        # Boutton "Coup suivant"
        html_body += """        <button class="boutton" style="margin:auto; margin-top:10px; display:block;" onclick='window.location="bn_cgi.py?id="+sessionID+"&mode=%d"'>
    Coup suivant
    </button>\n""" % mode

    # Sauvegarde de l'état de la partie
    try :
        sh = shelve.open(os.path.join("sessions", "session_%s" % ID))
        sh['joueur']=joueur
        sh['ordi']=ordi
    finally :
        sh.close

# Finalisation de la page
html_body += "  </body>\n"
html_body += "</html>"

def clean_html(texte) :
    """Remplace les accents par leurs équivalents en HTML"""
    convert={'à':'&agrave', 'é':'&eacute', 'è':'&egrave', 'ê':'&ecirc'}
    for char in convert :
        texte = texte.replace(char, convert[char])
    return texte

# Affichage de la page
# --------------------
print(clean_html(html_header))
print(clean_html(html_body))


