from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Meta-data
comment = (
    "Fit to the data from 195 star-forming high-redshift galaxies. "
    "Asplund et al. (2009) solar abundances are assumed. "
    "The median stellar mass is 1e10 Msun."
)
citation = "Strom et al. (2022)"
bibcode = "2022ApJ...925..116S"
plot_as = "line"
redshift = np.array([1.9, 3.1])

M_star = unyt.unyt_array(np.logspace(9.0, 11.3, 20), units="Msun")

models = {
    "OH": {"alpha": (8.35, 0.02), "beta": (0.14, 0.05), "label": "12+log10(O/H)"},
    "NH": {"alpha": (7.07, 0.03), "beta": (0.29, 0.07), "label": "12+log10(N/H)"},
}


def fitcurve(M, alpha, beta):
    return alpha + beta * (np.log10(M / unyt.Msun) - 10.0)


for model in models:
    label = models[model]["label"]

    name = f"Stellar mass - Gas phase metallicity relation ({label})"
    output_filename = f"Strom2022_{model}.hdf5"

    alpha, alpha_err = models[model]["alpha"]
    beta, beta_err = models[model]["beta"]

    Z = fitcurve(M_star, alpha, beta)
    Zpp = fitcurve(M_star, alpha + alpha_err, beta + beta_err)
    Zpm = fitcurve(M_star, alpha + alpha_err, beta - beta_err)
    Zmp = fitcurve(M_star, alpha - alpha_err, beta + beta_err)
    Zmm = fitcurve(M_star, alpha - alpha_err, beta - beta_err)
    Z_max = np.maximum(np.maximum(Zpp, Zpm), np.maximum(Zmp, Zmm))
    Z_min = np.minimum(np.minimum(Zpp, Zpm), np.minimum(Zmp, Zmm))

    Z_scatter = unyt.unyt_array([Z - Z_min, Z_max - Z], units="dimensionless")
    Z = unyt.unyt_array(Z, units="dimensionless")

    # Write everything
    processed = ObservationalData()
    processed.associate_x(
        M_star, scatter=None, comoving=False, description="Galaxy Stellar Mass"
    )
    processed.associate_y(
        Z,
        scatter=Z_scatter,
        comoving=False,
        description=f"Gas phase metallicity ({label})",
    )
    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_redshift(redshift.mean(), *redshift)
    processed.associate_plot_as(plot_as)
    processed.associate_cosmology(cosmology)

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
