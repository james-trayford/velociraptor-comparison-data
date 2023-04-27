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

data = np.loadtxt("../raw/Kravstov2018.txt")

# Meta-data
comment = (
    "Halo and stellar masses from Kravstov  et al. (2018) "
    "(2018AstL...44....8K). Stellar mass and cosmology corrections were not "
    "Halo masses were converted from an M_500 to M_200 definition by assuming "
    "needed. an NFW profile and concentration of c=5, which leads to a "
    "conversion factor of 1.29. Stellar masses were measured in 30, 50 and "
    "100 kpc apertures."
)
citation = "Kravstov et al. (2018)"
bibcode = "2018AstL...44....8K"
name = "BCG stellar mass-halo mass relation at z=0.15"
plot_as = "points"
redshift = 0.15
h = h_sim

# Write a separate file for each aperture
apertures = [30, 50, 100]
for x in range(3):
    output_filename = f"Kravstov2018_{apertures[x]}.hdf5"
    output_directory = "../"

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    M_200 = (10 ** data[:, 0]) * unyt.Solar_Mass
    Mstar = (10 ** data[:, 1 + x]) * unyt.Solar_Mass

    # Write everything
    processed = ObservationalData()
    processed.associate_x(
        M_200,
        scatter=None,
        comoving=True,
        description="Halo Mass ($M_{200, {\rm crit}}$)",
    )
    processed.associate_y(
        Mstar, scatter=None, comoving=True, description="Galaxy Stellar Mass"
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
