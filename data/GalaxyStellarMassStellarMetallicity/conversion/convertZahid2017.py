from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
import scipy.stats as stats

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

Z_solar_obs = 0.0142
h_sim = cosmology.h


input_filename = "../raw/Zahid_2017.txt"

output_filename = "Zahid2017_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
M_star = raw[:, 1]
Z_star = 10 ** raw[:, 3] * unyt.dimensionless * Z_solar_obs / solar_metallicity

mass_bins = np.arange(8.55, 10.95, 0.1)
mass_bin_centers = 0.5 * (mass_bins[1:] + mass_bins[:-1])
Z_median, _, _ = stats.binned_statistic(
    M_star, Z_star, statistic="median", bins=mass_bins
)
Z_std_up, _, _ = stats.binned_statistic(
    M_star, Z_star, statistic=lambda x: np.percentile(x, 84.0), bins=mass_bins
)
Z_std_do, _, _ = stats.binned_statistic(
    M_star, Z_star, statistic=lambda x: np.percentile(x, 16.0), bins=mass_bins
)

M_star = 10 ** mass_bins * unyt.Solar_Mass
Z_star = Z_median * unyt.dimensionless
# Define the scatter as offset from the mean value
y_scatter = (
    unyt.unyt_array((Z_median - Z_std_do, Z_std_up - Z_median)) * unyt.dimensionless
)

# Meta-data
comment = (
    "Data obtained from Zahid et al. (2017). No need for "
    "h-correction. The metallicity is expressed in units of solar metallicity, using Z=0.0142. "
    "The error bars given the 16th and 84th percentile of the distribution. "
    f"This has been corrected to use Z_solar={solar_metallicity}. "
)
citation = "Zahid et al. (2017) (SDSS)"
bibcode = "2017ApJ...847...18Z"
name = "Stellar mass - Stellar metallicity relation"
plot_as = "line"
redshift = 0.08
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Z_star, scatter=y_scatter, comoving=True, description="Stellar metallicity"
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
