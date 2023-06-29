#  Hybrid MD decision making package
#
#  Copyright (c) Tamas K. Stenczel 2021-2023.
"""Refitting of ACE models on the fly"""
import os
import subprocess
from time import time

import ase.io
from hybrid_md.refit import save_previous_model_files
from hybrid_md.state_objects import HybridMD


def refit_external_fit(state: HybridMD):
    """ACE model refitting, executes an external Julia program called fit.jl"""

    # extract main settings
    refit_settings = state.settings.refit

    # move any files leftover from the last fit
    save_previous_model_files(state)

    # gather training set
    frames_train = ase.io.read(state.xyz_filename, ":") + state.get_previous_data()

    # training structures
    ase.io.write("train.xyz", frames_train)

    # fit the model
    fit_str = "julia --project={} fit.jl".format(
        os.environ.get("JULI1A_PROJECT", os.getcwd())
    )

    # fit the model
    proc = subprocess.run(
        fit_str,
        shell=True,
        capture_output=True,
        text=True,
    )

    # print the outputs to file
    with open(f"{refit_settings.gp_name}.fit-stdout.{time()}.txt", "w") as file:
        file.write(proc.stdout)
    with open(f"{refit_settings.gp_name}.fit-stderr.{time()}.txt", "w") as file:
        file.write(proc.stderr)

    if proc.returncode != 0:
        raise RuntimeError(
            f"Fitting program failed with exit code {proc.returncode}: {fit_str}"
        )
