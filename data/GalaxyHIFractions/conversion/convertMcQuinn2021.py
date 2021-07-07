from velociraptor.observations.objects import ObservationalData
import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmologies
h_sim = cosmology.h

input_filename = "../raw/McQuinn2021_SHIELD_data.txt"

output_filename = "McQuinn2021_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename, usecols=(1, 2, 3, 4, 5, 6))
M_star = pow(10.0, raw[:, 3]) * unyt.Solar_Mass * kroupa_to_chabrier_mass
M_HI = pow(10.0, raw[:, 0]) * unyt.Solar_Mass
MHI_per_Mstar = M_HI / M_star

MHI_hi = pow(10.0, raw[:, 0] + raw[:, 2]) * unyt.Solar_Mass
MHI_lo = pow(10.0, raw[:, 0] - raw[:, 1]) * unyt.Solar_Mass
Mstar_hi = pow(10.0, raw[:, 3] + raw[:, 5]) * unyt.Solar_Mass * kroupa_to_chabrier_mass 
Mstar_lo = pow(10.0, raw[:, 3] - raw[:, 4]) * unyt.Solar_Mass * kroupa_to_chabrier_mass

y_scatter = (
    unyt.unyt_array(
        [
            np.sqrt(
                ((MHI_hi - M_HI) / M_HI) ** 2 + ((Mstar_hi - M_star) / M_star) ** 2
            ),
            np.sqrt(
                ((MHI_lo - M_HI) / M_HI) ** 2 + ((Mstar_lo - M_star) / M_star) ** 2
            ),
        ]
    )
    * MHI_per_Mstar
)

# Meta-data
comment = (
    "Stellar Masses obtained assuming a Kroupa (2001) IMF. "
    "local measurements decoupled from the Hubble flow (no h)."
    "HI measurements via 21cm emission in the SHIELD sample."
)

citation = "McQuinn et al 2021 (SHIELD)"
bibcode = "2021arXiv210505100M"
name = "Stellar mass - HI Gas to Stellar Mass ratio"
plot_as = "points"
redshift = 0.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    MHI_per_Mstar,
    scatter=y_scatter,
    comoving=True,
    description="Stellar mass - HI Gas to Stellar Mass ratio",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, 0, 2)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
