from bn_grille import *

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

# Intégration de matplotlib dans tkinter : 
# http://matplotlib.org/examples/user_interfaces/embedding_in_tk.html

def surface_probas(n=1000, grille = GrilleSuivi()):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.view_init(elev=24., azim=106)

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Probabilités', rotation=180)
	labels = [chr(65+i) for i in range(10)]
	ax.set_xticklabels(labels)
	ax.invert_xaxis()

	# Divers réglages graphiques peu concluants...
	#~ ax.w_xaxis.pane.set_visible(False)
	#~ ax.w_xaxis.gridlines.set_visible(False)
	#~ ax.w_xaxis.line.set_visible(False)
	#~ ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
	#~ ax.set_axis_off()

	#~ grille.etat[(2,3)] = -1 # Petite variation sur la grille
	start = time()
	(case, pmax) = grille.case_max(n, ordre='decroissant')
	print("Temps : %.5f secondes" % (time()-start))
	
	ax.text(case[0],case[1],pmax,"Pmax=%.3f en %s" % (pmax, alpha(case)), ha="center")
	ax.set_title("Échantillon de taile %d" % n)
	x = y = np.arange(0, 10, 1)
	X, Y = np.meshgrid(x, y)
	zs = np.array([grille.probas[(i,j)] for i,j in zip(np.ravel(X), np.ravel(Y))])
	Z = zs.reshape(X.shape)

	# Couleurs : http://matplotlib.org/examples/color/colormaps_reference.html
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.7)
	#~ surf2 = ax.plot_wireframe(X, Y, Z)

	fig.colorbar(surf, shrink=0.5, aspect=5)
	plt.show()

if __name__ == "__main__" :
	#~ taille_bateaux=[2,3,3,4,5]
	#~ surface_probas(n=100000, grille=GrilleSuivi(taille_bateaux=taille_bateaux))
	grille=GrilleSuivi()
	#~ for i in range(7):
		#~ for j in range(10):
			#~ grille.etat[(i,j)]=-1
	#~ for k in range(20):
		#~ grille.etat[(rand.randrange(0, grille.xmax), rand.randrange(0, grille.ymax))] = -1
	surface_probas(n=10000, grille=grille)
