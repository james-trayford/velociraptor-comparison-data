from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/SNIa_rate_vs_SFR_Smith2012.txt"

output_filename = "Smith2012.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()
raw = np.loadtxt(input_filename)

comment = "SDSS-II SN Survey [$0.05<z<0.25$]"
citation = "Smith et al. (2012)"
bibcode = "2012ApJ...755...61S"
name = "Star Formation Rates-SNIa Rate per Stellar Mass"
plot_as = "points"
redshift = 0.15
h_obs = 0.7
h = cosmology.h

SFR = unyt.unyt_array(10 ** raw.T[0], units="Msun/year")
SNuM = unyt.unyt_array(10 ** raw.T[1], units="yr**(-1)")

SNuM_err = unyt.unyt_array(
    [
        10 ** raw.T[1] - 10 ** raw.T[2],
        10 ** raw.T[3] - 10 ** raw.T[1],
    ],
    units="yr**(-1)",
)

dSFR = 0.2

SFR_err = unyt.unyt_array(
    [
        10 ** (raw.T[0]) - 10 ** (raw.T[0] - dSFR),
        10 ** (raw.T[0] + dSFR) - 10 ** (raw.T[0]),
    ],
    units="Msun/year",
)

processed.associate_x(
    SFR, scatter=SFR_err, comoving=True, description="Specific Star Formation rate"
)
processed.associate_y(
    SNuM, scatter=SNuM_err, comoving=False, description="SNIa rate per stellar mass"
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
