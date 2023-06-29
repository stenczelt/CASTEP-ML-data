# Al2O3 MD

## Experiment
We are performing MD of a cell of Al2O3, with 118 atoms - one Al and one O deleted. This can easily be used for 
investigating vacancy migration. The current simulation is done on a single temperature of 2500K, one can easily repeat 
this on a range of temperatures in parallel, for drawing scientific conclusions as well. 

## Simulations tested

All with the same starting structure.

- `accelerated-GAP`: Accelerated MD with GAP model, adaptive stepping method.
- `pure-AIMD`: short 100 step AIMD, no acceleration. Tested for timing: ca 100 steps can be done per day.
