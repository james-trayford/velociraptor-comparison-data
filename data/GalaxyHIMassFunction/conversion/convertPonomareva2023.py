from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

ORIGINAL_H = 0.674

# Exec the master cosmology file passed as first argument
# These lines are _required_ and you are required to use
# the cosmology specified (this is an astropy.cosmology
# instance)
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Ponomareva2023.txt"
output_filename = "Ponomareva2023.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.genfromtxt(input_filename, comments="#")

processed = ObservationalData()

comment = (
    "The HI mass function from the MeerKAT telescope's data based on 276 direct detections from "
    "the MIGHTEE Survey Early Science data covering redshifts 0 < z < 0.084. "
    "Uses the Planck Collaboration et al. (2020) cosmology: h = 0.674, Omegam = 0.315, "
    "and OmegaL = 0.685. "
    "The authors define a critical HI line flux above which the sample is expected to be 100 complete. This leaves "
    "them with 203 sources from which the HI mass function is subsequently constructed."
)

citation = "Ponomareva et al. (2023, MIGHTEE)"
bibcode = "2023MNRAS.tmp.1270P"
name = "HI mass function from the MIGHTEE Survey at z=0"
plot_as = "points"
redshift = 0.0
h = cosmology.h

M = 10 ** data[:, 0] * (h / ORIGINAL_H) ** (-2) * unyt.Solar_Mass
# no error in M_HI provided
M_err = np.row_stack([M.value * 0.0] * 2) * M.units

Phi = 10 ** data[:, 1] * (h / ORIGINAL_H) ** 3
Phi_err_p = 10 ** (data[:, 1] + data[:, 2]) * (h / ORIGINAL_H) ** 3 - Phi
Phi_err_m = Phi - 10 ** (data[:, 1] - data[:, 3]) * (h / ORIGINAL_H) ** 3
Phi = unyt.unyt_array(Phi, units="1/Mpc**3")
Phi_err = unyt.unyt_array([Phi_err_m, Phi_err_p], units="1/Mpc**3")


processed.associate_x(M, scatter=M_err, comoving=True, description="Galaxy HI Mass")
processed.associate_y(Phi, scatter=Phi_err, comoving=True, description="Phi (HIMF)")
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
