#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

traj_SPENVIS_filename = 'traj_300km-20Re_SPENVIS.txt'
traj_IRENE_filename   = 'traj_300km-20Re_IRENE.txt'

traj_data = np.loadtxt(traj_SPENVIS_filename, unpack=True, skiprows=73, delimiter=',')

traj_data[1,:] += 6371.
traj_data[0,:] += 57023. - traj_data[0,0] # set to Jan 1, 2015 in MJD

np.savetxt(traj_IRENE_filename, traj_data[:4,:].T)