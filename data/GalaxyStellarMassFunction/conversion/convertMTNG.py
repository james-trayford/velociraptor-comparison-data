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

input_filename = "../raw/mtng_gsmf.txt"

output_filename = "MillenniumTNG.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()
raw = np.loadtxt(input_filename)

Mstar = raw[:, 0] * unyt.Solar_Mass
Phi = raw[:, 1] * unyt.Mpc ** (-3)

# Meta-data
comment = "Data extracted from fig. 2 of the paper."
citation = "Pakmor et al. (2022) (MTNG)"
bibcode = "2022arXiv221010060P"
name = "GSMF from Millennium-TNG (Fig. 2)"
redshift = 0.0
plot_as = "line"

# Write everything
processed.associate_x(
    Mstar, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Phi,
    scatter=None,
    comoving=True,
    description="Phi (GSMF)",
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
