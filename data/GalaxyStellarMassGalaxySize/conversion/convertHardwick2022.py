from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_filename = "Vernon.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

bibcode = "2022MNRAS.509.3751H"
name = "Galaxy Stellar Mass-Galaxy Size"
plot_as = "points"
redshift = 0.0
h_obs = 0.7
h = cosmology.h

data = np.loadtxt("../raw/Hardwick2022.txt")

# Stellar mass
log_Mstar = data[:, 1]
Mstar = unyt.unyt_array(10 ** log_Mstar, units=unyt.Solar_Mass)

for i, output_filename, label in zip(
    [2, 0],
    ["Hardwick2022_halfmass.hdf5", "Hardwick2022_halflight.hdf5"],
    ["half-mass", "half-light, r-band"],
):

    comment = (
        f"Galaxy stellar mass-size relation from the eXtended GALEX Arecibo SDSS Survey (xGASS) survey. "
        f"Contains approximately 1200 galaxies in the redshift range 0.01 < z < 0.05 with a flat distribution of stellar "
        f"masses between 10**9 and 10**11.5 Msun. "
        f"Shows the median {label} galaxy size in stellar mass bins of 0.2 dex."
    )

    citation = f"Hardwick et al. (2022) [{label}]"

    # Galaxy sizes (half-mass or half-light)
    log_R = data[:, 2 + i]
    # Errors on the size (error on the median value)
    log_dR = data[:, 3 + i]

    dR_down = 10 ** log_R - 10 ** (log_R - log_dR)
    dR_up = 10 ** (log_R + log_dR) - 10 ** log_R

    R = unyt.unyt_array(10 ** log_R, units=unyt.kpc)
    dR = unyt.unyt_array([dR_down, dR_up], units=unyt.kpc)

    processed.associate_x(
        Mstar, scatter=None, comoving=False, description="Galaxy Stellar Mass"
    )
    processed.associate_y(R, scatter=dR, comoving=False, description="Galaxy size")
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
