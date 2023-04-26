from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
from astropy.cosmology import FlatLambdaCDM

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h
Omega_b = cosmology.Ob0
Omega_m = cosmology.Om0
FLATCDM = FlatLambdaCDM(H0=cosmology.H0, Om0=cosmology.Om0)

output_filename = "Kravtsov2018.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Cosmology correction factor
correction_factor = h_sim / 0.7

# Data from table 1 from the paper, the BCG + non-BCG column
raw_data = np.loadtxt("../raw/Kravtsov2013.txt")
M_500 = raw_data[:, 0] * 1e14
Mstar = raw_data[:, 1] * 1e12
Mstarer = raw_data[:, 2] * 1e12

f_star = Mstar / M_500
f_starer = Mstarer / M_500

M_500 *= correction_factor ** (-1)

f_star *= correction_factor ** (-1.5)
f_starer *= correction_factor ** (-1.5)

# Convert to proper units
M_500 = unyt.unyt_array(M_500, units="Msun")
fb_500 = unyt.unyt_array(f_star, units="dimensionless")
error_fb_500_p = unyt.unyt_array(f_starer, units="dimensionless")
error_fb_500_m = error_fb_500_p

# Normalise by the cosmic mean
fb_500 = fb_500 / (Omega_b / Omega_m)
error_fb_500_p = error_fb_500_p / (Omega_b / Omega_m)
error_fb_500_m = error_fb_500_m / (Omega_b / Omega_m)

# Define the scatter as offset from the mean value
y_scatter = unyt.unyt_array((error_fb_500_m, error_fb_500_p))

# Meta-data
comment = "Stellar fraction data from the combined X-ray and SDSS observations"
citation = "Kravtsov et al. (2018)"
bibcode = " 2018AstL...44....8K"
name = "Kravtsov+18 fstar"
plot_as = "points"
redshift = 0.05
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_500, scatter=None, comoving=True, description="Halo mass (M_500)"
)
processed.associate_y(
    fb_500, scatter=y_scatter, comoving=True, description="Stellar fraction (<R_500)"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
