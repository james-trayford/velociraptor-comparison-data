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

data = np.loadtxt("../raw/DeMaio2020.txt")

# Meta-data
comment = (
    "Halo and stellar masses from DeMaio et al. (2020) (2020MNRAS.491.3751D). "
    "Stellar mass and cosmology corrections were not needed. "
    "Halo masses were converted from an M_500 to M_200 definition by assuming "
    "an NFW profile and concentration of c=5, which leads to a conversion "
    "factor of 1.29. "
    "Stellar masses were measured in 10, 50 and 100 kpc apertures. "
)
citation = "DeMaio et al. (2020)"
bibcode = "2020MNRAS.491.3751D"
name = "BCG stellar mass-halo mass relation at z=0.4"
plot_as = "points"
redshift = 0.4
redshift_lower = 0.0
redshift_upper = 0.5
h = h_sim

output_directory = "../"
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

apertures = [10, 50, 100]  # kpc

# Write a separate file for each aperture
for x, aperture in enumerate(apertures):
    output_filename = f"DeMaio2020_{aperture}kpc.hdf5"

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
    processed.associate_redshift(redshift, redshift_lower, redshift_upper)
    processed.associate_plot_as(plot_as)
    processed.associate_cosmology(cosmology)

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
