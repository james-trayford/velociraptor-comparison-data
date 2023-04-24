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

output_filename = "Zhang2016_30kpc.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt("../raw/Zhang2016.txt")
M_200 = (10 ** data[:, 0]) * unyt.Solar_Mass
Mstar_30kpc = (10 ** data[:, 1]) * unyt.Solar_Mass

# Meta-data
comment = (
    "Halo and stellar masses from Zhang et al. (2016) (2016ApJ...816...98Z). "
    "Stellar mass and cosmology corrections were not needed. "
    "Stellar masses were measured in a 32 kpc aperture, so they are used to "
    "compare with 30 kpc apertures from the simulations."
)
citation = "Zhang et al. (2016)"
bibcode = "2016ApJ...816...98Z"
name = "BCG stellar mass-halo mass relation at z=0.1"
plot_as = "points"
redshift = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_200, scatter=None, comoving=True, description="Halo Mass ($M_{200, {\rm crit}}$)"
)
processed.associate_y(
    Mstar_30kpc, scatter=None, comoving=True, description="Galaxy Stellar Mass"
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
