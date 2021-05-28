from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
import copy
import re
from velociraptor.tools.lines import binned_median_line

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/DGR_Galametz2011.csv"
output_filename = f"Galametz2011.hdf5"
delimiter = "&"

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

raw = np.genfromtxt(input_filename, dtype=float, delimiter=delimiter)

# Oxygen abundance to Z absolute conversion
logOH_plus_twelve_sun = 8.69
Z_sun = 0.0134
logOH_plus_twelve_to_Z_abs = Z_sun * pow(10.0, -logOH_plus_twelve_sun)

logOH_plus_twelve_med = raw[:, 1] * unyt.dimensionless
dust_to_gas_med = raw[:, 4] * unyt.dimensionless
Z_abs = raw[:, 1] * logOH_plus_twelve_to_Z_abs
M_Z = Z_abs * (raw[:, 3] + raw[:, 5])
dust_to_metal = raw[:, -2] * unyt.dimensionless / M_Z

# Meta-data
comment = f"values for individual galaxies compiled by Galametz+2011"
citation = f"Galametz et al. 2011 compilation"
bibcode = "2011A&A...532A..56G"
name = "Dust-to-metal ratio as a function of log10(O/H)+12"
plot_as = "points"
redshift = 0.0
redshift_lower = 0.0
redshift_upper = 3.0
h = 0.7

# Write everything
outobj = ObservationalData()
outobj.associate_x(
    logOH_plus_twelve_med,
    scatter=None,
    comoving=True,
    description="Gas phase log10(O/H) + 12",
)
outobj.associate_y(
    dust_to_metal, scatter=None, comoving=True, description="Dust-to-metal Ratio",
)
outobj.associate_citation(citation, bibcode)
outobj.associate_name(name)
outobj.associate_comment(comment)
outobj.associate_redshift(redshift, redshift_lower, redshift_upper)
outobj.associate_plot_as(plot_as)
outobj.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

outobj.write(filename=output_path)
