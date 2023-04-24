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

output_filename = "Gonzalez2013.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Cosmology correction factor
correction_factor = h_sim / 70.2

# Data from table 2 from the paper, fstar includes the change to the mass due to IMF change as documented by Chiu+18
M_500 = np.array(
    [2.26, 5.15, 0.95, 3.46, 3.59, 0.99, 0.95, 3.23, 2.26, 2.41, 2.37, 1.45]
) * correction_factor ** (-1)

M_500err = np.array(
    [0.19, 0.42, 0.10, 0.32, 0.28, 0.11, 0.10, 0.19, 0.23, 0.18, 0.24, 0.21]
) * correction_factor ** (-1)


f_star = (
    np.array(
        [
            0.024,
            0.013,
            0.028,
            0.017,
            0.013,
            0.030,
            0.041,
            0.022,
            0.023,
            0.023,
            0.022,
            0.020,
        ]
    )
    * correction_factor ** (-1.5)
    * 0.76
)

f_starer = (
    np.array(
        [
            0.002,
            0.001,
            0.003,
            0.002,
            0.002,
            0.004,
            0.005,
            0.002,
            0.003,
            0.003,
            0.003,
            0.003,
        ]
    )
    * correction_factor ** (-1.5)
    * 0.76
)

# Convert to proper units
M_500 = unyt.unyt_array(M_500, units="Msun")
M_500_err = unyt.unyt_array(M_500err, units="Msun")
fb_500 = unyt.unyt_array(f_star, units="dimensionless")
error_fb_500_p = unyt.unyt_array(f_starer, units="dimensionless")
error_fb_500_m = error_fb_500_p

# Normalise by the cosmic mean
fb_500 = fb_500 / (Omega_b / Omega_m)
error_fb_500_p = error_fb_500_p / (Omega_b / Omega_m)
error_fb_500_m = error_fb_500_m / (Omega_b / Omega_m)

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((M_500_err, M_500_err))
y_scatter = unyt.unyt_array((error_fb_500_m, error_fb_500_p))

# Meta-data
comment = "Stellar fraction data from the combined X-ray and optical observations"
citation = "Gonzalez et al. (2013)"
bibcode = " 2013ApJ...778...14G"
name = "Gonzalez+13 fstar"
plot_as = "points"
redshift = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_500, scatter=x_scatter, comoving=True, description="Halo mass (M_500)"
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
