#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

import glob


reduced_directory = './Reduced_IRENE_data/'

for file in glob.glob(reduced_directory + '*Plot_001.txt'):
	print('reading... ', file)

	thickness_mm, electron_dose_rad, proton_dose_rad, total_dose_rad = np.loadtxt(file, unpack=True)

	plt.loglog(thickness_mm, total_dose_rad, label=file)

plt.legend()
plt.title('Dose in Si behind Al Shielding for Various Trajectories')
plt.xlabel('Aluminum Shielding Thickness (mm)')
plt.ylabel('Dose in Silicon (rad)')
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.show()