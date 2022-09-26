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

output_filename = "Tachella_2022.hdf5"
output_directory = "../"

# Both in log
mstar = np.array([10.6, 10.2])
mstar_err = np.array([[0.3, 0.2], [0.2, 0.2]])

zstar = np.array([-0.5, -1.3])
zstar_err = np.array([[0.7, 0.4], [0.4, 0.6]])

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
    "Stellar metallicity for two early JWST galaxies at z=8.6, "
    "extracted from SED fits, but using spectroscopic redshifts for "
    "the sources. "
    "Data obtained assuming a Chabrier IMF and h=0.6774. "
)
citation = "Tachella et al. (2022)"
bibcode = "2022ApJ...927..170T"
name = "Stellar mass - stellar metallicity relation "
plot_as = "points"
redshift = 8.67
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
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
