#!/bin/bash

#SBATCH --job-name=Al2O3-0
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

# modules for CASTEP installation
module load PrgEnv-gnu/8.3.3
module load cray-fftw/3.3.10.3
module load cray-python/3.9.13.1
module load mkl/2023.0.0

# Python & path to programs
castep_exe=/work/e89/e89/tksukcp/opt/castep-vanilla/obj/linux_x86_64_gfortran10-XT--mpi/castep.mpi

# CASTEP & GAP (implicit)
export OMP_NUM_THREADS=1
export OMP_PLACES=cores
srun --hint=nomultithread --distribution=block:block $castep_exe al2o3-120

/bin/echo -------------------------------------------------------------
/bin/echo Finish on: $(date)
/bin/echo -------------------------------------------------------------

