import pandas as pd
import numpy as np

'''
MIT License

Copyright (c) 2020 Faviola Molina - dLab - Fundación Ciencia y Vida

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

def readingData(inputFile):

    df = pd.read_csv(inputFile)
    print(df.columns.to_list())

    return df

def selectingData(df):

    temp = df.loc[df['state'] == 'New York'].copy()
    temp.drop(columns = 'state', inplace = True)
    temp['fips'].fillna(99999,inplace = True)

    df_ny = temp.astype({'fips': 'int32'}).copy()
    df_ny.sort_values('date', inplace= True)
    df_ny.reset_index(inplace = True, drop = True)

    return df_ny

def writingData(df):

    df.to_csv('../output/raw_epidemiology_NY_std.csv', index = False)

if __name__ == '__main__':

    df = readingData('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    df_ny = selectingData(df)
    writingData(df_ny)
