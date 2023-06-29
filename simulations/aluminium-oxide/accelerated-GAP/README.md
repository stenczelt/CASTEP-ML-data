# Al2O3 experiment


## Experiment
We are performing MD of a cell of Al2O3, with 118 atoms - one Al and one O deleted. This can easily be used for 
investigating vacancy migration. The current simulation is done on a single temperature of 2500K, one can easily repeat 
this on a range of temperatures in parallel, for drawing scientific conclusions as well. 

## How to reproduce simulation
You will find the raw inputs and job outputs as well. In order to reproduce this calculation, you need to take the 
following files:
- `al2o3-120.cell` & `al2o3-120.param` CASTEP inputs
- `al2o3-120.hybrid-md-input.yaml` settings of the acceleration program
- `job.archer2.sh`: job script, adapt to your own HPC setup. This one was used on Archer2.

n.b. the program is not deterministic, the initial positions will have added noise as well as initial guesses will have
various sources randomness at initialisation, so the steps where refitting happens and the plots will not be exactly 
the same. 

## Analysis

In order to produce the plots below, you need to perform the following steps:
1. run: `grep "<-- Hybrid-MD" al2o3-120.castep > al2o3-120.castep.tmp`. This cuts the relevant lines from the .castep
file for parsing by the Python scripts below. This is optional, though the scripts expect he output file rather than 
the .castep file.
2. Convert the .castep file's content to a CSV - `python analyse.py`. This CSV is enough to reproduce the plots now.
3. Create the plots: `python plot.py`. This will create 2 energy and 2 force error plots, with a shorter and a longer x
axis for both.


# file size note

GitHub has a file size limit of 100MB, the `al2o3-120.castep.tar` was larger than that, but has been compressed.

In order to see the plain version, please run:
```bash
tar -xvzf al2o3-120.castep.tar.gz
```

Same goes for the `al2o3-120.md` file, which has been compressed and split
```bash
cat al2o3-120.md.tar.gz.parta* > al2o3-120.md.tar.gz
tar -xvzf al2o3-120.md.tar.gz
```