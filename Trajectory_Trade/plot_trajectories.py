#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

import glob

RE = 6371.2 # km


for file in glob.glob('*_IRENE_GEI.txt'):
	print('reading... ', file)

	mjd, Rx, Ry, Rz = np.loadtxt(file, unpack=True)

	fig, axs = plt.subplots(2, 2)
	fig.suptitle('Trajectory file: ' + file)
	axs[0, 0].plot(Rx, Ry)
	axs[0, 0].set_title('Ry vs. Rx')
	axs[0, 0].set( ylabel='Ry(km)[J2000-EARTH]')

	axs[0, 1].plot(Rz, Ry, 'tab:orange')
	axs[0, 1].set_title('Ry vs. Rz')
	axs[0, 1].set(xlabel='Rz(km)[J2000-EARTH]')

	axs[1, 0].plot(Rx, Rz, 'tab:green')
	axs[1, 0].set_title('Rz vs. Rx')
	axs[1, 0].set(xlabel='Rx(km)[J2000-EARTH]', ylabel='Rz(km)[J2000-EARTH]')

	# https://stackoverflow.com/questions/44980658/remove-the-extra-plot-in-the-matplotlib-subplot
	axs[1,1].set_axis_off()
	fig.tight_layout()

	plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python

	figure_filename = file[0:-4] + "_traj-plot.png"
	print('saving... ', figure_filename)
	plt.savefig(figure_filename, dpi=800, bbox_inches='tight', pad_inches=0.1)
	# axs[1, 1].plot(x, -y, 'tab:red')
	# axs[1, 1].set_title('Axis [1, 1]')
#plt.show()