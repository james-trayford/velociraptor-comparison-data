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

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.arange(8, 12.25, 0.25)
M_star = 10 ** raw * unyt.Solar_Mass
Z_star = 0.04 * raw - 0.28
error_Z_star = 0.01 * raw + 0.09

# Correction factor due to the difference in (X_O/X_Fe)_Sun
# From Grevesse & Sauval (1998) to Asplund+ (2009)

O_H_Grevesse98 = 8.83
Mg_H_Grevesse98 = 7.58
Fe_H_Grevesse98 = 7.50

O_Fe_Grevesse98 = O_H_Grevesse98 - Fe_H_Grevesse98
Mg_Fe_Grevesse98 = Mg_H_Grevesse98 - Fe_H_Grevesse98

O_over_H_Asplund09 = 8.69
Fe_over_H_Asplund09 = 7.50
Mg_over_H_Asplund09 = 7.6

O_over_Fe_Asplund09 = O_over_H_Asplund09 - Fe_over_H_Asplund09
Mg_over_Fe_Asplund09 = Mg_over_H_Asplund09 - Fe_over_H_Asplund09

element_list = np.array(["MgFe", "OFe"])

for element in element_list:

    output_filename = "RomeroGomez2023_Data_" + element + ".hdf5"
    if element == "OFe":
        correction = O_Fe_Grevesse98 - O_over_Fe_Asplund09

    if element == "MgFe":
        correction = Mg_Fe_Grevesse98 - Mg_over_Fe_Asplund09

    Z_median = (Z_star + correction) * unyt.dimensionless
    Z_lo = (Z_star - error_Z_star + correction) * unyt.dimensionless
    Z_hi = (Z_star + error_Z_star + correction) * unyt.dimensionless

    # Define the scatter as offset from the mean value
    y_scatter = unyt.unyt_array((Z_median - Z_lo, Z_hi - Z_median))

    # Meta-data
    comment = (
        "The metallicity is expressed as [alpha/Fe]. Note that alpha does not stand for Oxygen. "
        "Romero-Gomez et al. applied the MILES pipeline (Vazdekis et al. 2015, Pietrinferni et al. 2004, 2006) to the ATLAS-3D galaxy catalog (Cappilleri et al. 2013). "
        "They provided best-fitting relations along with error bars for the 16th and 84th percentile of the distribution. "
        f"The data has been corrected to use Z_solar={solar_metallicity} (Asplund+ 2009)"
    )
    citation = "Romero-Gomez et al. (2023) (ATLAS-3D)"
    bibcode = "2023MNRAS.522...130R"
    name = "Stellar mass - [alpha/Fe] relation"
    plot_as = "line"
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
