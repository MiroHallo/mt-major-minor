#!/usr/bin/env python3
# =============================================================================
# PLOT TRINITY OF BEACH-BALLS FROM MAJOR AND MINOR DC-MT DECOMPOSITION
# 
# Author: Miroslav HALLO, Charles University
# E-mail: hallo@karel.troja.mff.cuni.cz
# Revision 2017/02: The first version of the function
# Revision 2018/12: Enhanced version
# Revision 2026/04: New Python version
# Tested with: Python 3.12.3, Matplotlib 3.10.8, NumPy 2.4.4, ObsPy 1.5.0
# Method:
# Hallo,M., Asano,K., Gallovic,F. (2017): Bayesian inference and interpretation
#      of centroid moment tensors of the 2016 Kumamoto earthquake sequence, 
#      Kyushu, Japan, Earth, Planets and Space, 69:134. 
#      https://doi.org/10.1186/s40623-017-0721-4
# Hallo,M., Oprsal,I., Asano,K., Gallovic,F. (2019): Seismotectonics of the 2018
#      Northern Osaka M6.1 earthquake and its aftershocks: joint movements
#      on strike-slip and reverse faults in inland Japan, Earth,
#      Planets and Space, 71:34. https://doi.org/10.1186/s40623-019-1016-8
# 
# Copyright (C) 2017,2018 Miroslav Hallo
# 
# This program is published under the GNU General Public License (GNU GPL).
# 
# This program is free software: you can modify it and/or redistribute it
# or any derivative version under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
# 
# This code is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY. We would like to kindly ask you to acknowledge the authors
# and don't remove their names from the code.
# 
# You should have received copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
# 
# =============================================================================

import matplotlib.pyplot as plt
import numpy as np
from obspy.imaging.beachball import beach as bb

# =============================================================================
# INPUT PARAMETERS
# =============================================================================

# Strike, Dip, Rake of the Full non-DC moment tensor
sdr  = np.array([52.4, 76.8, 163.7])

# Full non-DC moment tensor (Harvard, [M11, M22, M33, M12, M13, M23])
mt  = np.array([[1.1067, 1.5367, -2.6433, 0.26, 0.08, -0.720]])

# Major DC moment tensor (Harvard, [M11, M22, M33, M12, M13, M23])
mt1 = np.array([[0.21921, 1.4434, -1.6626, 0.58336, -0.035697, -0.52161]])

# Minor DC moment tensor (Harvard, [M11, M22, M33, M12, M13, M23])
mt2 = np.array([[0.88745, 0.093313, -0.98077, -0.32336, 0.1157, -0.19839]])

# Scalar seismic moment ratio of the Major DC moment tensor
ra1 = 0.632

# Scalar seismic moment ratio of the Minor DC moment tensor
ra2 = 0.368

# Color of beach-balls
facecolor = 'red'

# =============================================================================
# CODE
# =============================================================================

# Prepare beach-ball size
rat = ra1 + ra2
na1 = ra1/rat * 200
na2 = ra2/rat * 200

# -----------------------------------------------------------------------------
# First figure
outfile = "input_MT.png"

# Plot input non-DC moment tensor
fig = plt.figure(figsize=(5,5))
ax = plt.axes()
plt.axis('off')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
lw = 2
plt.xlim(-100-lw/2, 100+lw/2)
plt.ylim(-100-lw/2, 100+lw/2)
na = 200
full = bb(mt.flatten(), xy=(0, 0), linewidth=lw, facecolor=facecolor, edgecolor='black', zorder=1, width=na)
ax.add_collection(full)
dc_lines = bb(sdr, xy=(0, 0), linewidth=lw/5, facecolor='none', edgecolor='black', zorder=2, nofill=True, width=na)
ax.add_collection(dc_lines)

# Save file
plt.savefig(outfile, bbox_inches='tight', pad_inches=0)
plt.close()

# -----------------------------------------------------------------------------
# Second figure
outfile = "trinity_MT.png"

# Plot trinity of beach-balls
fig = plt.figure(figsize=(15,5))
ax = plt.axes()
plt.axis('off')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
lw=2
plt.xlim(-100-lw/2, 500+lw/2)
plt.ylim(-100-lw/2, 100+lw/2)

full = bb(mt1.flatten(), xy=(0, 0), linewidth=lw, facecolor='black', edgecolor='black', zorder=1, width=na1)
ax.add_collection(full)

full = bb(mt2.flatten(), xy=(200, 0), linewidth=lw, facecolor='black', edgecolor='black', zorder=1, width=na2)
ax.add_collection(full)

full = bb(mt1.flatten()+mt2.flatten(), xy=(400, 0), linewidth=lw, facecolor=facecolor, edgecolor='black', zorder=1)
ax.add_collection(full)
dc_lines = bb(sdr, xy=(400, 0), linewidth=lw/5, facecolor='none', edgecolor='black', zorder=2, nofill=True, width=na)
ax.add_collection(dc_lines)

# Save file
plt.savefig(outfile, bbox_inches='tight', pad_inches=0)
plt.close()