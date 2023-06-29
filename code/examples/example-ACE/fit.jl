using ACE1pack

train_xyz = "$(@__DIR__)/train.xyz"
elements = [:O, :Al]
e_ref = Dict(:O => -388.4671, :Al => -105.5907)
rcut = 5.0
order = 2
totaldegree = 10
weights = Dict("default" => Dict("E" => 30.0, "F" => 1.0 , "V" => 1.0 ))

model = acemodel(
    elements = elements,
    Eref = e_ref,
    rcut = rcut,
    order = order,
    totaldegree = totaldegree
)

acefit!(
    model, JuLIP.read_extxyz(train_xyz);
    solver = ACEfit.BayesianLinearRegressionSVD(),
    weights = weights,
    energy_key = "QM_energy",
    force_key = "QM_forces",
    virial_key = "QM_virial",
	mode = :distributed
	)

export2lammps("ACE-lmp.yace", model)

ACE1pack.linear_errors(
    JuLIP.read_extxyz(train_xyz), model;
    energy_key = "QM_energy",
    force_key = "QM_forces",
    virial_key = "QM_virial"
)

