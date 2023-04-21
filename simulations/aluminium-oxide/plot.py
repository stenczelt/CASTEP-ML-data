"""Plotting of results, using CSV of data extracted from .castep file

Plots the following things:
- energy & force RMSE plots with 0-1 ps & 0-100 ps x_lim
- adds horizontal lines indicating the tolerances we used
- vertical lines for when refitting has happened 

"""
import matplotlib
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# global settings
figsize = (10, 6)
matplotlib.rcParams.update({"font.size": 16})
plot_kwargs = dict(marker="o", markeredgewidth=0.0)

frmse_tolerance = 0.3  # eV/Å
energy_tolerance = 5  # meV/atom

# read the dataR
df = pd.read_csv("al2o3-120.data.csv")

# convert
df["ediff"] *= 1000  # meV/atom

# annotate with MD time
df["time"] = df["md_iteration"] * 0.001

# energy plot
fig, ax = plt.subplots(figsize=figsize)
sns.lineplot(ax=ax, data=df, x="time", y="ediff", **plot_kwargs)
ax.set_ylabel("energy error meV/atom")
ax.set_xlabel("time / ps (1fs timestep)")

for val in df[df["action"] == "DECREASE"].time:
    ax.axvline(val, c="tab:gray", linestyle=":")
ax.axhline(energy_tolerance, c="tab:red", label="limit: 5meV/atom")
ax.legend()

for x_lim in [
    (-5, 105),
    (-0.05, 1),
]:
    ax.set_xlim(x_lim)
    fig.tight_layout()
    fig.savefig(f"plot_Al2O3_energy-{x_lim[1]}.pdf")

# forces plot
fig, ax = plt.subplots(figsize=figsize)
sns.lineplot(ax=ax, data=df, x="time", y="frmse", label="F diff, RMSE", **plot_kwargs)

ax.set_ylabel("force RMSE eV/Å")
ax.set_xlabel("time / ps (1fs timestep)")

for val in df[df["action"] == "DECREASE"].time:
    ax.axvline(val, c="tab:gray", linestyle=":")

ax.axhline(frmse_tolerance, c="tab:red", label="limit F-RMSE 0.5eV/Å")
ax.set_ylim(0, 0.4)
ax.legend()

for x_lim in [
    (-5, 105),
    (-0.05, 1),
]:
    ax.set_xlim(x_lim)
    fig.tight_layout()

    fig.tight_layout()
    fig.savefig(f"plot_Al2O3_forces-{x_lim[1]}.pdf")
