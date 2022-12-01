from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

Z_solar_obs = 0.0142
h_sim = cosmology.h

input_filename = "../raw/Kudritzki_2016.txt"

output_filename = "Kudritzki2016_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
M_star = 10 ** raw[:, 0] * unyt.Solar_Mass
Z_median = 10 ** raw[:, 1] * unyt.dimensionless * Z_solar_obs / solar_metallicity


# Meta-data
comment = (
    "Data obtained from Kudritzki et al. (2016). No need for "
    "h-correction. The metallicity is expressed in units of solar metallicity, using Z=0.0142. "
    f"This has been corrected to use Z_solar={solar_metallicity}. "
)
citation = "Kudritzki et al. (2016)"
bibcode = "2016ApJ...829...70K"
name = "Stellar mass - Stellar metallicity relation"
plot_as = "points"
redshift = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Z_median, scatter=None, comoving=True, description="Stellar metallicity"
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
