from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h

input_filename = "../raw/Terrazas17.dat"

# Read the data
data = np.loadtxt(input_filename)

# Stellar masses
Mstar = unyt.unyt_array(10 ** data[:, 0], units="Solar_Mass")

# Star formation rates
SFR = unyt.unyt_array(10 ** data[:, 1], units="Solar_Mass / year")

# Specific Star formation rates  (uncertainty taken from Sec. 2)
sSFR = SFR / Mstar
sSFR_hi = unyt.unyt_array(10 ** (np.log10(sSFR) + 0.45), units="year**-1")
sSFR_lo = unyt.unyt_array(10 ** (np.log10(sSFR) - 0.45), units="year**-1")
sSFR_scatter = unyt.unyt_array([sSFR - sSFR_lo, sSFR_hi - sSFR])

# Black Hole Masses
BH_mass = unyt.unyt_array(10 ** data[:, 3], units="Solar_Mass")
BH_mass_hi = unyt.unyt_array(10 ** (data[:, 3] + data[:, 4]), units="Solar_Mass")
BH_mass_lo = unyt.unyt_array(10 ** (data[:, 3] - data[:, 4]), units="Solar_Mass")
BH_mass_scatter = unyt.unyt_array([BH_mass - BH_mass_lo, BH_mass_hi - BH_mass])

# Upper limits
upper_limits = np.array(data[:, 2], dtype=bool)
print(upper_limits)
no_limits = np.logical_not(upper_limits)

print(no_limits)

# First, data without upper limits #########################
BH_mass_no_limit = BH_mass[no_limits]
BH_mass_scatter_no_limit = unyt.unyt_array(
    [BH_mass_scatter[0][no_limits], BH_mass_scatter[1][no_limits]]
)
sSFR_no_limit = sSFR[no_limits]
sSFR_scatter_no_limit = unyt.unyt_array(
    [sSFR_scatter[0][no_limits], sSFR_scatter[1][no_limits]]
)

# Meta-data
comment = (
    "Selection of local galaxies with masses > 10^10 Msun. "
    "Data with upper limits removed. "
    f"No cosmology correction needed."
)
citation = f"Terrazas (2017) "
bibcode = "2017ApJ...844..170T"
name = "Black hole mass - Specific Star Formation Rate relation"
plot_as = "points"
# We purposely make this data show up not only a z=0 but also at higher z
redshift_lower, redshift_upper = -0.1, 3.1
redshift = 0.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    BH_mass_no_limit,
    scatter=BH_mass_scatter_no_limit,
    comoving=True,
    description="Black Hole Mass",
)
processed.associate_y(
    sSFR_no_limit,
    scatter=sSFR_scatter_no_limit,
    comoving=True,
    description="Specific Star Formation Rate",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, redshift_lower, redshift_upper)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_filename = "Terrazas2017.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)

# Second, data with upper limits #########################
BH_mass_upper_limit = BH_mass[upper_limits]
BH_mass_scatter_upper_limit = unyt.unyt_array(
    [BH_mass_scatter[0][upper_limits], BH_mass_scatter[1][upper_limits]]
)
sSFR_upper_limit = sSFR[upper_limits]
sSFR_scatter_upper_limit = unyt.unyt_array(
    [sSFR_scatter[0][upper_limits], sSFR_scatter[1][upper_limits]]
)

# Meta-data
comment = (
    "Selection of local galaxies with masses > 10^10 Msun. "
    "Only upper limits considered. "
    f"No cosmology correction needed."
)
citation = f"Terrazas (2017) - upper limits"
bibcode = "2017ApJ...844..170T"
name = "Black hole mass - Specific Star Formation Rate relation"
plot_as = "points"
# We purposely make this data show up not only a z=0 but also at higher z
redshift_lower, redshift_upper = -0.1, 3.1
redshift = 0.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    BH_mass_upper_limit,
    scatter=BH_mass_scatter_upper_limit,
    comoving=True,
    description="Black Hole Mass",
)
processed.associate_y(
    sSFR_upper_limit,
    scatter=None,
    comoving=True,
    description="Specific Star Formation Rate",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, redshift_lower, redshift_upper)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_filename = "Terrazas2017_upper_limits.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
