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
correction_factor = h_sim / 70.0

# Data from table 1 from the paper, the non-BCG column
M_500 = np.array([15.6, 10.30, 7, 5.34, 2.35, 1.86, 1.34, 0.46, 0.47]) * 1e14
Mstar = (
    np.array([12.22, 8.21, 5.28, 4.01, 1.89, 2.22, 1.77, 0.97, 0.47]) * 1e12
    + np.array([3.12, 4.14, 3.06, 1.47, 0.79, 1.26, 1.09, 0.91, 1.38]) * 1e12
)

Mstarer = (
    np.sqrt(
        np.array([1.58, 1.05, 0.74, 0.75, 0.49, 0.47, 0.41, 0.29, 0.18]) ** 2
        + np.array([0.36, 0.30, 0.30, 0.13, 0.05, 0.11, 0.06, 0.05, 0.14]) ** 2
    )
    * 1e12
)


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
