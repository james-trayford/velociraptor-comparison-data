from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = f"../raw/Curti2020.txt"

processed = ObservationalData()
raw = np.loadtxt(input_filename)

comment = (
    "The relationships between stellar mass and gas-phase metallicity "
    "in the local Universe for SDSS galaxies. "
    "Uses Chabrier (2003) initial mass function. "
    "Uses the Solar metallicity of 12 + log(O/H)_Sun = 8.69. "
    "The data focuses on star forming galaxies. "
    "No conversion w.r.t solar metallicity value is needed. "
    "Uses cosmology assuming the parameters presented by Planck Collaboration et al. (2016)"
)
citation = "Curti et al. (2020)"
bibcode = "2020MNRAS.491..944C"
name = f"Galaxy Stellar Mass - Gas Metallicity"
plot_as = "points"
redshift = 0.1

Mstar = 10.0 ** raw[:, 0]
metal = raw[:, 1]
metal_error = raw[:, 2]

Mstar = unyt.unyt_array(Mstar, units=unyt.Msun)
metal = unyt.unyt_array(metal, units=unyt.dimensionless)
metal_error = unyt.unyt_array(metal_error, units=unyt.dimensionless)

processed.associate_x(
    Mstar, scatter=None, comoving=False, description="Galaxy Stellar Mass"
)
processed.associate_y(
    metal,
    scatter=metal_error,
    comoving=False,
    description="Galaxy Gas Metallicity (3 kpc aperture)",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Curti2020.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
