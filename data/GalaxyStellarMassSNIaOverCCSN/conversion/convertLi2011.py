from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Li2011.txt"

output_filename = "Li2011.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()
raw = np.loadtxt(input_filename)

comment = "Based on the Lick Observatory Supernova Search (LOSS)."
citation = "Li et al. (2011)"
bibcode = "2011MNRAS.412.1473L"
name = "Cosmic CC SN rate"
plot_as = "points"
redshift = 0.0
h_obs = 0.7
h = cosmology.h

Mstar = unyt.unyt_array(10 ** raw.T[0], units="Msun")
SNIa_rate = unyt.unyt_array(raw.T[1], units="yr**(-1) * yr")

SNIa_log_err_up = raw.T[3]
SNIa_log_err_down = raw.T[2]
SNIa_err = unyt.unyt_array(
    [
        SNIa_rate - SNIa_log_err_down,
        SNIa_log_err_up - SNIa_rate,
    ],
    units="yr * yr**(-1)",
)
print(SNIa_err)
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
    SNIa_rate, scatter=SNIa_err, comoving=False, description="SNIa over CC SN rate"
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
