from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys


# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = f"../raw/data_schruba2011.txt"

processed = ObservationalData()

comment = "Based on the IRAM HERCULES survey."
bibcode = "2011AJ....142...37S"
name = "Molecular to atomic ratio as a function of neutral gas surface density"
plot_as = "points"

xself = lambda x: x
nonan = lambda x: x if x != "NaN" else np.nan
data = np.genfromtxt(
    input_filename,
    usecols=(5, 7, 10),
    dtype=[("Sigma_HI", np.float32), ("Sigma_H2", np.float32), ("quality", np.int32)],
)

for type, quality in {"detection": 2, "upper limit": 1}.items():
    citation = f"Schruba et al. (2011) [{type}]"

    subset = data[data["quality"] == quality]

    sigma_HI = unyt.unyt_array(subset["Sigma_HI"], "Msun/pc**2")
    sigma_H2 = unyt.unyt_array(subset["Sigma_H2"], "Msun/pc**2")
    sigma_neutral = sigma_HI + sigma_H2

    H2_to_HI = sigma_H2 / sigma_HI

    processed.associate_x(
        sigma_neutral,
        scatter=None,
        comoving=False,
        description="Neutral Gas Surface Density",
    )

    processed.associate_y(
        H2_to_HI,
        scatter=None,
        comoving=False,
        description="Molecular to Atomic Gas Ratio",
    )

    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_redshift(0.0, 0.0, 0.0)
    processed.associate_plot_as(plot_as)
    processed.associate_cosmology(cosmology)

    output_path = f"../Schruba2011_{type.replace(' ', '_')}.hdf5"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
