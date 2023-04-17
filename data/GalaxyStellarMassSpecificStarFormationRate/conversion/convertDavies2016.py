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


def SFR_vs_Mstar_relation(norm, norm_err, slope, slope_err, log10Mstar):
    """
    norm: normalization of the fitting relation in units of Msun/yr (in log-log space)
    norm_err: error on the normalization
    slope: slope of the fitting relation (in log-log space)
    slope_err: error on the slope
    log10Mstar: log10 of stellar mass in units of Msun

    returns: SFR, positive and negative errors on the SFR, all in units of Msun/yr
    """

    log10SFR = slope * (log10Mstar - 10.0) + norm

    # Create scatter by varying slope and normalization
    log10SFR_v1 = (slope - slope_err) * (log10Mstar - 10.0) + norm
    log10SFR_v2 = (slope + slope_err) * (log10Mstar - 10.0) + norm
    log10SFR_v3 = slope * (log10Mstar - 10.0) + (norm + norm_err)
    log10SFR_v4 = slope * (log10Mstar - 10.0) + (norm - norm_err)

    log10SFR_m, log10SFR_p = [], []
    for v1, v2, v3, v4 in zip(log10SFR_v1, log10SFR_v2, log10SFR_v3, log10SFR_v4):
        log10SFR_m.append(min(v1, v2, v3, v4))
        log10SFR_p.append(max(v1, v2, v3, v4))

    log10SFR_m, log10SFR_p = np.array(log10SFR_m), np.array(log10SFR_p)

    SFR = 10.0 ** log10SFR
    SFR_m = 10.0 ** log10SFR_m
    SFR_p = 10.0 ** log10SFR_p
    delta_SFR_m = SFR - SFR_m
    delta_SFR_p = SFR_p - SFR

    return SFR, delta_SFR_m, delta_SFR_p


# Cosmologies
h_obs = 0.7
h_sim = cosmology.h

input_filename = "../raw/Davies2016.txt"
processed = ObservationalData()
raw = np.loadtxt(input_filename)

# Meta-data
name = "Galaxy Stellar Mass - Galaxy sSFR"
comment = (
    "Assumes Chabrier (2003) IMF. "
    "Uses GAMA II equatorial dataset with redshifts from z=0 to 0.35. "
    "Plots fitting relations to the actual data in four redshift bins, "
    " which are defined using a normalization and a slope. "
    "The fits correspond to active galaxies only.The authors fit a line to the peak of the blue population and the "
    "trough between blue and red populations in the u − r colour distribution. Galaxies which lie below the trough are "
    "classed as star forming."
    "The fitting range is valid within 9.25 < log10[M*/Msun] < 12. "
    "Cosmology: H0 = 70 kms-1 Mpc-1, Omega_lambda = 0.7 and Omega_m = 0.3."
)
citation = "Davies et al. (2016) (GAMA, SF)"
bibcode = "2016MNRAS.461..458D"
plot_as = "line"

# Store metadata at the top level
multi_z = MultiRedshiftObservationalData()
multi_z.associate_citation(citation, bibcode)
multi_z.associate_name(name)
multi_z.associate_comment(comment)
multi_z.associate_cosmology(cosmology)
multi_z.associate_maximum_number_of_returns(1)

output_filename = "Davies2016.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Define stellar masses for the fitting relations from Davies et al. (2016)
Mstar = np.logspace(9.25, 11.5, 20)
log10Mstar = np.log10(Mstar)

for i in range(np.shape(raw)[0]):

    # Fetch the fields we need
    z_left, z_right, _, _, slope, slope_err, norm, norm_err, *_ = raw[i, :]

    # Compute mean redshift of the bin using its edges
    z_c = 0.5 * (z_left + z_right)

    # Compute SFR using the fitting relations from Davies et al. (2016)
    SFR, delta_SFR_m, delta_SFR_p = SFR_vs_Mstar_relation(
        norm=norm,
        norm_err=norm_err,
        slope=slope,
        slope_err=slope_err,
        log10Mstar=log10Mstar,
    )

    # Create a single observational-data instance at redshift z
    processed = ObservationalData()

    # Define y scatter as a unyt array
    sSFR_scatter = unyt.unyt_array(
        (delta_SFR_m / Mstar, delta_SFR_p / Mstar), units="1/yr"
    )
    # Define y values as a unyt array
    sSFR = unyt.unyt_array(SFR / Mstar, units="1/yr")

    # Define x values as a unyt array. Also, apply the h-correction factor to Mstar
    # (Mstar \propto D_Lum ** 2 \propto 1/h**2). Note that the dependence on h for sSFR
    # is expected to cancel out.
    Mstar_Msun = unyt.unyt_array(Mstar * (h_sim / h_obs) ** -2, units="Msun")

    processed.associate_x(
        Mstar_Msun,
        scatter=None,
        comoving=False,
        description="Galaxy Stellar Mass",
    )
    processed.associate_y(
        sSFR,
        scatter=sSFR_scatter,
        comoving=False,
        description="Specific Star Formation Rate (sSFR)",
    )

    processed.associate_redshift(z_c, z_left, z_right)
    processed.associate_plot_as(plot_as)

    multi_z.associate_dataset(processed)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
