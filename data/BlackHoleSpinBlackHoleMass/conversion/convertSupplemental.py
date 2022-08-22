from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Supplemental.txt"
delimiter = None

output_filename = "Supplemental_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

# Read the data (only those columns we need here)
raw = np.loadtxt(input_filename, delimiter=delimiter, usecols=(2, 3, 4, 5, 6, 7))

M_BH = 10 ** 6 * raw[:, 0] * unyt.Solar_Mass
M_BH_low = 10 ** 6 * (raw[:, 0] - raw[:, 2]) * unyt.Solar_Mass
M_BH_high = 10 ** 6 * (raw[:, 0] + raw[:, 1]) * unyt.Solar_Mass

a_BH = raw[:, 3] * unyt.dimensionless
a_BH_low = (raw[:, 3] - raw[:, 5]) * unyt.dimensionless
a_BH_high = (raw[:, 3] + raw[:, 4]) * unyt.dimensionless

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((M_BH - M_BH_low, M_BH_high - M_BH))
y_scatter = unyt.unyt_array((a_BH - a_BH_low, a_BH_high - a_BH))

comment = (
    " Masses are obtained mostly from X-ray reverberation."
    "Spins are obtained using X-ray reflection methods, with the exception of"
    "the last two objects."
    "The papers used for the spin values are the following:"
    "W2013 Walton et al. (2013); 2013MNRAS.428.2901W,"
    "V2016 Vasudevan et al. (2016); 2016MNRAS.458.2012V,"
    "J2019 Jiang et al. (2019); 2019MNRAS.489.3436J,"
    "W2021 Walton et al. (2021); 2021arXiv210710278W,"
    "G2021 Ghosh et al. (2021); 2021ApJ...908..198G,"
    "B2021 Bambi et al. (2021); 2021SSRv..217...65B,"
    "SR2022 Sisk-Reynes et al. (2022); 2022MNRAS.514.2568S,"
    "A2019 Akiyama et al. (2019); 2019ApJ...875L...5E,"
    "V2016 Valtonen et al. (2016); 2016ApJ...819L..37V,"
    "L2020 Laine et al. (2020); 2020ApJ...894L...1L."
)
citation = "Supplemental data"
bibcode = "various, see comments"
name = "Black Hole Mass - Black Hole Spin"
plot_as = "points"
redshift = 0.0

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
