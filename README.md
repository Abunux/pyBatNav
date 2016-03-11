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


Lancement en ligne de commande :
--------------------------------
$ ./main.py

$ python3 main.py

Le programme main.py accepte un argument facultatif en ligne de commande pour l'interface :
- ./main.py --console : pour une interface console
- ./main.py --tkinter : pour l'interface graphique
- ./main.py --web : pour l'interface web. Il faut alors ouvrir la page http://localhost:8000/index.html dans son navigateur

Si aucune interface n'est précisée, une menu propose d'en choisir une.

Il est également possible de lancer directement les fichiers :
- bn_console.py
- bn_tkinter.py
- bn_webserveur.py


Important :
-----------
N'ayant que des machines sous Linux à disposition, tout mon développement a été fait sur cette plateforme (Xubuntu 14.04 64bits, Geany et xfce4-terminal 0.6.3). Tout marche impécablement bien (vraiment...).

Par contre il m'a été impossible de tester mon code sous MacOS, et pour les tests sous Windows j'ai du utiliser une machine virtuelle.

Sous Windows il y a quelques problèmes :
- La figure statistique sous pyzo ne marche pas (matplotlib plante, c'est un bug connu). Il faut installer à part matplotlib et numpy et lancer directement "main.py -c"
- Dans l'interface console, si on lance main.py à partir d'un terminal, il plante au moment de lancer une partie. C'est un problème avec les caractères Unicodes, que je n'avais pas sous Linux, dû à la gestion de ces caractères par le terminal Windows. Du coup j'ai rajouté un mode avec des caractères de secours (mais on perd l'encadrement des bateaux).
- Sous PyZo, les caractères unicodes marchent bien (mais c'est très moche car on ne peut pas effacer l'écran).
- J'ai eu quelques soucis avec le script cgi, mais c'est réglé.

Également, en cas de problème avec l'interface web, lire le fichier ALire.txt du dossier interface_web. 
Mais j'ai bien tout testé sous Windows, même avec Internet Explorer, et ça a l'air de bien marcher.

Vous l'aurez compris il vaut mieux, si vous en avez la possibilité, lancer ce programme sous Linux.

 --------------------------------------------------------------------------------------
 |  Surtout en cas de problème, n'hésitez pas à me contacter : maths.muller@gmail.com |
 --------------------------------------------------------------------------------------

(j'ai passé trop de temps sur ce projet pour que ça plante juste pour un problème de plateforme (en plus non libre...))





