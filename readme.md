# Open Data Hack 2023

**Goal:** Use an LSTM AI model to predict the fill levels of recycling stations in St. Gallen
and create a pathfinding algorithm that finds the ideal routes for city employees, for the next work week.

### Components

1) AI model that predicts future fill levels based on historic data
2) Pathfinding algorithm that finds the optimal order of recycling stations based on the predicted fill levels and location
3) Visualise optimal route with a web app

### Setup
Create a conda environment with `conda create --name <env> --file requirements.txt`. We recommend using python version 3.9.

Create a Google Maps API key and save it for later steps (you can easily find the documentation online).

Run the bash script `download-data.sh`. This will download the data to the data folder. Afterwards run `preprocessing.py` directly which will create a single csv file from all the 3 datasets.

##### Alternative Setup:
Download the files below into the data folder: 
- [Füllstandsensoren Glassammelstellen (Weissglas)](https://www.daten.stadt.sg.ch/explore/dataset/fuellstandsensoren-glassammelstellen-weissglas/table/?disjunctive.device_id&disjunctive.name)
- [Füllstandsensoren Glassammelstellen (Grünglas)](https://www.daten.stadt.sg.ch/explore/dataset/fuellstandsensoren-glassammelstellen-gruenglas/table/?disjunctive.device_id&disjunctive.name)
- [Füllstandsensoren Glassammelstellen (Braunglas)](https://www.daten.stadt.sg.ch/explore/dataset/fuellstandsensoren-glassammelstellen-braunglas/table/?disjunctive.device_id&disjunctive.name)

#### Train the model
To train the model, the datasets must be available and merged (as done in the Setup step). The file must be available under data/days_merged.csv. Afterwards, you can execute `main.py` in the project root which will train the model and save a snapshot to the trained-models/ folder.

#### API
The Google Maps API key must be saved under as `MAPS_KEY=<key>` in a .env file in the project root.

In order to use the model, the datasets must be available and merged (as done in the Setup step). Also, the model must be trained. Afterwards, the command `flask --app lib/api run` can be executed from the project root. 

#### UI
The Google Maps API key must be saved in a second location as `REACT_APP_GOOGLE_MAPS_API_KEY=<key>` in a .env file in the predictor-app/ folder.

The UI is located in the predictor-app/ folder. First run `npm install` in the given folder, the start it using `npm run start`.

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
