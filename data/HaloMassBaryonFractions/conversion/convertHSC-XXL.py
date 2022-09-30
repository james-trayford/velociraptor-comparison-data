from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
from astropy.cosmology import FlatLambdaCDM

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h
Omega_b = cosmology.Ob0
Omega_m = cosmology.Om0
FLATCDM = FlatLambdaCDM(H0=cosmology.H0, Om0=cosmology.Om0)

output_filename = "HSC-XXL.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Create a function for the fit from the paper
def def_fgas_Aki(M500, z):
    # Cosmology correct M500 to cited cosmology
    M500_cc = M500 * (h_sim / 0.70) ** (1.0)
    # Convert to scale free
    M500_cc_e = M500_cc * FLATCDM.efunc(z)
    # Calculate ration with the pivot
    Z = np.log(M500_cc_e / 1e14)
    # Calculate the term in the exponent
    exp_term = 1.95 + 1.29 * Z
    # Calculate Mgas*E(z)
    Mgas_e = np.exp(exp_term) * 1e12
    # Convert it to Mgas
    Mgas = Mgas_e / FLATCDM.efunc(z)
    # Calculate fgas and cosmology correct it
    fgas = Mgas * (h_sim / 0.70) ** (-1.5) / M500_cc
    # Error in the exponent
    err_on_exp = np.sqrt(0.08 ** 2 + (0.16) ** 2 * Z ** 2)
    # Convert to linear error
    lin_err = np.abs(err_on_exp * np.exp(1.95 + 1.29 * Z) * 1e12)
    # Apply cosmology correction terms
    fgas_err = lin_err * (h_sim / 0.70) ** (-1.5) / (M500_cc * FLATCDM.efunc(z))
    return fgas, fgas_err


# Create a function for the fit from the paper
def def_fstar_Aki(M500, z):
    # Cosmology correct M500 to cited cosmology
    M500_cc = M500 * (h_sim / 0.70) ** (1.0)
    # Convert to scale free
    M500_cc_e = M500_cc * FLATCDM.efunc(z)
    # Calculate ration with the pivot
    Z = np.log(M500_cc_e / 1e14)
    # Calculate the term in the exponent
    exp_term = 0.76 + 0.85 * Z
    # Calculate Mstar*E(z)
    Mstar_e = np.exp(exp_term) * 1e12
    # Convert it to Mstar
    Mstar = Mstar_e / FLATCDM.efunc(z)
    # Calculate fgas and cosmology correct it
    fstar = Mstar * (h_sim / 0.70) ** (-1.5) / M500_cc
    # Error in the exponent
    err_on_exp = np.sqrt(0.09 ** 2 + (0.12) ** 2 * Z ** 2)
    # Convert to linear error
    lin_err = np.abs(err_on_exp * np.exp(0.76 + 0.85 * Z) * 1e12)
    # Apply cosmology correction terms
    fstar_err = lin_err * (h_sim / 0.70) ** (-1.5) / (M500_cc * FLATCDM.efunc(z))
    return fstar, fstar_err


# Read the data
M_500 = np.array([10 ** (13.5), 10 ** (14.5)])
fs_500, error_fs_500_p = def_fstar_Aki(M_500, 0.3)
fg_500, error_fg_500_p = def_fgas_Aki(M_500, 0.3)

fb_500 = fs_500 + fg_500
error_fb_500_p = np.sqrt(error_fs_500_p ** 2 + error_fg_500_p ** 2)

# Convert to proper units
M_500 = unyt.unyt_array(M_500, units="Msun")
fb_500 = unyt.unyt_array(fb_500, units="dimensionless")
error_fb_500_p = unyt.unyt_array(error_fb_500_p, units="dimensionless")
error_fb_500_m = error_fb_500_p

# Normalise by the cosmic mean
fb_500 = fb_500 / (Omega_b / Omega_m)
error_fb_500_p = error_fb_500_p / (Omega_b / Omega_m)
error_fb_500_m = error_fb_500_m / (Omega_b / Omega_m)

# Define the scatter as offset from the mean value
y_scatter = unyt.unyt_array((error_fb_500_m, error_fb_500_p))

# Meta-data
comment = (
    "Gas fraction data from the fit to weak-lensing mass HSC-XXL clusters. "
    "Data was corrected for the simulation's cosmology."
)
citation = "Akino et al. (2021)"
bibcode = " 2021arXiv211110080A"
name = "HSC-XXL Gas Fractions"
plot_as = "points"
redshift = 0.3
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_500, scatter=None, comoving=True, description="Halo mass (M_500)"
)
processed.associate_y(
    fb_500, scatter=y_scatter, comoving=True, description="Gas fraction (<R_500)"
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
