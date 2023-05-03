from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h

output_filename = "Gonzalez2013_50kpc.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt("../raw/Gonzalez2013.txt")
M_200 = (10 ** data[:, 0]) * unyt.Solar_Mass
Mstar_50kpc = (10 ** data[:, 1]) * unyt.Solar_Mass

# Meta-data
comment = (
    "Halo and stellar masses from Gonzalez et al. (2013) "
    "(2013ApJ...778...14G). Stellar mass and cosmology corrections are not "
    "needed. Halo masses are defined using the critical overdensity "
    "definition. Stellar mass and cosmology corrections are not "
    "needed. Halo masses were converted from an M_500 to M_200 (critical "
    "overdensity) definition by assuming an NFW profile and concentration of "
    "c=5, which leads to a conversion factor of 1.29. Stellar masses were "
    "measured in 50 kpc projected apertures."
)
citation = "Gonzalez et al. (2013)"
bibcode = "2013ApJ...778...14G"
name = "BCG stellar mass-halo mass relation at z=0.1"
plot_as = "points"
redshift = 0.1
redshift_lower = 0.0
redshift_upper = 0.13
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_200, scatter=None, comoving=True, description="Halo Mass ($M_{200, {\rm crit}}$)"
)
processed.associate_y(
    Mstar_50kpc, scatter=None, comoving=True, description="Galaxy Stellar Mass"
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
