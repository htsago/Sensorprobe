import pandas as pd
import glob

csv_files = glob.glob('D:/Sensorprobe/Test/*.csv')
combined_data = pd.DataFrame()

for file in csv_files:
    data = pd.read_csv(file)
    combined_data = pd.concat([combined_data, data])

combined_data.sort_values(by='R1_1', inplace=False)
combined_data.to_csv('model_new.csv', index=False)

print("Done!")