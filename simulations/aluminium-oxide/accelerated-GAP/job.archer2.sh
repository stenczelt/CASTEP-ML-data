#!/bin/bash

#SBATCH --job-name=Al2O3-1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00

#SBATCH --account=e89-came
#SBATCH --partition=standard
#SBATCH --qos=long

/bin/echo -------------------------------------------------------------
/bin/echo Running on host: $(hostname)
/bin/echo Started on: $(date)
/bin/echo -------------------------------------------------------------

# modules for QUIP & CASTEP installation
module switch PrgEnv-cray PrgEnv-gnu/8.1.0
module load PrgEnv-gnu/8.1.0
module load cpe/22.04
module load mkl/2023.0.0

# Python & path to programs
source /work/e89/e89/tksukcp/castep-restart/install-2023-03-11/venv/bin/activate
export PATH="/work/e89/e89/tksukcp/castep-restart/install-2023-03-11/bin/:$PATH"
castep_exe=/work/e89/e89/tksukcp/castep-restart/install-2023-03-11/bin/castep.mpi

which gap_fit
which hybrid-md


# CASTEP & GAP (implicit)
export OMP_NUM_THREADS=1
export OMP_PLACES=cores
srun --hint=nomultithread --distribution=block:block $castep_exe al2o3-120

/bin/echo -------------------------------------------------------------
/bin/echo Finish on: $(date)
/bin/echo -------------------------------------------------------------
