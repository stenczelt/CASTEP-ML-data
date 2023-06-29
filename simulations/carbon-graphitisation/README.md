# Graphitisation data supporting "Machine-learned acceleration for molecular dynamics in CASTEP"

The data is arranged in the following format:

## 10k_atoms
In this folder there is a final structure (in .xyz format) at the end of the annealing process for both the ML+CASTEP and C-GAP-17 driven runs. There is also bond angle distrubtion, ring statistics and radial distribution function. Within the .xyz, there is coordination information ('n_neighb')

## 200_atoms
This folder contains the trajectory information for the C-GAP-17 run (done in LAMMPS) and also the ML+CASTEP run (done within CASTEP MD). We also provide the input .yaml (which contains the gap_fit string) and CASTEP parameter files. There is also a tar'd DFT_data folder which contains the 10x5x5 structures for the error analysis along with the CASTEP output. The energies and forces used for the error matrix can be found in the respective .npy file which can be readily loaded into numpy for analysis. 

## ML-CASTEP-potential
The potential used to drive the 10k atom system is located in this folder along with the training .xyz file used during the 200 atom ML+CASTEP run. In the train.xyz there are 2 key columns: "QM_forces" and "FF_forces" which correspond to the DFT computed forces and the forces computed using the generated on-the-fly potential respectively.
