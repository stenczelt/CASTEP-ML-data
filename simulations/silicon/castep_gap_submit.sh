#!/bin/bash

#SBATCH --job-name=JOB_NAME
#SBATCH --nodes=1
#SBATCH --tasks-per-node=128
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00

#SBATCH --account=e89-oxc
#SBATCH --partition=standard
#SBATCH --qos=standard

# --------------------------------------------------------------------
# settings:
#   EDIT THIS FOR SPECIFYING THE CASTEP FILENAME SEED
castep_seed=liqSi_250

/bin/echo -------------------------------------------------------------
/bin/echo Running on host: $(hostname)
/bin/echo Started on: $(date)
/bin/echo Castep seed: $castep_seed
/bin/echo -------------------------------------------------------------

# modules for QUIP & CASTEP installation
module load cray-python
module switch PrgEnv-cray PrgEnv-gnu
module load PrgEnv-gnu
module load cpe
module load mkl

# Python & path to programs
source /path/to/venv/bin/activate
export PATH="/path/to/castep-gap-2023-03-11/bin/:$PATH"
castep_exe=/path/to/castep-gap-2023-03-11/bin/castep.mpi

# CASTEP & GAP (implicit)
export OMP_NUM_THREADS=1
export OMP_PLACES=cores
srun --hint=nomultithread --distribution=block:block $castep_exe $castep_seed

/bin/echo -------------------------------------------------------------
/bin/echo Finish on: $(date)
/bin/echo -------------------------------------------------------------

