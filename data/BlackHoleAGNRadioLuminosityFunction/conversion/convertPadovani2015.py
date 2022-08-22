from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Padovani2015.txt"
delimiter = None

output_filename = "Padovani2015_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

# Read the data (only those columns we need here)
raw = np.loadtxt(input_filename, delimiter=delimiter, usecols=(0, 1, 2, 3, 4, 5))

L1_4 = 10 ** raw[:, 0] * unyt.Watt / unyt.Hertz
L1_4_low = 10 ** (raw[:, 0] - raw[:, 2]) * unyt.Watt / unyt.Hertz
L1_4_high = 10 ** (raw[:, 0] + raw[:, 1]) * unyt.Watt / unyt.Hertz

# Padovani et al. (2015) define their luminosity function using the natural logarithm.
# We convert to the usual definition, using dex, by multiplying with a conversion factor
# that is equal to ln(10). We also multiply by 1e-9 to convert from units of Gpc^-3 to Mpc^-3.
logarithmic_conversion_factor = np.log(10)
Phi = logarithmic_conversion_factor * 1e-9 * 10 ** raw[:, 3] / unyt.Mpc ** 3
Phi_low = (
    logarithmic_conversion_factor * 1e-9 * 10 ** (raw[:, 3] - raw[:, 5]) / unyt.Mpc ** 3
)
Phi_high = (
    logarithmic_conversion_factor * 1e-9 * 10 ** (raw[:, 3] + raw[:, 4]) / unyt.Mpc ** 3
)

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((L1_4 - L1_4_low, L1_4_high - L1_4))
y_scatter = unyt.unyt_array((Phi - Phi_low, Phi_high - Phi_low))

comment = (
    " AGN radio luminosity data, taken from Padovani et al. (2015):"
    " 2015MNRAS.452.1263P"
)
citation = "Padovani et al. (2015)"
bibcode = "2015MNRAS.452.1263P"
name = "AGN Radio Luminosity Function"
plot_as = "points"
redshift = 0.1
redshift_high = 0.4
redshift_low = 0.0

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
processed.associate_redshift(redshift, redshift_high, redshift_low)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
