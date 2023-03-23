
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import special
import pandas as pd

# phi is rotation of virtual x axis in x-y plane, theta is angle rotated about virtual x axis
def plane_change(x, y, z, phi, theta):
	ux = np.cos(phi)
	uy = np.sin(phi)
	# https://en.wikipedia.org/wiki/Rotation_matrix, see Rotation matrix from axis and angle
	x_new = (np.cos(theta) + ux**2*(1.-np.cos(theta))) * x + (ux*uy*(1.-np.cos(theta))) * y + (uy*np.sin(theta)) * z
	y_new = (uy*ux*(1.-np.cos(theta))) * x + (np.cos(theta) + uy**2*(1.-np.cos(theta))) * y + (-1.*ux*np.sin(theta)) * z
	z_new = (-1.*uy*np.sin(theta)) * x + (ux*np.sin(theta)) * y + (np.cos(theta)) * z

	return x_new, y_new, z_new

def r_mod(x, y, z):
	return np.sqrt(x**2 + y**2 + z**2)

def MJD_shift(MJD_0, sec_shift):
	return MJD_0 + sec_shift / (86400.)

max_radius = 15. * 6371. # 15 earth radii, km
#MJD_start = 60676. # noon on Jan 1 of 2025
raw_traj_file = 'MoonBeam_5ARB_alt55_M285_(000)_inertial_traj.csv'

WS = pd.read_csv(raw_traj_file)

t_GEI_sec       = np.array(WS["time (sec)"])
x_GEI_MoonPlane = np.array(WS["rx (km)"])
y_GEI_MoonPlane = np.array(WS["ry (km)"])
z_GEI_MoonPlane = np.array(WS["rz (km)"])

N_tilt = 10
tilt_range = np.linspace(18., 28., N_tilt) / 180. * np.pi # rad
MJD_range  = np.array([58849., 60676.]) # 2020 and 2025

for MJD_i in MJD_range:
	for tilt_range_i in tilt_range:
		new_traj_filename = 'MoonBEAM_trajectory_GEI_MJD_' + str(int(MJD_i)) + '_tilt_' + str(int(np.round(tilt_range_i * 180./np.pi,0))) + '.txt'
		
		print(new_traj_filename)

		x_GEI_EarthPlane, y_GEI_EarthPlane, z_GEI_EarthPlane = plane_change(x_GEI_MoonPlane, y_GEI_MoonPlane, z_GEI_MoonPlane, 0., tilt_range_i)
		t_GEI_MJD = MJD_shift(MJD_i, t_GEI_sec)

		radius_km = r_mod(x_GEI_EarthPlane, y_GEI_EarthPlane, z_GEI_EarthPlane)

		x_GEI_EarthPlane = x_GEI_EarthPlane[radius_km < max_radius]
		y_GEI_EarthPlane = y_GEI_EarthPlane[radius_km < max_radius]
		z_GEI_EarthPlane = z_GEI_EarthPlane[radius_km < max_radius]
		t_GEI_MJD        = t_GEI_MJD[radius_km < max_radius]

		np.savetxt(new_traj_filename, np.c_[t_GEI_MJD, x_GEI_EarthPlane, y_GEI_EarthPlane, z_GEI_EarthPlane])