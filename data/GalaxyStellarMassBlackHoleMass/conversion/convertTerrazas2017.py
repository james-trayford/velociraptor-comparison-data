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
delimiter = ","

output_filenames = ["Terrazas2017_SF.hdf5", "Terrazas2017_NSF.hdf5"]
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
data = np.loadtxt(input_filename)

# Stellar masses
Mstar = unyt.unyt_array(10 ** data[:, 0], units="Solar_Mass")
Mstar_hi = unyt.unyt_array(10 ** (np.log10(Mstar) + 0.15), units="Solar_Mass")
Mstar_lo = unyt.unyt_array(10 ** (np.log10(Mstar) - 0.15), units="Solar_Mass")
Mstar_scatter = unyt.unyt_array([Mstar - Mstar_lo, Mstar_hi - Mstar])

# Star formation rates
SFR = unyt.unyt_array(10 ** data[:, 1], units="Solar_Mass / year")

# Specific Star formation rates  (uncertainty taken from Sec. 2)
sSFR = SFR / Mstar

# Black Hole Masses
BH_mass = unyt.unyt_array(10 ** data[:, 3], units="Solar_Mass")
BH_mass_hi = unyt.unyt_array(10 ** (data[:, 3] + data[:, 4]), units="Solar_Mass")
BH_mass_lo = unyt.unyt_array(10 ** (data[:, 3] - data[:, 4]), units="Solar_Mass")
BH_mass_scatter = unyt.unyt_array([BH_mass - BH_mass_lo, BH_mass_hi - BH_mass])

# sSFR limit
sSFR_limit = unyt.unyt_quantity(1e-11, units="1 / year")

mask_SF = sSFR >= sSFR_limit
mask_NSF = sSFR < sSFR_limit

bibcode = "2017ApJ...844..170T"
name = "Black hole mass - Stellar mass relation"
plot_as = "points"
# We purposely make this data show up not only a z=0 but also at higher z
redshift_lower, redshift_upper = -0.1, 3.1
redshift = 0.0
h = h_sim

for i, output_filename, text in zip(
    [0, 1], output_filenames, ["sSFR > 10^-11", "sSFR < 10^-11"]
):

    if i == 0:
        mask = mask_SF
    else:
        mask = mask_NSF
    num_galaxies = np.sum(mask)

    # Meta-data
    comment = (
        f"Selection of local galaxies with {text}. " f"No cosmology correction needed."
    )
    citation = f"Terrazas (2017) ({text})"

    Mstar_scatter_masked = unyt.unyt_array(
        [Mstar_scatter[0][mask], Mstar_scatter[1][mask]]
    )
    BH_mass_scatter_masked = unyt.unyt_array(
        [BH_mass_scatter[0][mask], BH_mass_scatter[1][mask]]
    )

    # Write everything
    processed = ObservationalData()
    processed.associate_x(
        Mstar[mask],
        scatter=Mstar_scatter_masked,
        comoving=True,
        description="Galaxy Stellar Mass",
    )
    processed.associate_y(
        BH_mass[mask],
        scatter=BH_mass_scatter_masked,
        comoving=True,
        description="Black Hole Mass",
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
