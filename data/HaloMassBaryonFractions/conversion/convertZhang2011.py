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

# correction factors, IMF correction is to go to Chabries (2003)
correction_factor = h_sim / 0.7
b_HSE = 0.74302868
IMF_factor = 0.56

# Data from table 1 from the paper, fstar includes the change to the mass due to IMF change as documented by Chiu+18
raw_data = np.loadtxt("../raw/Zhang2011.txt")
M_500 = raw_data[:, 0] * 1e14
M_500err = raw_data[:, 1] * 1e14
fstar = raw_data[:, 2] * correction_factor ** (-1.5) * IMF_factor
fstar_err = raw_data[:, 3] * correction_factor ** (-1.5) * IMF_factor
Mstar = fstar * M_500
Mstarer = Mstar * np.sqrt((fstar_err / fstar) ** 2 + (M_500 / M_500err) ** 2)
Mgas = raw_data[:, 4] * 1e13
Mgaser = raw_data[:, 5] * 1e13

M_bar = Mgas + Mstar
M_barer = np.sqrt(Mgaser ** 2 + Mstarer ** 2)

f_bar = M_bar / M_500
f_barer = (
    np.abs(f_bar)
    * np.sqrt((M_500err / M_500) ** 2 + (M_barer / M_bar) ** 2)
    * correction_factor ** (-1.5)
)

M_500 *= correction_factor ** (-1)

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
