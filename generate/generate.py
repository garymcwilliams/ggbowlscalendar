#!/usr/bin/env python

# generate match yml file

from datetime import date, timedelta

matchdata = []
idx = 0
file = open("matches.txt", "r")
for line in file:
    if idx == 0:
        me = line.rstrip()
    elif idx == 1:
        filename = line.rstrip()
    elif idx == 2:
        duration = line.rstrip()
    elif idx == 3:
        year, month, day = line.split(",")
        curdate = date(int(year), int(month), int(day))
    elif idx == 4:
        start_time = line.rstrip()
    else:
        where, opp, delta = line.rstrip().split(" ")
        curdate = curdate + timedelta(days=int(delta))
        print(f"{curdate} {where} {opp}")
        matchdata.append(f"- {where}: {opp}")
        matchdata.append(f"  date: '{curdate}'")
        matchdata.append("  our_score: 0")
        matchdata.append("  opp_score: 0")
    idx += 1

savefile = f"{filename}.yml"
print(f"Saving {savefile}")
with open(f"{savefile}", 'w') as f:
    f.write(f"me: {me}\n")
    f.write(f"start_time: '{start_time}'\n")
    f.write(f"duration: {duration}\n")
    f.write("matches:\n")
    for item in matchdata:
        f.write(f"{item}\n")
