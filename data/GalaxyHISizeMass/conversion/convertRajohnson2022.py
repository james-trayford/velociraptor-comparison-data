from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

processed = ObservationalData()

comment = "Based on a fit to 204 galaxies from the MIGHTEE Survey Early Science data."
citation = "Rajohnson et al. (2022)"
bibcode = "2022MNRAS.512.2697R"
name = "HI Size Mass Relation"
plot_as = "line"

fit_slope = 0.501
fit_intercept = -3.252
fit_intercept_sigma_low = 0.074
fit_intercept_sigma_high = 0.073

Mrange = unyt.unyt_array(np.logspace(6.5, 12.0, 20), units="Msun")
logM = np.log10(Mrange)

HI_size = unyt.unyt_array(10.0 ** (fit_slope * logM + fit_intercept), units="kpc")
HI_size_low = unyt.unyt_array(
    10.0 ** (fit_slope * logM + fit_intercept - fit_intercept_sigma_low), units="kpc"
)
HI_size_high = unyt.unyt_array(
    10.0 ** (fit_slope * logM + fit_intercept + fit_intercept_sigma_high), units="kpc"
)
HI_size_err = unyt.unyt_array([HI_size - HI_size_low, HI_size_high - HI_size])

processed.associate_x(Mrange, scatter=None, comoving=False, description="HI Mass")
processed.associate_y(
    HI_size,
    scatter=HI_size_err,
    comoving=False,
    description="HI Size",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(0.042, 0.0, 0.084)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Rajohnson2022.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
