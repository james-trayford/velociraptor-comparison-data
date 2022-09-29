from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_filename = "Kistler2014.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

comment = "LOSS"
citation = "Kistler et al. (2013)"
bibcode = "2013ApJ...770...88K"
name = "Galaxy Stellar Mass-SNIa Rate per Stellar Mass"
plot_as = "line"
redshift = 0.0
h_obs = 0.7
h = cosmology.h

Mstar = unyt.unyt_array(np.logspace(9, 12), units="Msun")

alpha = 5e-3
beta = 4.2e-4
Mcal = 10
omega = 0.33

rate = (
    alpha * (1.0 + np.exp((np.log10(Mstar / unyt.Msun) - Mcal) / omega)) ** (-1) + beta
)

SNIa_rate = unyt.unyt_array(rate * np.logspace(9, 12) / 1e10, units="yr**(-1)")


processed.associate_x(
    Mstar, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(SNIa_rate, scatter=None, comoving=False, description="SNIa rate")
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
