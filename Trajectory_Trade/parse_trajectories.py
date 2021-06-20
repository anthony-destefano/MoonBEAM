#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

import glob

RE = 6371. # km
#vreplace = np.vectorize(np.char.replace)

directory_list_filename = 'list_of_trajectory_directories.txt'

# https://stackoverflow.com/questions/35617073/python-numpy-how-to-best-deal-with-possible-0d-arrays
directories, separate_segments = np.atleast_1d(np.loadtxt(directory_list_filename, unpack=True, dtype=str))
separate_segments = separate_segments.astype(int)
filename_out = ''

for (cur_directory, is_separate) in zip(directories, separate_segments):
	#plt.figure()

	ephemeris_time_s_set = np.array([])
	julian_date_day_set  = np.array([])
	sim_time_day_set     = np.array([])
	seg_time_day_set     = np.array([])
	Rx_km_set            = np.array([])
	Ry_km_set            = np.array([])
	Rz_km_set            = np.array([])
	Vx_km_s_set          = np.array([])
	Vy_km_s_set          = np.array([])
	Vz_km_s_set          = np.array([])
	mass_kg_s_set        = np.array([])

	for file in glob.glob(cur_directory + '\\*.csv'):
		print('reading... ', file, is_separate)

		if is_separate == 1:
			ephemeris_time_s_set = np.array([])
			julian_date_day_set  = np.array([])
			sim_time_day_set     = np.array([])
			seg_time_day_set     = np.array([])
			Rx_km_set            = np.array([])
			Ry_km_set            = np.array([])
			Rz_km_set            = np.array([])
			Vx_km_s_set          = np.array([])
			Vy_km_s_set          = np.array([])
			Vz_km_s_set          = np.array([])
			mass_kg_s_set        = np.array([])

		ephemeris_time_s, julian_date_day, sim_time_day, seg_time_day, Rx_km, Ry_km, Rz_km, Vx_km_s, Vy_km_s, Vz_km_s, mass_kg = np.loadtxt(file, unpack=True, delimiter=',', skiprows=5, dtype=str)
		# https://www.studytonight.com/numpy/numpy-replace-function
		# https://stackoverflow.com/questions/3877209/how-to-convert-an-array-of-strings-to-an-array-of-floats-in-numpy
		ephemeris_time_s_set = np.append(ephemeris_time_s_set, np.char.replace(ephemeris_time_s, '"', '').astype(float))
		julian_date_day_set  = np.append(julian_date_day_set, np.char.replace(julian_date_day, '"', '').astype(float))
		sim_time_day_set     = np.append(sim_time_day_set, np.char.replace(sim_time_day, '"', '').astype(float))
		seg_time_day_set     = np.append(seg_time_day_set, np.char.replace(seg_time_day, '"', '').astype(float))
		Rx_km_set            = np.append(Rx_km_set, np.char.replace(Rx_km, '"', '').astype(float))
		Ry_km_set            = np.append(Ry_km_set, np.char.replace(Ry_km, '"', '').astype(float))
		Rz_km_set            = np.append(Rz_km_set, np.char.replace(Rz_km, '"', '').astype(float))
		Vx_km_s_set          = np.append(Vx_km_s_set, np.char.replace(Vx_km_s, '"', '').astype(float))
		Vy_km_s_set          = np.append(Vy_km_s_set, np.char.replace(Vy_km_s, '"', '').astype(float))
		Vz_km_s_set          = np.append(Vz_km_s_set, np.char.replace(Vz_km_s, '"', '').astype(float))
		mass_kg_set          = np.append(mass_kg_s_set, np.char.replace(mass_kg, '"', '').astype(float))

		#print(is_separate, is_separate == 1)

		if is_separate == 1:
			filename_out = file[len(cur_directory)+1:-4] + '_IRENE_GEI.txt'
			print('saving... ', filename_out)
			# https://stackoverflow.com/questions/15192847/saving-arrays-as-columns-with-np-savetxt
			np.savetxt(filename_out, np.c_[julian_date_day_set-2400000.5, Rx_km_set, Ry_km_set, Rz_km_set])

	if is_separate == 0:
		filename_out = file[len(cur_directory)+1:-4] + '_IRENE_GEI.txt'
		print('saving... ', filename_out)
		# https://stackoverflow.com/questions/15192847/saving-arrays-as-columns-with-np-savetxt
		np.savetxt(filename_out, np.c_[julian_date_day_set-2400000.5, Rx_km_set, Ry_km_set, Rz_km_set])
		#altitude_km = np.sqrt(Rx_km_set**2 + Ry_km_set**2 + Rz_km_set**2)

		#plt.plot(ephemeris_time_s, altitude_km, label=file)
		#plt.plot(Rx_km_set/RE, Ry_km_set/RE, label=file)

# 	plt.legend()
# plt.show()
