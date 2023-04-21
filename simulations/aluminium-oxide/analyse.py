"""
Extract data from the .castep file.

Reads the tables generated with the hybrid-md package and saves the error and
decision data into a csv file.

Before running this, do the following for better performance
$ grep "<-- Hybrid-MD" al2o3-120.castep > al2o3-120.castep.tmp
"""

import re
from pathlib import Path

import pandas as pd

# filenames of input & output
seed = "al2o3-120"
castep_filename = f"{seed}.castep.tmp"
csv_filename = f"{seed}.data.csv"

# regex for reading the output tables
pattern_block = re.compile(
    r"^.*?(?P<md_iteration>\d+).*?<-- Hybrid-MD$\n"
    r"(?:^.*?<-- Hybrid-MD$\n){3}"
    r"^.*?(?P<ediff>[\d.]+).*?<-- Hybrid-MD$\n"
    r"^.*?(?P<fmax>[\d.]+).*?<-- Hybrid-MD$\n"
    r"^.*?(?P<frmse>[\d.]+).*?<-- Hybrid-MD$\n"
    r"(?:^.*?<-- Hybrid-MD(?:-Cumul)?$\n){10}"
    r"^.*?(?P<action>DECREASE|INCREASE) interval to\s+(?P<new_interval>\d+).*?<-- Hybrid-MD-Adapt$",
    re.MULTILINE,
)

file = Path(castep_filename).open(mode="r")
text = file.read()
data = pattern_block.findall(text)

# deal with restart: add 100k to second part
in_2nd_run = False
for i in range(1, len(data)):
    if in_2nd_run:
        data[i][0] = str(int(data[i][0]) + 100000)
    else:
        if int(data[i - 1][0]) > int(data[i][0]):
            in_2nd_run = True

df = pd.DataFrame(
    data,
    columns=[
        "md_iteration",
        "ediff",
        "fmax",
        "frmse",
        "action",
        "new_interval",
    ],
)

df.to_csv(csv_filename)
