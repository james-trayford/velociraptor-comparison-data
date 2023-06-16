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

redshift_list = [4.0, 5.0, 6.0, 7.0, 8.0]
h_obs = 0.7
h_sim = cosmology.h

output_filename = "Navarro-Carrera2023.hdf5"
output_directory = "../"
comment = (
    "GSMF derived from 3300 galaxies between redshifts z = 3.5 and 8.5, selected from JWST images "
    "in the Hubble Ultra Deep Field and UKIDSS Ultra Deep Survey field. "
    "Uses the Chabrier 2003 initial mass function. "
    "Cosmology: H0=70.0, OmegaM=0.30. "
    "The data is taken from Table 4 of the paper. The points that lie under the stellar mass completeness limits or "
    "that have <= 1 galaxy counts are not quoted in this Table."
)
citation = "Navarro-Carrera et al. (2023)"
bibcode = "2023arXiv230516141N"
name = "High redshift (4<z<8) GSMF from JWST"
plot_as = "points"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

multi_z = MultiRedshiftObservationalData()
multi_z.associate_citation(citation, bibcode)
multi_z.associate_name(name)
multi_z.associate_comment(comment)
multi_z.associate_cosmology(cosmology)
multi_z.associate_maximum_number_of_returns(1)

for redshift in redshift_list:

    processed = ObservationalData()
    data = np.loadtxt(f"../raw/Navarro-Carrera2023_z{redshift:.0f}.dat")

    log10_Mstar_m, log10_Mstar_p = data[:, 0], data[:, 1]
    Phi, Phi_err = data[:, 2], data[:, 3]

    log10_Mstar = 0.5 * (log10_Mstar_m + log10_Mstar_p)
    Mstar = (10.0 ** log10_Mstar) * unyt.Solar_Mass * (h_sim / h_obs) ** -2
    Phi = (Phi * 1e-4) * unyt.Mpc ** (-3) * (h_sim / h_obs) ** 3
    Phi_err = ((Phi_err * 1e-4) * unyt.Mpc ** (-3)) * (h_sim / h_obs) ** 3

    processed.associate_x(
        Mstar, scatter=None, comoving=True, description="Galaxy Stellar Mass"
    )
    processed.associate_y(Phi, scatter=Phi_err, comoving=True, description="Phi (GSMF)")
    processed.associate_redshift(redshift, redshift - 0.5, redshift + 0.5)
    processed.associate_plot_as(plot_as)

    multi_z.associate_dataset(processed)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
