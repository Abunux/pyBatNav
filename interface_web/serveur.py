#!/usr/bin/python3

import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

def launch_serveur():
	# Effaçage des sessions antérieures éventuelles
	for session in os.listdir(os.path.join("interface_web","sessions")):
		os.remove(os.path.join("sessions", session))

	# Source pour la partie serveur:
	# https://www.safaribooksonline.com/library/view/programming-python-4th/9781449398712/ch01s08.html

	webdir = './interface_web'	# Répertoire des pages html et du dossier cgi-bin
	#~ webdir = '.'	# Répertoire des pages html et du dossier cgi-bin
	port = 8000		# Port

	print("Serveur lancé")
	print("Page accessible sur http://localhost:8000/index.html")
	print("----------------------------------------------------")
	print()

	os.chdir(webdir)                                       # Répertoire racine HTML
	srvraddr = ("", port)                                  # hostname, port
	srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
	srvrobj.serve_forever()                                # Lance le serveur en démon

if __name__ == "__main__" :
	launch_serveur()
	print("test")
