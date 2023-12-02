# Open Data Hack 2023

**Goal:** Use an AI model to predict the fill levels of recycling stations in St. Gallen
and create a pathfinding algorithm that finds the ideal routes for city employees.

### Components

1) AI model that predicts future fill levels based on historic data
2) Pathfinding algorithm that finds the optimal order of recycling stations based on the predicted fill levels
3) Optional: Visualise optimal route with a web app or similar

### Setup

Download the file [here](https://www.daten.stadt.sg.ch/explore/dataset/fullstandssensoren-sammelstellen-stadt-stgallen/export/?disjunctive.name&disjunctive.tags&sort=measured_at) 
and safe it at `data/fill-level.csv` or use the `download-data.sh` script.

### API

Use the generate_dummy_data method to receive random sensor values. The model should return the prediction the same way.
The method takes a list of the requested sensor names as argument.

### Ideas
Ideas that can be explored if there is time:
- [ ] Vary the number of inputs, the timeranges, the number of outputs...
- [ ] Add sensor noise threshold
- [ ] Test if training on single sensors is better

### Data
List of all sensor names:
- 107075 | 2B2A
- 107114 | 654B
- 107123 | 980F
- 107122 | 6370
- 107072 | F389
- 107121 | 679F
- 107031 | 6348
- 107128 | 0BCE
- 107047 | 0D1A
- 107096 | 4814
- 107064 | 4B16
- 107054 | 2AE2
- 107065 | 4A3D
- 107115 | 7F12
- 107097 | 0C5C
- 107048 | 671B
- 107055 | 2C76
- 107095 | 64BC
- 107026 | 67BE
- 107043 | 8300
- 107108 | 0AEA
- 107058 | 282C
- 107112 | 2B88
- 107040 | 8572
- 104243
- 107053 | 667E
- 107132 | 255E
- 107038 | 2B8D
- 107104 | 66E0
- 107044 | 63DB
- 107049 | 4B00
- 107127 | 817E
- 104244
- 107109 | 67EF
- 107034 | 8104
- 107067 | 84A1
- 107130 | 4818
- 107077 | 2CC4
- 107057 | 69C8
- 107068 | 4455
- 107062 | 49A3
- 107041 | 470A
