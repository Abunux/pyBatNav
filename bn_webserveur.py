#!/usr/bin/env python3

import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

# Partie serveur inspirée de :
# https://www.safaribooksonline.com/library/view/programming-python-4th/9781449398712/ch01s08.html

def launch_serveur():
    # On se place dans le répertoire web
    webdir = 'interface_web'
    os.chdir(webdir)
    # Création du serveur
    port = 8000
    serveur_addresse = ("", port)
    serveur = HTTPServer(serveur_addresse, CGIHTTPRequestHandler)

    # Effaçage des sessions antérieures éventuelles
    sessions_path = "sessions"
    if not os.path.exists(sessions_path) :
        print("Création du répertoire de sessions")
        os.makedirs(sessions_path)
    for session in os.listdir(sessions_path):
        try :
            os.remove(os.path.join(sessions_path, session))
        except :
            pass

    # Affichage des infos de lancement
    print()
    print("----------------------------------------------------")
    print("Serveur lancé sur le port %s" % port)
    print("Page accessible sur http://localhost:%s/index.html" % port)
    print("----------------------------------------------------")
    print("""
En cas de problème, si par exemple votre navigateur vous propose de
télécharger le fichier bn_cgi.py, lisez le fichier ALire.txt situé
dans le répertoire interface_web.
Contact : maths.muller@gmail.com
""")
    print("----------------------------------------------------")
    print("\nLog de connexion :\n")

    # Lancement du serveur en mode démon
    # On le stop avec CTRL+C
    serveur.serve_forever()

if __name__ == "__main__" :
    launch_serveur()
