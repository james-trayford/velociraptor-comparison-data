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


redshifts = [
    0.064,
    0.12,
    0.18,
    0.25,
    0.32,
    0.41,
    0.51,
    0.63,
    0.76,
    0.92,
    1.1,
    1.3,
    1.6,
    2.0,
    2.4,
    3.0,
    3.5,
    4.0,
]

citation = "Thorne et al. (2021)"
bibcode = "2021MNRAS.505..540T"
name = "Galaxy Stellar Mass Function"
plot_as = "line"
h_obs = 0.6777
h = cosmology.h

comment = (
    f"GSMF at redshifts {min(redshifts)}<z{max(redshifts)}, "
    "from the DEVILS suvery (D10-COSMOS field)."
    "Raw data re-binned by the authors in bins of 0.2dex."
    "h-free. Cosmology from Planck 2013; O_M = 0.307, O_L = 0.693. "
    "Chabrier IMF, masses obtained via the PROSPECT code. Consistent with GAMA."
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
    raw_filename = f"../raw/Thorne2021_z{tag}.txt"

    M, N, sigma = np.loadtxt(raw_filename, delimiter=" ").T

    mass = unyt.unyt_array(M, units=unyt.Solar_Mass)
    smf = unyt.unyt_array(10 ** N, units=1 / unyt.Mpc ** 3)
    smf_lo = unyt.unyt_array(10 ** (N - sigma), units=1 / unyt.Mpc ** 3)
    smf_hi = unyt.unyt_array(10 ** (N + sigma), units=1 / unyt.Mpc ** 3)
    smf_scatter = unyt.unyt_array([smf - smf_lo, smf_hi - smf])

    processed.associate_x(
        mass,
        scatter=None,
        comoving=False,
        description=f"Galaxy Stellar Mass",
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

output_path = f"{output_directory}/Thorne2021.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
