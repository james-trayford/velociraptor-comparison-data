from velociraptor.observations.objects import ObservationalData
import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmologies
h_sim = cosmology.h

input_filename = "../raw/Menard2010.txt"

output_filename = "Menard2010_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
R_proj = pow(10.0, raw[:, 0]) * unyt.kpc
Sigma_dust = pow(10.0, raw[:, 1]) * unyt.Solar_Mass * pow(unyt.pc, -2)
Sigma_dust_lo = pow(10.0, raw[:, 2]) * unyt.Solar_Mass * pow(unyt.pc, -2)
Sigma_dust_hi = pow(10.0, raw[:, 3]) * unyt.Solar_Mass * pow(unyt.pc, -2)

y_scatter = unyt.unyt_array([Sigma_dust_hi - Sigma_dust, Sigma_dust - Sigma_dust_lo])


# Meta-data
comment = "Dust Surface density in the CGM as a function of projected radius for galaxies at z ~0.3, with i-band magnitudes 17 < i < 21. Obtained through reddening measurements using galaxy pairs. "

citation = "Menard et al 2010"
bibcode = "2010MNRAS.405.1025M"
name = "Projected Radius - Dust Surface Density"
plot_as = "points"
redshift = 0.3
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    R_proj, scatter=None, comoving=True, description="Projected Radius"
)
processed.associate_y(
    Sigma_dust, scatter=y_scatter, comoving=True, description="Dust Surface Density",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, 0, 2)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
