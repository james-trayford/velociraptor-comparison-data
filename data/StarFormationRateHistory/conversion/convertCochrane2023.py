from velociraptor.observations.objects import (
    ObservationalData,
)

import unyt
import numpy as np
import os
import sys


def cosmic_star_formation_history_сochrane():
    # Meta-data
    name = "Star formation rate density from Cochrane et al. (2023)"
    comment = (
        "The cosmic star formation history over 0 < z < 4, using deep, radio continuum observations of "
        "The Low Frequency Array Two Metre Sky Survey."
        "Uses the Chabrier initial mass function. "
        "Cosmology: H0=70.0, OmegaM=0.30. "
        "No cosmological corrections were applied during the conversion of the raw data."
    )

    citation = "Cochrane et al. (2023, LOFAR)"
    bibcode = "2023MNRAS.tmp.1548C"
    plot_as = "points"
    output_filename = "Cochrane2023.hdf5"
    output_directory = "../"

    # Create observational data instance
    processed = ObservationalData()
    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_cosmology(cosmology)

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # Load raw Cochrane2023 data
    data = np.loadtxt(f"../raw/sfr_cochrane2023.dat")

    # Fetch the fields we need
    z_m, z_p = data[:, 0], data[:, 1]
    z = 0.5 * (z_m + z_p)
    a = 1.0 / (1.0 + z)
    a = unyt.unyt_array(a, units="dimensionless")

    SFR, SFR_err = data[:, 7], data[:, 8]  # Msun / yr / Mpc**3
    SFR_scatter = unyt.unyt_array((SFR_err, SFR_err), units="Msun/yr/Mpc**3")
    SFR = unyt.unyt_array(SFR, units="Msun/yr/Mpc**3")

    processed.associate_x(
        a, scatter=None, comoving=False, description="Cosmic scale factor"
    )
    processed.associate_y(
        SFR,
        scatter=SFR_scatter,
        comoving=False,
        description="Cosmic average star formation rate density",
    )

    processed.associate_redshift(np.mean(z))
    processed.associate_plot_as(plot_as)

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)


# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Generate, format and save the Cochrane et al. 2023
cosmic_star_formation_history_сochrane()
