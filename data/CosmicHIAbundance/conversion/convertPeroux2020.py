from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Peroux2020_OmegaHI.txt"

processed = ObservationalData()

comment = (
    "Based on a fit. "
    "The data was corrected to our cosmology. "
    "We undid the correction from HI density to total mass density by "
    "multiplying with 0.76."
)
citation = "Peroux & Howk (2020)"
bibcode = "2020ARA&A..58..363P"
name = "HI Mass Cosmic History"
plot_as = "line"

zgrid = np.linspace(0.0, 4.0, 50)
agrid = 1.0 / (1.0 + zgrid)


def fitting_formula(z, a, b):
    return (
        a
        * unyt.unyt_quantity.from_astropy(cosmology.critical_density0)
        * (1.0 + z) ** b
    ).to("Msun/Mpc**3")


raw = np.loadtxt(input_filename, usecols=(1, 2))
rhoHI = fitting_formula(zgrid, *raw[0])
rhoHI_low = fitting_formula(zgrid, *raw[1])
rhoHI_high = fitting_formula(zgrid, *raw[2])

# convert from the cosmology assumed by Peroux & Howk
# (Omega_m = 0.3, Omega_lambda = 0.7, h = 0.7)
# to our cosmology
cosmology_correction = (
    np.sqrt(cosmology.Om0 * (1.0 + zgrid) ** 3 + cosmology.Ode0) / cosmology.h
) / (np.sqrt(0.3 * (1.0 + zgrid) ** 3 + 0.7) / 0.7)
# Peroux & Howk converted the HI density into a total mass density
# assuming an H abundance of 0.76
# Undo this correction
rhoHI *= 0.76 * cosmology_correction
rhoHI_low *= 0.76 * cosmology_correction
rhoHI_high *= 0.76 * cosmology_correction

a = unyt.unyt_array(agrid, units=unyt.dimensionless)
rhoHI_err = unyt.unyt_array(
    [rhoHI - rhoHI_low, rhoHI_high - rhoHI], units=unyt.Msun / unyt.Mpc ** 3
)
rhoHI = unyt.unyt_array(rhoHI, units=unyt.Msun / unyt.Mpc ** 3)

processed.associate_x(
    a, scatter=None, comoving=False, description="Cosmic scale factor"
)
processed.associate_y(
    rhoHI,
    scatter=rhoHI_err,
    comoving=False,
    description="Cosmic HI Mass Density",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
zmin = zgrid.min()
zmax = zgrid.max()
processed.associate_redshift(0.5 * (zmin + zmax), zmin, zmax)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Peroux2020.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
