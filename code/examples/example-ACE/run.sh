#!/bin/bash

# exit on error
set -e

/bin/echo -------------------------------------------------------------
/bin/echo Running on host: $(hostname)
/bin/echo Started on: $(date)
/bin/echo -------------------------------------------------------------
/bin/echo Path to castep.mpi : $(which castep.mpi)
/bin/echo Path to python     : $(which python)
/bin/echo Path to hybrid-md  : $(which hybrid-md)
/bin/echo Path to julia      : $(which julia)
/bin/echo JULIA_PROJECT path : ${JULIA_PROJECT}
/bin/echo -------------------------------------------------------------

mpirun -np 32 castep.mpi al2o3-120

/bin/echo -------------------------------------------------------------
/bin/echo Finish on: $(date)
/bin/echo -------------------------------------------------------------
