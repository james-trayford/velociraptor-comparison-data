from velociraptor.observations.objects import ObservationalData

# coding=utf8
import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename_array = [
    "../raw/SE_SNe_rate_vs_gas_metallicity_Graur_2017.txt",
    "../raw/SNII_rate_vs_gas_metallicity_Graur_2017.txt",
]
output_filename_array = [
    "Graur2017_SE_SNe.hdf5",
    "Graur2017_SNII.hdf5",
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
    citation = "Graur et al. (2017)"
    bibcode = "2017ApJ...837..120G"
    if i == 0:
        name = "Gas metallicity - SE SN Rate per Stellar Mass"
    elif i == 1:
        name = "Gas metallicity - SNII Rate per Stellar Mass"
    plot_as = "points"
    redshift = 0.2
    h_obs = 0.7
    h = cosmology.h

    gasZ = unyt.unyt_array(raw.T[0], units="dimensionless")
    SNuM = unyt.unyt_array(raw.T[3] * 1e-12, units="yr**(-1) * Msun**(-1)")

    SNuM_err = unyt.unyt_array(
        [
            raw.T[4] * 1e-12,
            raw.T[5] * 1e-12,
        ],
        units="yr**(-1) * Msun**(-1)",
    )

    gasZ_err = unyt.unyt_array(
        [
            raw.T[1],
            raw.T[2],
        ],
        units="dimensionless",
    )

    processed.associate_x(
        gasZ, scatter=gasZ_err, comoving=False, description="SF Gas 12+log(O/H) from Z"
    )
    processed.associate_y(
        SNuM,
        scatter=SNuM_err,
        comoving=False,
        description="SE SNe rate per stellar mass",
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
