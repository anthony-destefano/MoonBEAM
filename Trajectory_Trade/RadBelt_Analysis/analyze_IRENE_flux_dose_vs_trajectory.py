#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

traj_filename      = 'ephem_sat.dat'
diff_flux_filename = 'Equator_DifferentialFlux_Electron_Proton.txt'
dose_rate_filename = 'Equator_DoseRate_Electron_Proton_Total.txt'



# Read energy levels for electrons and protons from IRENE differential flux plot file
NE_e = 21
NE_p = 25

file = open(diff_flux_filename, 'r')

for i in range(4):
	file.readline()

header = file.readline()
header = header[14:-2].split('\' \'')

E_e = np.char.replace(np.char.replace(header[:NE_e], 'CL_95 Electron Differential Flux at ', ''), ' MeV', '').astype(float)
E_p = np.char.replace(np.char.replace(header[NE_e:], 'CL_95 Proton Differential Flux at ', '')  , ' MeV', '').astype(float)


# Read shielding thicknesses for electrons, protons, and total dose from IRENE dose rate plot file
N_d = 7

file = open(dose_rate_filename, 'r')

for i in range(4):
	file.readline()

header = file.readline()
header = header[14:-2].split('\' \'')

d_e = np.char.replace(np.char.replace(header[:N_d]     , 'CL_95 Electron Dose Rate at ', ''), ' mm', '').astype(float)
d_p = np.char.replace(np.char.replace(header[N_d:2*N_d], 'CL_95 Proton Dose Rate at ', '')  , ' mm', '').astype(float)
d_t = np.char.replace(np.char.replace(header[2*N_d:]   , 'CL_95 Total Dose Rate at ', '')   , ' mm', '').astype(float)

# Read trajectory file

traj_time, traj_x, traj_y, traj_z = np.loadtxt(traj_filename, unpack=True)

traj_time = (traj_time - traj_time[0]) * 24. * 60. # minutes from start

traj_r = np.sqrt(traj_x**2 + traj_y**2 + traj_z**2)


# Read differential flux file

flux_data = np.loadtxt(diff_flux_filename, unpack=True)

flux_time     = flux_data[0,:]
flux_electron = flux_data[1:NE_e,:]
flux_proton   = flux_data[NE_e+1:,:]

plt.semilogy(traj_r, flux_electron.T)
plt.show()

