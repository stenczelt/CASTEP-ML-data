"""
Extract the timings from Castep file.

Output with the attached data:
```
processing GAP.xml.fit-stdout.1678758267.2016377.txt
processing GAP_model-step000038-at-2023-03-13_09_04_41/GAP.xml.fit-stdout.1678696033.1055524.txt
processing GAP_model-step007167-at-2023-03-13_18_44_57/GAP.xml.fit-stdout.1678727463.1473866.txt
processing GAP_model-step000123-at-2023-03-13_10_34_33/GAP.xml.fit-stdout.1678698405.4725862.txt
processing GAP_model-step023859-at-2023-03-14_01_34_42/GAP.xml.fit-stdout.1678733625.437086.txt
processing GAP_model-step004248-at-2023-03-13_17_02_47/GAP.xml.fit-stdout.1678706566.6451728.txt
processing GAP_model-step000169-at-2023-03-13_11_18_00/GAP.xml.fit-stdout.1678703905.2394516.txt
processing GAP_model-step000015-at-2023-03-13_08_25_59/GAP.xml.fit-stdout.1678694974.4758544.txt
--------------------------------------------------------------------------------
GAP fit times: ['438.34680204000324', '34.973448025062680', '353.63793154340237', '68.749911988154054', '376.36719116289169', '194.97159587498754', '150.14054326433688', '35.933456109836698']
number of ab-initio steps: 57
number of gap_fit calls: 8
MD steps per ab-initio evaluation: 1754 MD steps per ab-initio
total time 159787.74
number of MD steps 57 100000
total time spent in SCF:     56419.93 s -  35.31%
avg duration of ab-initio calc.:     989.82 s
total time spent in gap_fit    1653.12 -   1.03%
total of other time:   98612.46 s -  61.71%
other time spent per step:          0.99 s
```
"""

import re
from pathlib import Path

# filenames of input & output
seed = "al2o3-120"

# code
castep_filename = f"{seed}.castep"

# regex for reading the output tables
pattern_block = re.compile(
    r"^Initial.*?(?P<init>[\d.]+)\s+<-- SCF$\n"
    r"(?:^.*?<-- SCF$\n){1,100}"
    r".*?(?P<last>[\d.]+)\s+<-- SCF$\n"
    r"------------------------------------------------------------------------ <-- SCF",
    re.MULTILINE,
)

with Path(castep_filename).open(mode="r") as file:
    text = file.read()

scf_times = pattern_block.findall(text)
num_md_steps = len(re.findall(r"Starting MD iteration", text))
total_time = float(re.search(r"Total time\s+=\s+([\d.]+) s", text[-1000:]).group(1))

# print(scf_times)

# calculate time spend in SCF loops
total_scf_time = 0.0
total_other_time = 0.0
t_before = 0
for start, end in scf_times:
    # start: time first SCF cycle (str)
    # end: time of last SCF cycle (str)
    start = float(start)
    end = float(end)

    total_other_time += start - t_before
    total_scf_time += end - start

    t_before = end

t_per_scf_step = total_scf_time / len(scf_times)

# GAP fitting times
gap_fit_times = []
for gap_fn in list(Path(".").glob("GAP.xml.fit-stdout.*.txt")) + list(
    Path(".").glob("GAP_model-step*/GAP.xml.fit-stdout.*.txt")
):
    print("processing", gap_fn)
    # with Path(gap_fn).open(mode="r") as file:
    with gap_fn.open(mode="r") as file:
        gap_fit_times.append(
            re.search(
                r"TIMER: GP sparsify\s+done in [\d.]+ cpu secs, ([\d.]+) wall clock secs",
                file.read(),
            ).group(1)
        )
print("-" * 80)
print("GAP fit times:", gap_fit_times)
print("number of ab-initio steps:", len(scf_times))
print("number of gap_fit calls:", len(gap_fit_times))
print(
    f"MD steps per ab-initio evaluation: {int(num_md_steps / len(scf_times))} MD steps per ab-initio"
)
print("total time", total_time)
print("number of MD steps", len(scf_times), num_md_steps)
total_gap_fit_time = sum(float(x) for x in gap_fit_times)
total_other_time -= total_gap_fit_time

print(
    f"total time spent in SCF:   {total_scf_time:10.2f} s - {total_scf_time / total_time * 100:6.2f}%"
)
print(f"avg duration of ab-initio calc.: {t_per_scf_step:10.2f} s")
print(
    f"total time spent in gap_fit {total_gap_fit_time:10.2f} - "
    f"{total_gap_fit_time / total_time * 100:6.2f}%"
)
print(
    f"total of other time: {total_other_time:10.2f} s - "
    f"{total_other_time / total_time * 100:6.2f}%"
)
print(f"other time spent per step:    {total_other_time / num_md_steps:10.2f} s")
print(total_scf_time + total_other_time, "total")
