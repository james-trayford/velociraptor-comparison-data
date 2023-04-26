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

output_filename = "Zhang2011.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Cosmology correction factor
correction_factor = h_sim / 0.7

# Data from table 1 from the paper, fstar includes the change to the mass due to IMF change as documented by Chiu+18

M_500 = (
    np.array(
        [
            6.37,
            1.83,
            1.91,
            1.76,
            0.50,
            4.93,
            3.44,
            6.55,
            3.41,
            0.62,
            14.70,
            1.39,
            1.45,
            11.18,
            7.36,
            4.44,
            2.69,
            7.13,
            3.03,
        ]
    )
    * 1e14
)

M_500err = (
    np.array(
        [
            1.00,
            0.39,
            0.58,
            0.27,
            0.14,
            0.98,
            0.66,
            0.79,
            0.63,
            0.12,
            2.61,
            0.28,
            0.34,
            1.78,
            1.25,
            0.67,
            0.42,
            1.38,
            0.75,
        ]
    )
    * 1e14
)

fstar = (
    np.array(
        [
            0.0115,
            0.0240,
            0.0239,
            0.0247,
            0.0233,
            0.0143,
            0.0217,
            0.0201,
            0.0182,
            0.0259,
            0.0065,
            0.0254,
            0.0268,
            0.0065,
            0.0114,
            0.0154,
            0.0177,
            0.0095,
            0.0169,
        ]
    )
    * correction_factor ** (-1.5)
    * 0.56
)

fstar_err = (
    np.array(
        [
            0.0012,
            0.0039,
            0.0039,
            0.0028,
            0.0040,
            0.0017,
            0.0026,
            0.0018,
            0.0022,
            0.0031,
            0.0007,
            0.0030,
            0.0035,
            0.0006,
            0.0011,
            0.0015,
            0.0017,
            0.0011,
            0.0023,
        ]
    )
    * correction_factor ** (-1.5)
    * 0.56
)

Mstar = fstar * M_500
Mstarer = Mstar * np.sqrt((fstar_err / fstar) ** 2 + (M_500 / M_500err) ** 2)

Mgas = (
    np.array(
        [
            8.13,
            1.36,
            1.45,
            2.07,
            0.47,
            6.10,
            5.09,
            8.42,
            5.11,
            0.80,
            13.35,
            1.86,
            2.13,
            7.66,
            13.76,
            5.04,
            2.97,
            7.11,
            2.54,
        ]
    )
    * 1e13
)

Mgaser = (
    np.array(
        [
            0.38,
            0.05,
            0.26,
            0.07,
            0.02,
            0.29,
            0.73,
            0.63,
            0.14,
            0.12,
            0.53,
            0.10,
            0.09,
            1.44,
            0.73,
            0.53,
            0.30,
            0.33,
            0.17,
        ]
    )
    * 1e13
)

M_bar = Mgas + Mstar
M_barer = np.sqrt(Mgaser ** 2 + Mstarer ** 2)

f_bar = M_bar / M_500
f_barer = (
    np.abs(f_bar)
    * np.sqrt((M_500err / M_500) ** 2 + (M_barer / M_bar) ** 2)
    * correction_factor ** (-1.5)
)


# Convert to proper units
M_500 = unyt.unyt_array(M_500, units="Msun")
M_500_err = unyt.unyt_array(M_500err, units="Msun")
fb_500 = unyt.unyt_array(f_bar, units="dimensionless")
error_fb_500_p = unyt.unyt_array(f_barer, units="dimensionless")
error_fb_500_m = error_fb_500_p

# Normalise by the cosmic mean
fb_500 = fb_500 / (Omega_b / Omega_m)
error_fb_500_p = error_fb_500_p / (Omega_b / Omega_m)
error_fb_500_m = error_fb_500_m / (Omega_b / Omega_m)

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((M_500_err, M_500_err))
y_scatter = unyt.unyt_array((error_fb_500_m, error_fb_500_p))

# Meta-data
comment = "Baryon fraction data from the combined X-ray and optical observations"
citation = "Zhang et al. (2011)"
bibcode = "2011A&A...535A..78Z"
name = "Zhang+11 fbar"
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
