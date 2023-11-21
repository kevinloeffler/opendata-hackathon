from lib.preprocessing import read_data

data = read_data('data/fill-level.csv')
print(data.iloc[2: 10])


