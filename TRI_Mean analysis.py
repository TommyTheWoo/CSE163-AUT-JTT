import pandas as pd
df = pd.read_excel('(read)ruggedness-scales-2020-tracts.xlsx', sheet_name='Ruggedness Scales 2020 Data', header=1)
#No missing values.
#zero_rows = df[df['RoadTRI_Min'] == 0]
#print(zero_rows.shape) 
#print((zero_rows['RoadTRI_Count'] == 0).sum())
#Both of these return 0. There are no missing values.
road_TRI_desc = (df.groupby('StateName20')['RoadTRI_Mean'].describe())
print(road_TRI_desc.sort_values(by='mean'))
area_TRI_desc = (df.groupby('StateName20')['AreaTRI_Mean'].describe())
print(area_TRI_desc.sort_values(by='mean'))
