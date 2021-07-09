#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt


# python analyze_IRENE_flux_dose_vs_trajectory.py traj_300km-20Re_IRENE_solmax.txt Equator3_DifferentialFlux_Electron_Proton.txt Equator3_DoseRate_Electron_Proton_Total.txt "20 Orbits during Solar Max at 95% confidence level"
# python analyze_IRENE_flux_dose_vs_trajectory.py traj_300km-20Re_IRENE_solmin.txt Equator4_DifferentialFlux_Electron_Proton.txt Equator4_DoseRate_Electron_Proton_Total.txt "20 Orbits during Solar Min at 95% confidence level"

def get_dose_at_time(t, fdose_time, fdose):
	for i in range(np.shape(fdose_time)[0]):
		if t < fdose_time[i]:
			return (fdose[i]-fdose[i-1]) * (t - fdose_time[i-1]) / (fdose_time[i] - fdose_time[i-1]) + fdose[i-1]

	return 0.

# https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html
vget_dose_at_time = np.vectorize(get_dose_at_time, excluded=['fdose_time','fdose'])
# https://www.w3resource.com/numpy/string-operations/add.php
vadd = np.vectorize(np.char.add)

traj_filename      = sys.argv[1]
diff_flux_filename = sys.argv[2]
dose_rate_filename = sys.argv[3]
fig_subtitle       = sys.argv[4]

Re = 6731. # km

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

flux_time     = flux_data[0,:] # min
flux_electron = flux_data[1:NE_e+1,:]
flux_proton   = flux_data[NE_e+1:,:]

# Read dose rate file

dose_data = np.loadtxt(dose_rate_filename, unpack=True)

dose_time     = dose_data[0,:] # min
dose_electron = dose_data[1:N_d+1,:]
dose_proton   = dose_data[N_d+1:2*N_d+1,:]
dose_total    = dose_data[2*N_d+1:,:]


for i in range(N_d):
	plt.semilogy(traj_r/Re, vget_dose_at_time(flux_time, fdose_time=dose_time, fdose=dose_electron[i]), label='Al shielding = ' + str(d_e[i]) + ' mm')

plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.xlabel('Distance from Earth Center (Re)')
plt.ylabel('Electron Dose Rate (rads/sec)')
plt.title('Electron Dose Rate vs. Orbit Distance\n' + fig_subtitle)
plt.legend()
plt.savefig('RadBelt_Electron_Dose_Rate_' + traj_filename[:-4] + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
for i in range(N_d):
	plt.semilogy(traj_r/Re, vget_dose_at_time(flux_time, fdose_time=dose_time, fdose=dose_proton[i]), label='Al shielding = ' + str(d_p[i]) + ' mm')

plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.xlabel('Distance from Earth Center (Re)')
plt.ylabel('Proton Dose Rate (rads/sec)')
plt.title('Proton Dose Rate vs. Orbit Distance\n' + fig_subtitle)
plt.legend()
plt.savefig('RadBelt_Proton_Dose_Rate_' + traj_filename[:-4] + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure()
for i in range(N_d):
	plt.semilogy(traj_r/Re, vget_dose_at_time(flux_time, fdose_time=dose_time, fdose=dose_total[i]), label='Al shielding = ' + str(d_p[i]) + ' mm')

plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.xlabel('Distance from Earth Center (Re)')
plt.ylabel('Total Dose Rate (rads/sec)')
plt.title('Total Dose Rate vs. Orbit Distance\n' + fig_subtitle)
plt.legend()
plt.savefig('RadBelt_Total_Dose_Rate_' + traj_filename[:-4] + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure(figsize=(6.4, 8))
curplot = plt.semilogy(traj_r/Re, flux_electron.T)
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.xlabel('Distance from Earth Center (Re)')
plt.ylabel(r'Electron Differential Flux (#/cm$^2$/MeV/sec)')
plt.title('Electron Differential Flux vs. Orbit Distance\n' + fig_subtitle)
elabel = vadd(E_e.astype(str), ' MeV')
plt.legend(curplot, elabel)
plt.savefig('RadBelt_Electron_Diff_Flux_' + traj_filename[:-4] + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.figure(figsize=(6.4, 8))
curplot = plt.semilogy(traj_r/Re, flux_proton.T)
plt.grid(b=True, which='both') # https://stackoverflow.com/questions/9127434/how-to-create-major-and-minor-gridlines-with-different-linestyles-in-python
plt.xlabel('Distance from Earth Center (Re)')
plt.ylabel(r'Proton Differential Flux (#/cm$^2$/MeV/sec)')
plt.title('Proton Differential Flux vs. Orbit Distance\n' + fig_subtitle)
plabel = vadd(E_p.astype(str), ' MeV')
plt.legend(curplot, plabel)
plt.savefig('RadBelt_Proton_Diff_Flux_' + traj_filename[:-4] + '.png', dpi=800, bbox_inches='tight', pad_inches=0.1)

plt.show()

