"""
Conversion script for the parameter searching values.
"""

from velociraptor.observations.objects import (
    ObservationalData,
    MultiRedshiftObservationalData,
)

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)


apertures = [30, 50, 100]
box_sizes = [25, 100]
redshifts = [0.0, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

citation = "Schaye et al. (2015)"
bibcode = "2015MNRAS.446..521S"
name = "Galaxy Stellar Mass Function"
plot_as = "line"
h_obs = 0.6777
h = cosmology.h

for aperture in apertures:
    for box_size in box_sizes:

        comment = (
            f"EAGLE GSMF at redshifts {min(redshifts)}<z{max(redshifts)}, "
            "calculated out of the SUBFIND catalogues. "
            "h-free. Cosmology from Planck 2013; O_M = 0.307, O_L = 0.693. "
            "More information is available in Schaye et al. 2015. This file "
            f"is for box-size {box_size} Mpc and aperture {aperture} kpc."
        )

        multi_z = MultiRedshiftObservationalData()
        multi_z.associate_citation(citation, bibcode)
        multi_z.associate_name(name)
        multi_z.associate_comment(comment)
        multi_z.associate_cosmology(cosmology)
        multi_z.associate_maximum_number_of_returns(1)

        for z in redshifts:
            tag = str(z).replace(".", "p")

            processed = ObservationalData()

            redshift = z
            raw_filename = f"../raw/Schaye2015_{box_size}_{aperture}kpc_z{tag}.txt"

            M, N, sigma = np.loadtxt(raw_filename, skiprows=3, delimiter=" ").T

            mass = unyt.unyt_array(M, units=unyt.Solar_Mass)
            smf = unyt.unyt_array(N, units=1 / unyt.Mpc ** 3)

            smf_scatter = unyt.unyt_array(sigma, units=1 / unyt.Mpc ** 3)

            processed.associate_x(
                mass,
                scatter=None,
                comoving=False,
                description=f"Galaxy Stellar Mass ({aperture} kpc)",
            )
            processed.associate_y(
                smf,
                scatter=smf_scatter,
                comoving=True,
                description="Galaxy Stellar Mass Function",
            )

            processed.associate_redshift(
                redshift, redshift_lower=redshift - 0.25, redshift_upper=redshift + 0.25
            )
            processed.associate_plot_as(plot_as)

            multi_z.associate_dataset(processed)

        output_path = f"{output_directory}/Schaye2015_{box_size}_{aperture}kpc.hdf5"

        if os.path.exists(output_path):
            os.remove(output_path)

        multi_z.write(filename=output_path)
