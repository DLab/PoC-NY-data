import pandas as pd
import numpy as np


df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

print(df.columns.to_list())

temp = df.loc[df['state'] == 'New York'].copy()

temp.drop(columns = 'state', inplace = True)

temp['fips'].fillna(99999,inplace = True)

df_ny = temp.astype({'fips': 'int32'}).copy()

df_ny.sort_values('date', inplace= True)

df_ny.reset_index(inplace = True, drop = True)

df_ny.to_csv('../output/raw_epidemiology_NY_std.csv', index = False)
