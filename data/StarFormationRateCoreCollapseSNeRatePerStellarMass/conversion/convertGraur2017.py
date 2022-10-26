from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

variations = [
    ("SE_SNe", "SE SN Rate per Stellar Mass"),
    ("SNII", "SNII Rate per Stellar Mass"),
]

for file_prefix, description in variations:

    input_filename = f"../raw/{file_prefix}_rate_vs_SFR_Graur_2017.txt"

    output_filename = f"Graur2017_{file_prefix}.hdf5"
    output_directory = "../"

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    processed = ObservationalData()
    raw = np.loadtxt(input_filename)

    comment = "LOSS [$z \\approx 0.2$]"
    citation = "Graur et al. (2017)"
    bibcode = "2017ApJ...837..120G"
    name = f"Star Formation Rates - {description}"
    plot_as = "points"
    redshift = 0.2
    h_obs = 0.7
    h = cosmology.h

    SFR = unyt.unyt_array(10 ** raw.T[0], units="Msun/year")
    SNuM = unyt.unyt_array(raw.T[3] * 1e-12, units="yr**(-1) * Msun**(-1)")

    SNuM_err = unyt.unyt_array(
        [
            raw.T[4] * 1e-12,
            raw.T[5] * 1e-12,
        ],
        units="yr**(-1) * Msun**(-1)",
    )

    SFR_err = unyt.unyt_array(
        [
            10 ** (raw.T[0]) - 10 ** (raw.T[0] - raw.T[1]),
            10 ** (raw.T[0] + raw.T[2]) - 10 ** (raw.T[0]),
        ],
        units="Msun/year",
    )

    processed.associate_x(
        SFR, scatter=SFR_err, comoving=True, description="Star Formation rate"
    )
    processed.associate_y(
        SNuM,
        scatter=SNuM_err,
        comoving=False,
        description=description,
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
