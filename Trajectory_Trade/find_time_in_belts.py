#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

import glob

#percent_of_max = float(sys.argv[1])

reduced_directory = './Reduced_IRENE_data/'

for file in glob.glob(reduced_directory + '*Plot_004.txt'):
	print('reading... ', file)

	data = np.loadtxt(file, unpack=True)

	time_minute = data[0,:]
	relative_net_flux = np.sum(data[1:,:], axis=0)

	#print(np.shape(time_minute), np.shape(relative_net_flux))

	time_in_belts = 0.
	for i in range(np.shape(time_minute)[0]-1):
		if relative_net_flux[i] > 0. and relative_net_flux[i+1] > 0.:
			time_in_belts += time_minute[i+1] - time_minute[i]

	print(time_in_belts, ' mins | ', time_in_belts/time_minute[-1]*100., ' percent of trajectory in belts\n')