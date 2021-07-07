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

input_filename = "../raw/Begum2008.txt"

output_filename = "Begum2008_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
M_star = pow(10.0, raw[:, 0]) * unyt.Solar_Mass * kroupa_to_chabrier_mass
M_HI = pow(10.0, raw[:, 1]) * unyt.Solar_Mass
MHI_per_Mstar = M_HI / M_star

# Meta-data
comment = (
    "Stellar Masses obtained assuming a Kroupa (2001) IMF. "
    "local measurements decoupled from the Hubble flow (no h)."
    "HI measurements via 21cm emission in the FIGGS sample."
)

citation = "Begum et al 2008 (FIGGS)"
bibcode = "2008MNRAS.386.1667B"
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
    scatter=None,
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
