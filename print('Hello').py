import pandas as pd
df = pd.read_excel('(read)ruggedness-scales-2020-tracts.xlsx', sheet_name='Ruggedness Scales 2020 Data', header=1)
print(df.head())
print('hello')