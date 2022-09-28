from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/SNIa_rate_vs_SFR_Graur_2015.txt"

output_filename = "Graur2015.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()
raw = np.loadtxt(input_filename)

comment = "LOSS [$z \\approx 0.075$]"
citation = "Graur et al. (2015)"
bibcode = "2015MNRAS.450..905G"
name = "Star Formation Rates-SNIa Rate per Stellar Mass"
plot_as = "points"
redshift = 0.075
h_obs = 0.7
h = cosmology.h

SFR =  unyt.unyt_array(raw.T[0],units="Msun/year")
SNuM = unyt.unyt_array(raw.T[3]*1e-12,units="yr**(-1) * Msun**(-1)")

SNuM_err = unyt.unyt_array(
    [
        np.sqrt(raw.T[4]**2 + raw.T[5]**2)*1e-12,
        np.sqrt(raw.T[6]**2 + raw.T[7]**2)*1e-12,
    ],
    units="yr**(-1) * Msun**(-1)",
)

SFR_err = unyt.unyt_array(
    [
        raw.T[1],
        raw.T[2],
    ],
    units="Msun/year",
)

processed.associate_x(SFR, scatter=SFR_err, comoving=True, description="Star Formation rate")
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
