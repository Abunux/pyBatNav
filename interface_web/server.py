import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

# Source pour la partie serveur: 
# https://www.safaribooksonline.com/library/view/programming-python-4th/9781449398712/ch01s08.html

# Effaçage des sessions antérieures éventuelles
for session in os.listdir("sessions"):
	os.remove(os.path.join("sessions",session))

webdir = '.'   # where your html files and cgi-bin script directory live
port   = 8000    # default http://localhost/, else use http://localhost:xxxx/

print("Serveur lancé")
print("Page accessible sur http://localhost:8000/index.html")
print("----------------------------------------------------")
print()

os.chdir(webdir)                                       # run in HTML root dir
srvraddr = ("", port)                                  # my hostname, portnumber
srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()                                # run as perpetual daemon

