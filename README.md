# Major and Minor double-couple decomposition of complex earthquake source
Major and Minor double-couple decomposition preserving the dominant PT-axis
***************************************

  This tool is intended for decomposition of non-double-couple seismic moment 
tensors (MTs) with preserved dominant P- or T-axis. The dominant axis direction 
is preserved for both the major and minor double-couple MTs. The Python script can 
be used for plotting of the trinity of beach-balls.

1 METHODOLOGY
===================

  Hallo, M., Asano, K., Gallovič, F. (2017). Bayesian inference and
interpretation of centroid moment tensors of the 2016 Kumamoto earthquake
sequence, Kyushu, Japan, Earth, Planets and Space, 69:134. [https://doi.org/10.1186/s40623-017-0721-4](https://doi.org/10.1186/s40623-017-0721-4)

  Hallo, M., Opršal, I., Asano, K., Gallovič, F. (2019). Seismotectonics
of the 2018 Northern Osaka M6.1 earthquake and its aftershocks: joint
movements on strike-slip and reverse faults in inland Japan, Earth,
Planets and Space, 71:34. [https://doi.org/10.1186/s40623-019-1016-8](https://doi.org/10.1186/s40623-019-1016-8)

2 TECHNICAL IMPLEMENTATION
===================

Python 3, Matrix Methods, Cross-Platform (Windows, Linux)

The official software version is archived on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19342063.svg)](https://doi.org/10.5281/zenodo.19342063)

3 PACKAGE CONTENT
===================

  a) "maj_min_dc.m" - Matlab codes for computing Major and Minor DC
  decomposition from a given non-DC MT
  
  b) "plot_maj_min_dc.py" - Python code for plotting and saving
  trinity of beach-balls
    
  c) "requirements.txt" - pip requirements file for instalation of dependencies

4 REQUIREMENTS
===================

  MATLAB: Version R2025b, Codes do not require any additional Matlab Toolboxes.
  
  Python: Version 3.12.3 or higher
  
  Libraries: matplotlib, numpy, obspy
  
  Install dependencies via pip:

```bash
pip install -r requirements.txt
```
  
5 COPYRIGHT
===================

Copyright (C) 2017,2018 Miroslav Hallo

This program is published under the GNU General Public License (GNU GPL).

This program is free software: you can modify it and/or redistribute it
or any derivative version under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This code is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY. We would like to kindly ask you to acknowledge the authors
and don't remove their names from the code.

You should have received copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
