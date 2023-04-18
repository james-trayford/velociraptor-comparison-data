from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Bollo2023.txt"

processed = ObservationalData()
raw = np.loadtxt(input_filename)

comment = (
    r"H\alpha luminosity function derived from a large sample of Lyman break galaxies around z=4.5 over "
    r"the GOODS-South and North fields. Uses Chabrier (2003) initial mass function. Stellar population models are "
    r"from Bruzual & Charlot (2003). Assumes metallicity of 0.2 Zsolar. "
    r"The cosmological parameters in this work are H0 = 70 kms−1 Mpc−1, Omega_m = 0.3, and Omega_lambda = 0.7."
)
citation = "Bollo et al. (2023)"
bibcode = "2023arXiv230405034B"
name = "Cosmic Star Formation Rate Density function around z=4.5"
plot_as = "points"

h_obs = 0.7
h_sim = cosmology.h

log10SFR = raw[:, 0]  # in units of Msun/yr
Phi_SFR = raw[:, 1] * (h_sim / h_obs) ** 3  # in units of 10−3 Mpc−3
delta_Phi_SFR_m = raw[:, 2] * (h_sim / h_obs) ** 3  # in units of 10−3 Mpc−3
delta_Phi_SFR_p = raw[:, 3] * (h_sim / h_obs) ** 3  # in units of 10−3 Mpc−3
SFR = (10.0 ** log10SFR) * (h_sim / h_obs) ** -2

SFR = unyt.unyt_array(SFR, units="Msun/yr")
Phi_SFR_scatter = unyt.unyt_array(
    (delta_Phi_SFR_m * 1e-3, delta_Phi_SFR_p * 1e-3), units="1/Mpc**3"
)
Phi_SFR = unyt.unyt_array(Phi_SFR * 1e-3, units="1/Mpc**3")

processed.associate_x(
    SFR, scatter=None, comoving=False, description="Star formation rate"
)
processed.associate_y(
    Phi_SFR,
    scatter=Phi_SFR_scatter,
    comoving=False,
    description="Phi (SFR)",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(4.5, 2.0, 7.0)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Bollo2023.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
