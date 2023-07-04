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

input_filename = "../raw/RomeroGomez_2023_ascii.txt"
delimiter = " "

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename, usecols=[1, 2, 3], skiprows=6)
M_star = 10 ** raw[:, 2] * unyt.Solar_Mass
select = np.where(raw[:, 2] > 0)[0] # Some missing data
M_star = M_star[select]
alpha_Fe = raw[select, 0]
error_alpha_Fe = raw[select, 1]

element_list = np.array(["MgFe", "OFe"])

for element in element_list:

    output_filename = "RomeroGomez2023_SphDwarfsLG_Data_" + element + ".hdf5"

    Z_median = alpha_Fe * unyt.dimensionless
    Z_lo = (alpha_Fe - error_alpha_Fe) * unyt.dimensionless
    Z_hi = (alpha_Fe + error_alpha_Fe) * unyt.dimensionless

    # Define the scatter as offset from the mean value
    y_scatter = unyt.unyt_array((Z_median - Z_lo, Z_hi - Z_median))

    # Meta-data
    comment = (
        "The metallicity is expressed as [alpha/Fe]. Note that alpha does not stand for Oxygen. "
        "Romero-Gomez et al. provides a data compilation of the alpha enhancement of Dwarf Galaxies in the Local Group. "
        f"The data has not been corrected to use Z_solar={solar_metallicity} (Asplund+ 2009), since it depends on the metallicity estimation of "
        f"individual galaxies."
    )
    citation = "Romero-Gomez et al. (2023) (LG Dwarfs)"
    bibcode = "2023MNRAS.522...130R"
    name = "Stellar mass - [alpha/Fe] relation"
    plot_as = "points"
    redshift = 0.1
    h = h_sim


    # Write everything
    processed = ObservationalData()
    processed.associate_x(
        M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
    )
    processed.associate_y(
        Z_median, scatter=y_scatter, comoving=True, description="Stellar [alpha/Fe]"
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
