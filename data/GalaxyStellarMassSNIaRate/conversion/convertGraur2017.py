from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename_array = [
    "../raw/Graur_2017_all.txt",
    "../raw/Graur_2017_passive.txt",
    "../raw/Graur_2017_active.txt",
]
output_filename_array = [
    "Graur2017.hdf5",
    "Graur2017_passive.hdf5",
    "Graur2017_active.hdf5",
]

for i in range(0, len(input_filename_array)):

    input_filename = input_filename_array[i]

    output_filename = output_filename_array[i]
    output_directory = "../"

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    processed = ObservationalData()
    raw = np.loadtxt(input_filename)

    comment = "LOSS [$z \\approx 0.2$]"
    if i == 1:
        comment = "LOSS [$z \\approx 0.2$, passive only]"
    elif i == 2:
        comment = "LOSS [$z \\approx 0.2$, active only]"
    citation = "Graur et al. (2017)"
    bibcode = "2017ApJ...837..120G"
    name = "Stellar mass-SNIa Rate"
    plot_as = "points"
    redshift = 0.2
    h_obs = 0.7
    h = cosmology.h

    Mstar = unyt.unyt_array(1e10 * raw.T[0], units="Msun")
    SNuM = unyt.unyt_array(raw.T[3] * 1e-12 * (1e10 * raw.T[0]), units="yr**(-1)")

    SNuM_err = unyt.unyt_array(
        [
            raw.T[4] * 1e-12 * (1e10 * raw.T[0]),
            raw.T[5] * 1e-12 * (1e10 * raw.T[0]),
        ],
        units="yr**(-1)",
    )

    Mstar_err = unyt.unyt_array(
        [
            1e10 * raw.T[1],
            1e10 * raw.T[2],
        ],
        units="Msun",
    )

    processed.associate_x(
        Mstar, scatter=Mstar_err, comoving=True, description="Galaxy stellar mass"
    )
    processed.associate_y(
        SNuM, scatter=SNuM_err, comoving=False, description="SNIa rate"
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
