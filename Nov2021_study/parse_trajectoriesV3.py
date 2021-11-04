#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
from astropy.time import Time

#vsplit = np.vectorize(split)

import glob

RE = 6371.2 # km

file = sys.argv[1]

ephemeris_time_UTC = np.array([])
Rx_km_set          = np.array([])
Ry_km_set          = np.array([])
Rz_km_set          = np.array([])

ephemeris_time_UTC, Rx_km, Ry_km, Rz_km = np.loadtxt(file, unpack=True, delimiter=',', skiprows=1, dtype=str)

# convert input UTC format to something astropy can handle internal (e.g., the iso format)

ephemeris_time_UTC_iso = np.array([])

for t in ephemeris_time_UTC:
	t_split = t.split()

	t_day   = t_split[0]
	t_month = 0
	t_year  = t_split[2]
	t_hms   = t_split[3]

	if t_split[1] == 'Jan':
		t_month = 1
	elif t_split[1] == 'Feb':
		t_month = 2
	elif t_split[1] == 'Mar':
		t_month = 3
	elif t_split[1] == 'Apr':
		t_month = 4
	elif t_split[1] == 'May':
		t_month = 5
	elif t_split[1] == 'Jun':
		t_month = 6
	elif t_split[1] == 'Jul':
		t_month = 7
	elif t_split[1] == 'Aug':
		t_month = 8
	elif t_split[1] == 'Sep':
		t_month = 9
	elif t_split[1] == 'Oct':
		t_month = 10
	elif t_split[1] == 'Nov':
		t_month = 11
	elif t_split[1] == 'Dec':
		t_month = 12

	ephemeris_time_UTC_iso = np.append(ephemeris_time_UTC_iso, t_year + '-' + str(t_month) + '-' + t_day + ' ' + t_hms)

ephemeris_time_UTC_astpy = Time(ephemeris_time_UTC_iso, format='iso', scale='utc')


# IRENE won't take inputs with trajectories larger than 50 Re
mask = np.sqrt(Rx_km.astype(float)**2 + Ry_km.astype(float)**2 + Rz_km.astype(float)**2)/RE < 50. 

filename_out = file[0:-4] + '_IRENE_GEI.txt'
print('saving... ', filename_out)
# https://stackoverflow.com/questions/15192847/saving-arrays-as-columns-with-np-savetxt
np.savetxt(filename_out, np.c_[np.array(ephemeris_time_UTC_astpy.mjd[mask]).astype(float), Rx_km[mask].astype(float), Ry_km[mask].astype(float), Rz_km[mask].astype(float)])