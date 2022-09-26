from velociraptor.observations.objects import ObservationalData

import unyt
import os
import sys
import csv
import numpy as np

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h

output_filename = "Furtak_2022.hdf5"
output_directory = "../"

# Both in log
mstar = np.array(
    [
        9.03,
        9.81,
        9.80,
        7.41,
        7.24,
        7.43,
        7.43,
        7.64,
        7.20,
        8.08,
        7.21,
        8.14,
        8.10,
        8.31,
        8.00,
    ]
)
mstar_err = np.array(
    [
        [0.23, 0.23],
        [0.07, 0.07],
        [0.20, 0.08],
        [0.97, 0.77],
        [0.92, 1.13],
        [0.97, 1.00],
        [0.10, 1.18],
        [1.26, 1.15],
        [1.09, 1.35],
        [1.48, 1.32],
        [0.93, 1.15],
        [1.42, 0.54],
        [1.55, 0.85],
        [1.33, 0.39],
        [1.53, 1.23],
    ]
)


zstar = np.array(
    [
        -1.82,
        -0.31,
        -1.84,
        -0.92,
        -0.84,
        -1.06,
        -0.59,
        -0.79,
        -1.43,
        -1.32,
        -1.11,
        -1.30,
        -1.02,
        -1.16,
        -1.00,
    ]
)
zstar_err = np.array(
    [
        [0.10, 0.24],
        [0.01, 0.01],
        [0.11, 0.81],
        [0.23, 0.25],
        [0.25, 0.36],
        [0.25, 0.18],
        [0.23, 0.20],
        [0.23, 0.29],
        [0.25, 0.24],
        [0.46, 0.59],
        [0.47, 0.35],
        [0.48, 0.55],
        [0.51, 0.53],
        [0.26, 0.36],
        [0.67, 0.43],
    ]
)

Zsun = 0.0142

Mstar_arr = unyt.unyt_array(10 ** mstar, units="Msun")
Zstar_arr = unyt.unyt_array(Zsun * 10 ** zstar, units="dimensionless")

Mstar_arr_err = unyt.unyt_array(
    [
        10 ** mstar - 10 ** (mstar - mstar_err[:, 0]),
        10 ** (mstar + mstar_err[:, 1]) - 10 ** mstar,
    ],
    units="Msun",
)

Zstar_arr_err = (
    unyt.unyt_array(
        [
            10 ** zstar - 10 ** (zstar - zstar_err[:, 0]),
            10 ** (zstar + zstar_err[:, 1]) - 10 ** zstar,
        ],
        units="dimensionless",
    )
    * Zsun
)

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Meta-data
comment = (
    "Stellar metallicity for 15 early JWST galaxies at z=10-16, lensed by "
    "SMACS J0723.3-7327 extracted from SED fits, with fits using BEAGLE. "
    "Data obtained assuming a Chabrier IMF and h=0.6774. "
)
citation = "Furtak1 et al. (2022)"
bibcode = "2022arXiv220805473F"
name = "Stellar mass - stellar metallicity relation "
plot_as = "points"
redshift = 12
z_min = 10.0
z_max = 16.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    Mstar_arr, scatter=Mstar_arr_err, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Zstar_arr, scatter=Zstar_arr_err, comoving=True, description="Stellar metallicity"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, [10.0, 16.0])
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
