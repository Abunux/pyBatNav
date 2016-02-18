#!/usr/bin/python3

import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

# Effaçage des sessions antérieures éventuelles
for session in os.listdir("sessions"):
	os.remove(os.path.join("sessions",session))

# Source pour la partie serveur: 
# https://www.safaribooksonline.com/library/view/programming-python-4th/9781449398712/ch01s08.html

webdir = '.'	# Répertoire des pages html et du dossier cgi-bon
port = 8000		# Port

print("Serveur lancé")
print("Page accessible sur http://localhost:8000/index.html")
print("----------------------------------------------------")
print()

os.chdir(webdir)                                       # run in HTML root dir
srvraddr = ("", port)                                  # hostname, port
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()                                # Lance le serveur en démon

