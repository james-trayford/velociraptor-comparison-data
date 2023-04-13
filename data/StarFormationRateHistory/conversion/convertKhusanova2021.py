from velociraptor.observations.objects import (
    ObservationalData,
    MultiRedshiftObservationalData,
)

import unyt
import numpy as np
import os
import sys


def cosmic_star_formation_history_khusanova():
    # Meta-data
    name = f"Star formation rate density from Enia et al. (2022)"
    comment = (
        "Uses the Chabrier initial mass function. " "Cosmology: H0=70.0, OmegaM=0.30."
    )

    citation = "Khusanova et al. (2021)"
    bibcode = "2021A&A...649A.152K"
    plot_as = "points"
    output_filename = "Khusanova2021.hdf5"
    output_directory = "../"

    # Create observational data instance
    processed = ObservationalData()
    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_cosmology(cosmology)

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # Load raw Khusanova2021 data
    data = np.loadtxt(f"../raw/sfr_khusanova2021.dat")

    # Fetch the fields we need
    z = data[:, 0]
    SFR, SFR_stderr_low, SFR_stderr_high = data[:, 1], data[:, 2], data[:, 3]

    a = 1.0 / (1.0 + z)

    a_bin = unyt.unyt_array(a, units="dimensionless")
    # convert from log10(SFRD) to SFRD and carry the uncertainties
    SFR_minus = 10.0 ** (SFR - SFR_stderr_low)
    SFR_plus = 10.0 ** (SFR + SFR_stderr_high)
    SFR = 10.0**SFR
    SFR_scatter = unyt.unyt_array(
        (SFR - SFR_minus, SFR_plus - SFR), units="Msun/yr/Mpc**3"
    )
    SFR = unyt.unyt_array(SFR, units="Msun/yr/Mpc**3")

    processed.associate_x(a_bin, comoving=False, description="Cosmic scale factor")
    processed.associate_y(
        SFR,
        scatter=SFR_scatter,
        comoving=False,
        description="Cosmic average star formation rate density",
    )

    processed.associate_redshift(z)
    processed.associate_plot_as(plot_as)

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)


# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Generate, format and save the Enia2022 data
cosmic_star_formation_history_khusanova()
