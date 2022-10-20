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

# Masks
upper_limits = np.array(data[:, 2], dtype=bool)
no_limits = np.logical_not(upper_limits)

bibcode = "2017ApJ...844..170T"
name = "Black hole mass - Specific Star Formation Rate relation"
plot_as = "points"
# We purposely make this data show up not only a z=0 but also at higher z
redshift_lower, redshift_upper = -0.1, 3.1
redshift = 0.0
h = h_sim

for mask, text in zip([no_limits, upper_limits], ["without", "only"]):

    BH_mass_masked = BH_mass[mask]
    BH_mass_scatter_masked = unyt.unyt_array(
        [BH_mass_scatter[0][mask], BH_mass_scatter[1][mask]]
    )
    sSFR_masked = sSFR[mask]
    sSFR_scatter_masked = unyt.unyt_array(
        [sSFR_scatter[0][mask], sSFR_scatter[1][mask]]
    )

    comment = (
        f"Selection of local galaxies with masses > 10^10 Msun. "
        f"Data, {text} upper limits. "
        f"No cosmology correction needed."
    )
    citation = f"Terrazas (2017) ({text} upper limits)"

    # Write everything
    processed = ObservationalData()
    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_redshift(redshift, redshift_lower, redshift_upper)
    processed.associate_plot_as(plot_as)
    processed.associate_cosmology(cosmology)

    processed.associate_x(
        BH_mass_masked,
        scatter=BH_mass_scatter_masked,
        comoving=True,
        description="Black Hole Mass",
    )
    processed.associate_y(
        sSFR_masked,
        scatter=sSFR_scatter_masked,
        comoving=True,
        description="Specific Star Formation Rate",
    )

    output_filename = f"Terrazas2017_{text}_upper_limits.hdf5"
    output_directory = "../"

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
