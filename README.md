# pyBatNav
     ╔══════════════════════════════════════════════════════════════════╗
     ║                                                                  ║
     ║   ██████╗  █████╗ ████████╗ █████╗ ██╗██╗     ██╗     ███████╗   ║
     ║   ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██║██║     ██║     ██╔════╝   ║
     ║   ██████╔╝███████║   ██║   ███████║██║██║     ██║     █████╗     ║
     ║   ██╔══██╗██╔══██║   ██║   ██╔══██║██║██║     ██║     ██╔══╝     ║
     ║   ██████╔╝██║  ██║   ██║   ██║  ██║██║███████╗███████╗███████╗   ║
     ║   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝   ║
     ║                                                                  ║
     ║        ███╗   ██╗ █████╗ ██╗   ██╗ █████╗ ██╗     ███████╗       ║
     ║        ████╗  ██║██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝       ║
     ║        ██╔██╗ ██║███████║██║   ██║███████║██║     █████╗         ║
     ║        ██║╚██╗██║██╔══██║╚██╗ ██╔╝██╔══██║██║     ██╔══╝         ║
     ║        ██║ ╚████║██║  ██║ ╚████╔╝ ██║  ██║███████╗███████╗       ║
     ║        ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚══════╝       ║
     ║                                                                  ║
     ╚══════════════════════════════════════════════════════════════════╝

             Projet de formation ISN 2015/2016 de l'académie de Lyon
                Auteur : Frédéric Muller
                Code du projet : https://github.com/Abunux/pyBatNav
                Licence Creative Common CC BY-NC-SA
                Projet démarré le 14/11/2015


Lancement :
-----------
Il y a pas mal de problèmes avec pyzo. Il a un bug connu avec matplotlib, son affichage console n'est pas terrible et il y a des problèmes avec les polices en tkinter. 
Il est donc fortement conseillé de lancer le programme main.py directement dans une console :

soit avec : $ ./main.py

soit avec : $ python3 main.py

Le programme main.py accepte un argument facultatif en ligne de commande pour l'interface :
- ./main.py --console : pour une interface console
- ./main.py --tkinter : pour l'interface grpahique
- ./main.py --web : pour l'interface web. Il faut alors ouvrir la page http://localhost:8000/index.html dans son navigateur

Si aucune interface n'est précisée, une menu propose d'en choisir une.

Il est également possible de lancer directement les fichiers :
- bn_console.py
- bn_tkinter.py
- bn_webserveur.py

Imortant :
----------
N'ayant que des machines sous Linux à disposition, il m'a été impossible de tester mon code sous Windows, ni sous MacOS.

J'espère qu'il fonctionne sous ces systèmes (il devrait en théorie)

En cas de problème avec l'interface web, lire le fichier ALire.txt du dossier interface_web
