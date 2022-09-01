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

output_filename = "Terrazas2017.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
data = np.loadtxt(input_filename)

# Stellar masses
Mstar = unyt.unyt_array(10 ** data[:, 0], units="Solar_Mass")

# Black Hole Masses
BH_mass = unyt.unyt_array(10 ** data[:, 3], units="Solar_Mass")
BH_mass_hi = unyt.unyt_array(10 ** (data[:, 3] + data[:, 4]), units="Solar_Mass")
BH_mass_lo = unyt.unyt_array(10 ** (data[:, 3] - data[:, 4]), units="Solar_Mass")
BH_mass_scatter = unyt.unyt_array([BH_mass_lo, BH_mass_hi])

# Star formation rates (uncertainty taken from Sec. 2)
SFR = unyt.unyt_array(10 ** data[:, 1], units="Solar_Mass / year")
SFR_hi = unyt.unyt_array(10 ** (data[:, 1] + 0.3), units="Solar_Mass / year")
SFR_lo = unyt.unyt_array(10 ** (data[:, 1] - 0.3), units="Solar_Mass / year")
SFR_scatter = unyt.unyt_array([SFR_lo, SFR_hi])

# Upper limits
limits = data[:, 2]

# Meta-data
comment = (
    "Selection of local galaxies with masses > 10^10 Msun. "
    f"No cosmology correction needed."
)
citation = f"Terrazas (2017) "
bibcode = "2017ApJ...844..170T"
name = "Black hole mass - Star Formation Rate relation"
plot_as = "points"
# We purposely make this data show up not only a z=0 but also at higher z
redshift_lower, redshift_upper = -0.1, 3.1
redshift = 0.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    BH_mass,
    scatter=BH_mass_scatter,
    comoving=True,
    description="Black Hole Mass",
)
processed.associate_y(
    SFR, scatter=SFR_scatter, comoving=True, description="Star Formation Rate"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, redshift_lower, redshift_upper)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
