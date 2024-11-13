import pandas as pd # type: ignore
import json

# Load CSV file
df = pd.read_csv('fake-soldier-data.csv')

soldiers_data = df.to_dict(orient='records')
with open('soldiers_data.json', 'w') as json_file:
    json.dump(soldiers_data, json_file, indent=4)
