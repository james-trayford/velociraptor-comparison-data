from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())


def compute_12_plus_log_O_over_H(Mstar, Z0, M0, beta, gamma):
    """
    Equation 3 from Lewis et al. (2023), which provides a four-parametric fit to
    gas metallicity-stellar mass relation
    """
    return Z0 - gamma / beta * np.log10(1.0 + np.power(Mstar / M0, -beta))


processed = ObservationalData()

comment = (
    "The gas-phase metallicity-Stellar mass relation for massive galaxies around redshift z = 0.7 "
    " from the LEGA-C Survey in the log stellar mass range from 9.81 to 11.1 Msun, "
    "smoothly extended by 0.5 dex to lower stellar masses by additional data at z=0.8 from "
    "the DEEP2 survey (Newman et al. 2013). "
    "Uses Chabrier (2003) initial mass function. "
    "The data includes only star-forming galaxies. "
    "No conversion w.r.t solar metallicity value is needed. "
    "Uses four emission lines ([O ii]l3727, Hgamma, Hbeta, and [O iii]l5007) to identify AGN, "
    "determine nebular extinction, and calculate gas-phase metallicity. "
    "The authors use cosmology with h = 0.7, Omegam = 0.3, and OmegaL = 0.7."
)
citation = "Lewis et al. (2023, LEGA-C+DEEP2)"
bibcode = "2023arXiv230412343L"
name = "Galaxy Stellar Mass - Gas Metallicity"
plot_as = "line"
redshift = 0.7
redshift_lower = 0.4
redshift_upper = 1.0

logMstar_min, logMstar_max = 9.3, 11.1
logMstar = np.linspace(logMstar_min, logMstar_max, 30)
Mstar = 10 ** logMstar

Z0 = 8.74
M0 = 10 ** 10.13  # Msun
gamma = 0.30
beta = 1.99

Metallicity = compute_12_plus_log_O_over_H(
    Mstar=Mstar, Z0=Z0, M0=M0, beta=beta, gamma=gamma
)
Mstar = unyt.unyt_array(Mstar, units=unyt.Msun)
Metallicity = unyt.unyt_array(Metallicity, units=unyt.dimensionless)

processed.associate_x(
    Mstar, scatter=None, comoving=False, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Metallicity,
    scatter=None,
    comoving=False,
    description="Galaxy Gas Metallicity",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, redshift_lower, redshift_upper)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Lewis2023.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
