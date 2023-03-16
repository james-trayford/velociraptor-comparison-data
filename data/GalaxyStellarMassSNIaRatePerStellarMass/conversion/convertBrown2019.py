from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

variations = [
    ("vol_limited", "_vol_limited", "volume limited"),
    ("full", "_full", "full survey"),
]

for file_prefix, save_prefix, comments in variations:

    input_filename = f"../raw/Brown_2019_{file_prefix}.txt"

    output_filename = f"Brown2019{save_prefix}.hdf5"
    output_directory = "../"

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    processed = ObservationalData()
    raw = np.loadtxt(input_filename)

    comment = f"ASAS-SN [$z \\approx 0.075${comments}]"
    citation = "Brown et al. (2019)"
    bibcode = "2019MNRAS.484.3785B"
    name = "Stellar mass-SNIa Rate per Stellar Mass"
    plot_as = "points"
    redshift = 0.075
    h_obs = 0.7
    h = cosmology.h

    Mstar = unyt.unyt_array(1e10 * 10 ** raw.T[0], units="Msun")
    SNuM = unyt.unyt_array(raw.T[3] * 2e-13, units="yr**(-1) * Msun**(-1)")

    SNuM_err = unyt.unyt_array(
        [
            (raw.T[3] - raw.T[4]) * 2e-13,
            (raw.T[5] - raw.T[3]) * 2e-13,
        ],
        units="yr**(-1) * Msun**(-1)",
    )

    Mstar_err = unyt.unyt_array(
        [
            1e10 * (10 ** raw.T[0] - 10 ** raw.T[1]),
            1e10 * (10 ** raw.T[2] - 10 ** raw.T[0]),
        ],
        units="Msun",
    )

    processed.associate_x(
        Mstar, scatter=Mstar_err, comoving=True, description="Galaxy stellar mass"
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
