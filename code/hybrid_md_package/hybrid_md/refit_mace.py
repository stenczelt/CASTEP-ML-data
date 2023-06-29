#  Hybrid MD decision making package
#
#  Copyright (c) Tamas K. Stenczel 2021-2023.
"""Refitting of MACE models on the fly"""
from argparse import Namespace
from typing import Optional

import ase.io

from hybrid_md.state_objects import HybridMD
from mace.model_training import train_mace_model
from mace.tools import CheckpointIO

RANDOM_SEED = 123


class ExtendedCheckpointIO(CheckpointIO):
    def get_last_epoch_number(self, swa=True):
        all_file_paths = self._list_file_paths()
        checkpoint_info_list = [
            self._parse_checkpoint_path(path) for path in all_file_paths
        ]
        selected_checkpoint_info_list = [
            info for info in checkpoint_info_list if info and info.tag == self.tag
        ]

        if len(selected_checkpoint_info_list) == 0:
            return None

        latest_checkpoint_info = max(
            selected_checkpoint_info_list, key=lambda info: info.epochs
        )

        return latest_checkpoint_info.epochs


def choose_device():
    import torch

    if torch.cuda.is_available():
        print("USING CUDA for MACE fitting with Hybrid-md")
        return "cuda"
    print("USING CPU for MACE fitting with Hybrid-md")
    return "cpu"


def refit_generic(
    state: HybridMD,
    device=None,
    random_seed=RANDOM_SEED,
    model_kwargs: Optional[dict] = None,
):
    """Refit a MACE model

    Parameters
    ----------
    state: HybridMD
    device: device for torch
    random_seed
    model_kwargs
    """

    # extract main settings
    refit_settings = state.settings.refit

    # settings
    model_name = refit_settings.gp_name  # JIT-compiled model which we can run in LAMMPS
    epochs_initial = 500
    epochs_additional = 100
    epoch_swa_from = 0.8  # fraction of the total

    # see if first one or not
    checkpoint_io = ExtendedCheckpointIO(
        directory="checkpoints",
        tag=f"MACE_model_run-{RANDOM_SEED}",
        keep=True,
    )
    last_epoch = checkpoint_io.get_last_epoch_number()
    if last_epoch is None:
        # no checkpoint, so we are starting from scratch
        max_num_epochs = epochs_initial
        start_swa = int(max_num_epochs * epoch_swa_from)
        print("Starting MACE training from scratch")
    else:
        max_num_epochs = last_epoch + epochs_additional
        start_swa = last_epoch + int(epochs_additional * epoch_swa_from)
        print(f"Continuing MACE training from epoch {last_epoch}")

    # gather training set
    train_frames = state.get_previous_data() + ase.io.read(state.xyz_filename, ":")

    # training structures
    ase.io.write("train.xyz", train_frames)

    # arguments & overwrites
    train_args = default_args()
    if device is None:
        train_args["device"] = choose_device()
    else:
        train_args["device"] = device

    train_args.update(
        dict(
            max_num_epochs=max_num_epochs,
            start_swa=start_swa,
            seed=random_seed,
        )
    )
    if model_kwargs:
        train_args.update(model_kwargs)

    # training
    model = train_mace_model(Namespace(**train_args))

    # JIT-compiled model
    convert_to_lammps(model, model_name)


def convert_to_lammps(model, out_path):
    from e3nn.util import jit
    from mace.calculators import LAMMPS_MACE

    model = model.double().to("cpu")
    lammps_model = LAMMPS_MACE(model)
    lammps_model_compiled = jit.compile(lammps_model)
    lammps_model_compiled.save(out_path)


def default_args():
    return {
        "name": "MACE_model",
        "batch_size": 10,
        "valid_batch_size": 1,
        "r_max": 4.5,
        "max_num_epochs": 50,
        "swa": True,
        "start_swa": 40,
        # ------------------------------------
        "model": "MACE",
        "device": "cpu",
        "seed": RANDOM_SEED,
        "log_dir": "logs",
        "model_dir": ".",
        "checkpoints_dir": "checkpoints",
        "results_dir": "results",
        "downloads_dir": "downloads",
        "default_dtype": "float64",
        "log_level": "INFO",
        "error_table": "PerAtomRMSE",
        "num_radial_basis": 8,
        "num_cutoff_basis": 5,
        "interaction": "RealAgnosticResidualInteractionBlock",
        "interaction_first": "RealAgnosticResidualInteractionBlock",
        "max_ell": 3,
        "correlation": 3,
        "num_interactions": 2,
        "MLP_irreps": "16x0e",
        "radial_MLP": "[64, 64, 64]",
        "hidden_irreps": "32x0e+32x1o",
        "num_channels": None,
        "max_L": None,
        "gate": "silu",
        "scaling": "rms_forces_scaling",
        "avg_num_neighbors": 1,
        "compute_avg_num_neighbors": True,
        "compute_stress": False,
        "compute_forces": True,
        "train_file": "train.xyz",
        "valid_file": None,
        "valid_fraction": 0.1,
        "test_file": None,
        "E0s": "average",
        "energy_key": "QM_energy",
        "forces_key": "QM_forces",
        "virials_key": "QM_virial-NOT-USED",
        "stress_key": "stress",
        "dipole_key": "dipole",
        "charges_key": "charges",
        "loss": "weighted",
        "forces_weight": 100.0,
        "swa_forces_weight": 100.0,
        "energy_weight": 1.0,
        "swa_energy_weight": 1000.0,
        "virials_weight": 1.0,
        "swa_virials_weight": 10.0,
        "stress_weight": 1.0,
        "swa_stress_weight": 10.0,
        "dipole_weight": 1.0,
        "swa_dipole_weight": 1.0,
        "config_type_weights": "'{Default:1.0}'",
        "huber_delta": 0.01,
        "optimizer": "adam",
        "lr": 0.01,
        "swa_lr": 0.001,
        "weight_decay": 5e-07,
        "amsgrad": True,
        "scheduler": "ReduceLROnPlateau",
        "lr_factor": 0.8,
        "scheduler_patience": 50,
        "lr_scheduler_gamma": 0.9993,
        "ema": True,
        "ema_decay": 0.99,
        "patience": 2048,
        "eval_interval": 2,
        "keep_checkpoints": False,
        "restart_latest": True,
        "save_cpu": False,
        "clip_grad": 10.0,
        "wandb": False,
        "wandb_project": "",
        "wandb_entity": "",
        "wandb_name": "",
        "wandb_log_hypers": [
            "num_channels",
            "max_L",
            "correlation",
            "lr",
            "swa_lr",
            "weight_decay",
            "batch_size",
            "max_num_epochs",
            "start_swa",
            "energy_weight",
            "forces_weight",
        ],
    }
