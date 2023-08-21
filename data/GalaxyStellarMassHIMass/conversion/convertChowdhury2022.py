from velociraptor.observations.objects import ObservationalData

import unyt
import os
import sys

ORIGINAL_H = 0.7

unitless = unyt.dimensionless

# Exec the master cosmology file passed as first argument
# These lines are _required_ and you are required to use
# the cosmology specified (this is an astropy.cosmology
# instance)
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_filename = "Chowdhury2022.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

citation = "Chowdhury et al. (2022)"
comment = (
    "Average HI mass versus stellar mass relation at 0.74<z<1.45 for star-forming galaxies in two "
    "different stellar mass bins. The data was obtained with Giant Metrewave Radio Telescope (GMRT), "
    "based stacking of HI 21cm signals from different galaxies. "
    "In total, there are 11,419 main-sequence galaxies. "
    "Corrected for h (the authors use h=0.7)."
)
bibcode = "2022ApJ...931L..34C"
name = "Galaxy HI mass vs stellar mass relation at z=1.1"
plot_as = "points"
redshift = 1.1
redshift_lower, redshift_upper = 0.74, 1.45
h = cosmology.h

h_corr_factor = pow(h / ORIGINAL_H, -2.0)

processed = ObservationalData()

# The two data points are taken from Table 1, columns 1 and 2 (Stellar-mass Subsamples)
Mstar = unyt.unyt_array([4.9e9, 21.4e9], "Msun") * h_corr_factor
Mstar_p = unyt.unyt_array([10.0e9, 240.0e9], "Msun") * h_corr_factor
Mstar_m = unyt.unyt_array([1.0e9, 10.0e9], "Msun") * h_corr_factor

Delta_Mstar_p = Mstar_p - Mstar
Delta_Mstar_m = Mstar - Mstar_m

M_HI = unyt.unyt_array([10.4e9, 16.3e9], "Msun") * h_corr_factor
Delta_M_HI = unyt.unyt_array([2.1e9, 3.5e9], "Msun") * h_corr_factor

processed.associate_x(
    Mstar,
    scatter=unyt.unyt_array([Delta_Mstar_m, Delta_Mstar_p]),
    comoving=False,
    description="Average stellar mass",
)
processed.associate_y(
    M_HI,
    scatter=Delta_M_HI,
    comoving=False,
    description="Average HI mass",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, redshift_lower, redshift_upper)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
