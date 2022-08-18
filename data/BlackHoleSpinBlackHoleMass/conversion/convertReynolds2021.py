from velociraptor.observations.objects import ObservationalData
from astropy.cosmology import WMAP7 as cosmology

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
#with open(sys.argv[1], "r") as handle:
#    exec(handle.read())

input_filename = "../raw/Reynolds2021.txt"
delimiter = None
half_mass = 1
log_mass = 0

output_filename = "Reynolds2021_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

# Read the data (only those columns we need here)
raw = np.loadtxt(input_filename, delimiter=delimiter, usecols=(1, 2, 3, 4, 5, 6))

M_BH = 10 ** 6 * raw[:, 0] * unyt.Solar_Mass
M_BH_low = 10 ** 6 * (raw[:, 0] - raw[:, 2]) * unyt.Solar_Mass
M_BH_high = 10 ** 6 * (raw[:, 0] + raw[:, 1]) * unyt.Solar_Mass

a_BH = raw[:, 3] * unyt.dimensionless
a_BH_low = (raw[:, 3] - raw[:, 5]) * unyt.dimensionless
a_BH_high = (raw[:, 3] + raw[:, 4]) * unyt.dimensionless

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((M_BH - M_BH_low, M_BH_high - M_BH))
y_scatter = unyt.unyt_array((a_BH - a_BH_low, a_BH_high - a_BH))

comment = (" Masses are obtained mostly from X-ray reverberation. "
           " Spins are obtained using X-ray reflection methods."
           " The mass data for the last four objects were obtained from:"
           " Bambi et al. (2021); 2021SSRv..217...65B,"
           " Bennert et al. (2006); 2006A&A...459...55B,"
           " Campitiello et al. (2020); 2020A&A...640A..39C,"
           " respectively, with the first work providing mass data for the"
           " first two objects. The mass of Swift J2127.4+5654 has been"
           " reduced by a factor of 10 to correct a typo in the original work."
           " The objects are listed in the same order as in Reynolds (2021)."
)
citation = "Reynolds (2021)"
bibcode = "2021ARA&A..59..117R"
name = "Black Hole Mass - Black Hole Spin"
plot_as = "points"
redshift = 0.0
h = cosmology.h

processed.associate_x(
    M_BH, scatter=x_scatter, comoving=False, description="Black hole mass"
)
processed.associate_y(
    a_BH, scatter=y_scatter, comoving=False, description="Black hole spin"
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
