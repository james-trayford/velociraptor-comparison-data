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

output_filename = "Saglia2016.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt("../raw/Saglia2016.txt")

sigma = (10 ** data[:, 0]) * unyt.kilometer / unyt.s
sigma_log = data[:, 0]
sigma_log_error = data[:, 1]

M_BH = (10 ** data[:, 2]) * unyt.Solar_Mass
M_BH_log = data[:, 2]
M_BH_log_error = data[:, 3]

sigma_scatter_low = (
    10 ** sigma_log - 10 ** (sigma_log - sigma_log_error)
) * unyt.kilometer / unyt.s
sigma_scatter_high = (
    10 ** (sigma_log + sigma_log_error) - 10 ** sigma_log
) * unyt.kilometer / unyt.s
sigma_scatter = unyt.unyt_array(
    (sigma_scatter_low, sigma_scatter_high), units=unyt.kilometer / unyt.s
)

M_BH_scatter_low = (
    10 ** M_BH_log - 10 ** (M_BH_log - M_BH_log_error)
) * unyt.Solar_Mass
M_BH_scatter_high = (
    10 ** (M_BH_log + M_BH_log_error) - 10 ** M_BH_log
) * unyt.Solar_Mass
M_BH_scatter = unyt.unyt_array(
    (M_BH_scatter_low, M_BH_scatter_high), units=unyt.Solar_Mass
)

# Meta-data
comment = (
    "Measured stellar velocity dispersion - black hole mass relation from "
    "Saglia et al. (2016) (2016ApJ...818...47S). The black hole masses were "
    "determined from dynamical measurements, while the line-of-sight velocity "
    "dispersions are weighted (by surface brightness) averages within "
    "projected apertures equal to the half-light radius."
)
citation = "Saglia et al. (2016)"
bibcode = "2016ApJ...818...47S"
name = "Velocity-dispersion - black hole mass relation at z=0."
plot_as = "points"
redshift = 0.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    sigma, scatter=sigma_scatter, comoving=True, description="Stellar velocity dispersion ($R_{\rm e}$ aperture)"
)
processed.associate_y(
    M_BH,
    scatter=M_BH_scatter,
    comoving=True,
    description="Black Hole Mass",
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
