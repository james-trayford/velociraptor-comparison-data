from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Walter2020_rhoH2.txt"

processed = ObservationalData()

comment = "Based on a fit."
citation = "Walter et al. (2020)"
bibcode = "2020ApJ...902..111W"
name = "H2 Mass Cosmic History"
plot_as = "line"

zgrid = np.linspace(0.0, 4.0, 50)
agrid = 1.0 / (1.0 + zgrid)


def fitting_formula(z, a, b, c, d):
    return (a * (1.0 + z) ** b) / (1.0 + ((1.0 + z) / c) ** d)


raw = np.loadtxt(input_filename, usecols=(1, 2, 3, 4))
rhoH2 = fitting_formula(zgrid, *raw[0])
rhoH2_low = fitting_formula(zgrid, *raw[1])
rhoH2_high = fitting_formula(zgrid, *raw[2])

a = unyt.unyt_array(agrid, units=unyt.dimensionless)
rhoH2_err = unyt.unyt_array(
    [rhoH2 - rhoH2_low, rhoH2_high - rhoH2], units=unyt.Msun / unyt.Mpc ** 3
)
rhoH2 = unyt.unyt_array(rhoH2, units=unyt.Msun / unyt.Mpc ** 3)

processed.associate_x(
    a, scatter=None, comoving=False, description="Cosmic scale factor"
)
processed.associate_y(
    rhoH2,
    scatter=rhoH2_err,
    comoving=False,
    description="Cosmic H2 Mass Density",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
zmin = zgrid.min()
zmax = zgrid.max()
processed.associate_redshift(0.5 * (zmin + zmax), zmin, zmax)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Walter2020.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
