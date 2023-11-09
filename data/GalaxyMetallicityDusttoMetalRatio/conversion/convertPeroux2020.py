from velociraptor.observations.objects import (
    MultiRedshiftObservationalData,
    ObservationalData,
)

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Peroux2020.txt"
delimiter = None

output_filename = "Peroux2020.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

raw = np.loadtxt(input_filename, delimiter=delimiter)

comment = (
    "Assuming Chabrier IMF. No h-correction "
    "was required as data was supplied h-free. "
)
citation = "Perouk & Howk (2020)"
bibcode = ""
name = "Galaxy Gas Phase Oxygen Abundance - Galaxy Dust-to-metal ratio"
plot_as = "points"
h = 0.7

z_hi = raw.T[3]
z_lo = raw.T[2]
z = 0.5 * (z_lo + z_hi)

oabundance = unyt.unyt_array(raw.T[0], units=unyt.Dimensionless)

d2m = unyt.unyt_array(10 ** raw.T[1], units=unyt.Dimensionless)
zs = np.sort(list(set(z)))
zlos = np.sort(list(set(z_lo)))
zhis = np.sort(list(set(z_hi)))

multi_z = MultiRedshiftObservationalData()
multi_z.associate_citation(citation, bibcode)
multi_z.associate_name(name)
multi_z.associate_comment(comment)
multi_z.associate_cosmology(cosmology)

for i in range(zs.size):
    processed = ObservationalData()

    bdx = z_lo == z_lo[i]

    processed.associate_x(
        oabundance[bdx],
        scatter=None,
        comoving=False,
        description="[O/H]",
    )
    processed.associate_y(
        d2m[bdx],
        scatter=None,
        comoving=False,
        description="D2M",
    )

    processed.associate_redshift(zs[i], zlos[i], zhis[i])
    processed.associate_plot_as(plot_as)
    multi_z.associate_dataset(processed)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
