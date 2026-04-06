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

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from obspy.imaging.beachball import beach as bb

# =============================================================================
# CLASSES
# =============================================================================

@dataclass
class TrinityClass:
    sdr: np.ndarray
    mt_full: np.ndarray
    mt_major: np.ndarray
    mt_minor: np.ndarray
    ratio_major: float
    ratio_minor: float
    facecolor: str = 'red'

# =============================================================================
# INPUT PARAMETERS
# =============================================================================

# Strike, Dip, Rake of the Full non-DC moment tensor
# Full non-DC moment tensor (Harvard, [M11, M22, M33, M12, M13, M23])
# Major DC moment tensor (Harvard, [M11, M22, M33, M12, M13, M23])
# Minor DC moment tensor (Harvard, [M11, M22, M33, M12, M13, M23])
# Scalar seismic moment ratio of the Major DC moment tensor
# Scalar seismic moment ratio of the Minor DC moment tensor
# Color of beach-balls

CURRENT_EVENT = TrinityClass(
    sdr      = np.array([52.4, 76.8, 163.7]),
    mt_full  = np.array([1.1067, 1.5367, -2.6433, 0.26, 0.08, -0.720]),
    mt_major = np.array([0.21921, 1.4434, -1.6626, 0.58336, -0.035697, -0.52161]),
    mt_minor = np.array([0.88745, 0.093313, -0.98077, -0.32336, 0.1157, -0.19839]),
    ratio_major = 0.632,
    ratio_minor = 0.368,
    facecolor = 'red',
)

# Output filenames
OUTPUT_FILE_1 = 'input_MT.png'
OUTPUT_FILE_2 = 'trinity_MT.png'

# =============================================================================
# FUNCTIONS
# =============================================================================

# Plot trinity of beach-balls
def plot_bb_trinity(inp: TrinityClass):
    """
    Plot trinity of beach-balls.

    Args:
        inp (TrinityClass): Class containing input parameters for trinity of MTs.
    Returns:
        None
    """
    # Prepare moment tensors
    mt0 = inp.mt_full
    mt1 = inp.mt_major
    mt2 = inp.mt_minor
    
    # Prepare beach-ball size
    rat = inp.ratio_major + inp.ratio_minor
    na1 = inp.ratio_major/rat * 200
    na2 = inp.ratio_minor/rat * 200

    # ------------------------------------
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
    full = bb(mt0.flatten(), xy=(0, 0), linewidth=lw, facecolor=inp.facecolor,
              edgecolor='black', zorder=1, width=na)
    ax.add_collection(full)
    dc_lines = bb(inp.sdr, xy=(0, 0), linewidth=lw/5, facecolor='none',
                  edgecolor='black', zorder=2, nofill=True, width=na)
    ax.add_collection(dc_lines)

    # Save file
    plt.savefig(OUTPUT_FILE_1, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"[+] SUCCESS: Saved to '{OUTPUT_FILE_1}'")

    # ------------------------------------
    # Plot trinity of beach-balls
    fig = plt.figure(figsize=(15,5))
    ax = plt.axes()
    plt.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    lw=2
    plt.xlim(-100-lw/2, 500+lw/2)
    plt.ylim(-100-lw/2, 100+lw/2)

    full = bb(mt1.flatten(), xy=(0, 0), linewidth=lw, facecolor='black',
              edgecolor='black', zorder=1, width=na1)
    ax.add_collection(full)

    full = bb(mt2.flatten(), xy=(200, 0), linewidth=lw, facecolor='black',
              edgecolor='black', zorder=1, width=na2)
    ax.add_collection(full)

    full = bb(mt1.flatten()+mt2.flatten(), xy=(400, 0), linewidth=lw,
              facecolor=inp.facecolor, edgecolor='black', zorder=1, width=na)
    ax.add_collection(full)
    dc_lines = bb(inp.sdr, xy=(400, 0), linewidth=lw/5, facecolor='none',
                  edgecolor='black', zorder=2, nofill=True, width=na)
    ax.add_collection(dc_lines)

    # Save file
    plt.savefig(OUTPUT_FILE_2, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"[+] SUCCESS: Saved to '{OUTPUT_FILE_2}'")


# -----------------------------------------------------------------------------
# Main function
def main():
    """
    Main function for standalone execution (plot trinity of beach-balls).

    - Read moment tensors and the scalar seismic moment ratio from the CURRENT_EVENT.
    - Plot trinity of beach-balls.
    - Save results into the OUTPUT_FILE_1 and OUTPUT_FILE_2.
    """
    print("-" * 50)
    
    print("[*] Plot trinity of beach-balls")
    plot_bb_trinity(CURRENT_EVENT)


# -----------------------------------------------------------------------------
# Entry point
if __name__ == "__main__":
    main()