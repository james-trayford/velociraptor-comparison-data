from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
import glob

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmologies
h_sim = cosmology.h

# conversion for output as a representative 12+log10(OH) value
twelve_plus_log_OH_solar = 8.69

input_filename = "../raw/konstantopoulou23_*.txt"

output_filename = "Konstantopoulou23_{}.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = {}
exgals = ["grbs", "dlas"]


def stringify_z(z):
    """
    Eagle-style text formatting of redshift label.
    Example: z=1.5 will be printed as z001p500.

    z: The redshift to produce a label for
    """
    whole = int(z)
    frac = int(1000 * (z - whole))
    return f"z{whole:03d}p{frac:03d}"


def read_tex_tables():
    """
    Read the LaTex formatted tables for the data, returning a dictionary object.
    """
    for fname in glob.glob("../raw/konstantopoulou23*"):
        abstype = fname.split(".")[-2].split("_")[-1]
        fields = ["Z", "Z_sigma", "DTM", "DTM_sigma", "z"]
        idxs = [-2, -6]
        dset = [[]] * len(fields)
        haszs = False
        if abstype in exgals:
            # fields.append('z')
            # dset.append([])
            haszs = True
        with open(fname) as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == "#":
                    continue
                els = line.split("&")
                inc = 0
                for i in idxs:
                    nums = els[i].split("$\pm$")
                    if len(nums) < 2:
                        # add value and error
                        dset[inc] = [*dset[inc], np.nan]
                        inc += 1
                        dset[inc] = [*dset[inc], np.nan]
                    else:
                        dset[inc] = [*dset[inc], float(nums[0])]
                        inc += 1
                        dset[inc] = [*dset[inc], float(nums[1])]
                    inc += 1
                if haszs:
                    # add redshift where applicable
                    dset[inc] = [*dset[inc], float(els[1])]
                else:
                    dset[inc] = [*dset[inc], 0.0]
        data[abstype] = np.column_stack(dset)
    return data


def process_for_redshift(zs, data):
    processed = ObservationalData()

    comment = (
        "Konstantopoulou et al. (2023). Obtained using VLT, X-shooter & HST for a combination of"
        "sources: MW, LMC, SMC, QSO-DLA and GRBs."
    )
    citation = "Konstantopoulou et al. (2023)"
    bibcode = "10.48550/arXiv.2310.07709"
    name = (
        "Dust-to-metal ratio as a function of metallicity (represented as O abundance)"
    )
    plot_as = "points"
    h = cosmology.h

    for i in range(len(zs) - 1):
        combination = []
        for src in data.keys():
            bdx = np.logical_and(
                data[src][:, -1] >= zs[i], data[src][:, -1] < zs[i + 1]
            )

            zcen = (zs[i + 1] + zs[i]) / 2
            redshift = zcen
            print(redshift)
            combination.append(data[src][bdx, :])
        combdat = np.vstack(combination)
        combdat = combdat[~np.isnan(combdat).any(axis=-1)]
        OH = (combdat[:, 0] + twelve_plus_log_OH_solar) * unyt.dimensionless
        OH_err = np.row_stack([combdat[:, 1]] * 2) * unyt.dimensionless
        # np.row_stack([combdat[:,1],-combdat[:,1]])+OH
        DTM = combdat[:, 2] * unyt.dimensionless
        DTM_err = np.row_stack([combdat[:, 3]] * 2) * unyt.dimensionless

        processed.associate_x(
            OH, scatter=OH_err, comoving=True, description="Gas Phase 12 + log10(O/H)"
        )
        processed.associate_y(
            DTM, scatter=DTM_err, comoving=True, description="Phi (GDMF)"
        )
        processed.associate_citation(citation, bibcode)
        processed.associate_name(name)
        processed.associate_comment(comment)
        processed.associate_redshift(redshift)
        processed.associate_plot_as(plot_as)
        processed.associate_cosmology(cosmology)

        output_path = f"{output_directory}/{output_filename.format(stringify_z(zcen))}"

        if os.path.exists(output_path):
            os.remove(output_path)

        processed.write(filename=output_path)


z_bins = [0, 0.5, 1, 2, 3, 7]
data = read_tex_tables()
process_for_redshift(z_bins, data)
