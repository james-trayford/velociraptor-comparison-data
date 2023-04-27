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

data = np.loadtxt("../raw/Huang2022.txt")

# Meta-data
comment = (
    "Halo and stellar masses from Huang et al. (2022) (2022MNRAS.515.4722H). "
    "Halo masses were converted from M_vir to M_200 definition by assuming "
    "an NFW profile and a concentration of c=5. This leads to a conversion "
    "factor of 0.87. Stellar masses were measured in 10, 30, 50 and 100 kpc "
    "apertures. "
)
citation = "Huang et al. (2022)"
bibcode = "2022MNRAS.515.4722H"
name = "BCG stellar mass-halo mass relation at z=0.4"
plot_as = "line"
redshift = 0.4
redshift_lower = 0.0
redshift_upper = 0.5
h = h_sim

# Write a separate file for each aperture
apertures = [10, 30, 50, 100]
for x in range(4):

    output_filename = f"Huang2022_{apertures[x]}.hdf5"
    output_directory = "../"

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    M_200 = (10 ** data[:, 0]) * unyt.Solar_Mass

    Mstar_log = data[:, 1 + 2 * x]
    Mstar = (10 ** Mstar_log) * unyt.Solar_Mass
    Mstar_scatter_log = data[:, 2 + 2 * x]

    Mstar_scatter_low = (
        10 ** Mstar_log - 10 ** (Mstar_log - Mstar_scatter_log)
    ) * unyt.Solar_Mass
    Mstar_scatter_high = (
        10 ** (Mstar_log + Mstar_scatter_log) - 10 ** Mstar_log
    ) * unyt.Solar_Mass
    Mstar_scatter = unyt.unyt_array(
        (Mstar_scatter_low, Mstar_scatter_high), units=unyt.Solar_Mass
    )

    # Write everything
    processed = ObservationalData()
    processed.associate_x(
        M_200,
        scatter=None,
        comoving=True,
        description="Halo Mass ($M_{200, {\rm crit}}$)",
    )
    processed.associate_y(
        Mstar,
        scatter=Mstar_scatter,
        comoving=True,
        description="Galaxy Stellar Mass",
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
