from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Wiseman2021.txt"

output_filename = "Wiseman2021.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()
raw = np.loadtxt(input_filename)

comment = "DES [$0.2 <z <0.6$]"
citation = "Wiseman et al. (2021)"
bibcode = "2021MNRAS.506.3330W"
name = "Galaxy Stellar Mass-SNIa rate"
plot_as = "points"
redshift = 0.5
h_obs = 0.7
h = cosmology.h

Mstar = unyt.unyt_array(10 ** raw.T[0], units="Msun")
SNIa_rate = unyt.unyt_array(10 ** raw.T[1], units="yr**(-1)")

SNIa_log_err = raw.T[2]
SNIa_err = unyt.unyt_array(
    [
        10 ** raw.T[1] - 10 ** (raw.T[1] - SNIa_log_err),
        10 ** (raw.T[1] + SNIa_log_err) - 10 ** raw.T[1],
    ],
    units="yr**(-1)",
)
dMstar = 0.25 / 2.0
Mstar_err = unyt.unyt_array(
    [
        10 ** (raw.T[0]) - 10 ** (raw.T[0] - dMstar),
        10 ** (raw.T[0] + dMstar) - 10 ** (raw.T[0]),
    ],
    units="Msun",
)

processed.associate_x(
    Mstar, scatter=Mstar_err, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    SNIa_rate, scatter=SNIa_err, comoving=False, description="SNIa rate"
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
