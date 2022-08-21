from velociraptor.observations.objects import ObservationalData
from astropy.cosmology import WMAP7 as cosmology

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Smolcic2009.txt"
delimiter = None
half_mass = 1
log_mass = 0

output_filename = "Smolcic2009_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

# Read the data (only those columns we need here)
raw = np.loadtxt(input_filename, delimiter=delimiter, usecols=(0, 1, 2, 3, 4, 5))

print(raw[:, 0] * 10 ** 21)
L1_4 = raw[:, 0] * (float(1e21) * unyt.dimensionless)
L1_4_low = (raw[:, 0] - raw[:, 2]) * (float(1e21) * unyt.dimensionless)
L1_4_high = (raw[:, 0] + raw[:, 1]) * (float(1e21) * unyt.dimensionless)

Phi = raw[:, 3] * (float(1e-4) * unyt.Mpc ** -3)
Phi_low = (raw[:, 3] - raw[:, 5]) * (float(1e-4) * unyt.Mpc ** -3)
Phi_high = (raw[:, 3] + raw[:, 4]) * (float(1e-4) * unyt.Mpc ** -3)

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((L1_4 - L1_4_low, L1_4_high - L1_4))
y_scatter = unyt.unyt_array((Phi - Phi_low, Phi_high - Phi_low))

comment = (
    " AGN radio luminosity data, taken from Smolcic et al. (2009):"
    " 2009ApJ...696...24S"
)
citation = "Smolcic et al. (2009)"
bibcode = "2009ApJ...696...24S"
name = "AGN Radio Luminosity Function"
plot_as = "points"
redshift = 0.23
h = cosmology.h

processed.associate_x(
    L1_4,
    scatter=x_scatter,
    comoving=False,
    description="AGN radio luminosity at 1.4 GHz",
)
processed.associate_y(
    Phi,
    scatter=y_scatter,
    comoving=False,
    description="AGN radio luminosity function at 1.4 GHz",
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
