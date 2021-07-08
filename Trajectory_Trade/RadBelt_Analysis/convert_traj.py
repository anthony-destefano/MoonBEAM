#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

traj_SPENVIS_filename = 'traj_300km-20Re_SPENVIS.txt'
traj_IRENE_filename   = 'traj_300km-20Re_IRENE_solmax.txt'
#traj_IRENE_filename   = 'traj_300km-20Re_IRENE_solmin.txt'

traj_data = np.loadtxt(traj_SPENVIS_filename, unpack=True, skiprows=73, delimiter=',')

traj_data[1,:] += 6371.
traj_data[0,:] += 57023. - traj_data[0,0] # set to Jan 1, 2015 in MJD (near solar max)
#traj_data[0,:] += 54832. - traj_data[0,0] # set to Jan 1, 2009 in MJD (near solar min)


np.savetxt(traj_IRENE_filename, traj_data[:4,:].T)