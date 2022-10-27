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
Omega_b = cosmology.Ob0
Omega_m = cosmology.Om0

input_filename = "../raw/mtng_hmsm.txt"

output_filename = "MillenniumTNG_ratio.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()
raw = np.loadtxt(input_filename)

M_200 = raw[:, 0] * unyt.Solar_Mass
ratio = raw[:, 1] * unyt.dimensionless
ratio *= Omega_b / Omega_m

# Meta-data
comment = ()
citation = "Pakmor et al. (2022) (MTNG)"
bibcode = "2022arXiv221010060P"
name = "Stellar mass - halos mass relation from Millennium-TNG (Fig. 2)"
plot_as = "line"
redshift = 0.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_200,
    scatter=None,
    comoving=False,
    description="Halo Mass ($M_{200, {\rm crit}}$)",
)
processed.associate_y(
    ratio,
    scatter=None,
    comoving=True,
    description="Galaxy Stellar Mass / Halo Mass ($M_* / M_{200, {\rm crit}}$)",
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
