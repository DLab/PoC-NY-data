import pandas as pd
import numpy as np


df = pd.read_csv('../input/cases_diff.csv', index_col='Unnamed: 0')


df2 = df.T
df2.reset_index(level=0, inplace = True)
df2.rename(columns = {'index': 'date'}, inplace = True)
print(df2)
variables = ['date']
identifiers = [x for x in df2.columns if x not in variables]
print(len(identifiers))

