# Silicon data supporting "Machine-learned acceleration for molecular dynamics in CASTEP"

## liquid Si speedtest 


completed in two parts on one node (128 cores) of the ARCHER2 HPC, UK:  
 
1. 24 hours of walltime to 89,710 timesteps  
2. remaining 10,290 to 100,000 total timesteps in 2.88 hours  

part 1. walltime: 86550.40 s  
part 1. time in scf: 2389.63 s  
part 1. time in gap_fit: 2350.11 s  
part 1. time in GAP-driven MD: 80115.57 s  

part 2. walltime: 10390.33 s  
part 2. time in scf: 68.28 s  
part 2. time in gap_fit: 556.16 s  
part 2. time in GAP-driven MD: 9765.89 s  

total combined walltime: 96940.33 s  
total combined time in scf: 2457.91 s  
total combined time in gap_fit: 2906.27 s  
total combined time in GAP-driven MD: 91576.15 s  

timing data for the 1st part of the simulation can be found in slurm-3769328.out
