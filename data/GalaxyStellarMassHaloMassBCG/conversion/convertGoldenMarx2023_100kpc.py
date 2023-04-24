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

output_filename = "GoldenMarx2023_100kpc.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt("../raw/GoldenMarx2023.txt")
M_200 = (10 ** data[:, 0]) * unyt.Solar_Mass

Mstar_100kpc_log = data[:, 7]
Mstar_100kpc = (10 ** Mstar_100kpc_log) * unyt.Solar_Mass
Mstar_100kpc_scatter_log = data[:, 8]

Mstar_100kpc_scatter_low = (10 ** Mstar_100kpc_log - 10 ** (Mstar_100kpc_log - Mstar_100kpc_scatter_log)) * unyt.Solar_Mass
Mstar_100kpc_scatter_high = (10 ** (Mstar_100kpc_log + Mstar_100kpc_scatter_log) - 10 ** Mstar_100kpc_log) * unyt.Solar_Mass
Mstar_100kpc_scatter = unyt.unyt_array((Mstar_100kpc_scatter_low, Mstar_100kpc_scatter_high), units = unyt.Solar_Mass)

# Meta-data
comment = (
    "Halo and stellar masses from Golden-Marx et al. (2023) "
    "(2023MNRAS.521..478G). Stellar masses were converted from Salpeter to "
    "Chabrier through a division by 1.72. Stellar masses were measured in 10, "
    "30, 50 and 100 kpc apertures."
)
citation = "Golden-Marx et al. (2023)"
bibcode = "2023MNRAS.521..478G"
name = "BCG stellar mass-halo mass relation at z=0.4"
plot_as = "points"
redshift = 0.4
redshift_lower = 0.
redshift_upper = 0.8
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_200, scatter=None, comoving=True, description="Halo Mass ($M_{200, {\rm crit}}$)"
)
processed.associate_y(
    Mstar_100kpc, scatter=Mstar_100kpc_scatter, comoving=True, description="Galaxy Stellar Mass"
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
