import pandas as pd
import numpy as np
import utils

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

def selectingData(df,source):

    county = utils.counties(source)

    temp = df.loc[df['state'] == 'New York'].copy()
    temp.drop(columns = 'state', inplace = True)
    aux1 = temp['fips'].loc[temp['county'] == 'Unknown'].fillna(90036)
    temp['fips'].loc[temp['county'] == 'Unknown'] = aux1.copy()
    aux2 = temp['fips'].loc[temp['county'] == 'New York City'].fillna(99999)
    temp['fips'].loc[temp['county'] == 'New York City'] = aux2.copy()
    date_list = temp['date'].unique()

    print(temp['county'].unique())

    k = 0
    for i in date_list:
        t = [i] * len(county)
        df_date = pd.DataFrame(data={'date': t})

        df = pd.DataFrame(np.zeros((len(county), 2)), columns=['cases', 'deaths'])
        cases_county = temp['cases'].loc[temp['date'] == i].to_list()
        deaths_county = temp['deaths'].loc[temp['date'] == i].to_list()
        county_list = temp['county'].loc[temp['date'] == i].copy()

        j = 0
        for row in county_list:
            idx = county.loc[county['county'] == row].index.values
            if idx.size > 0:
                df.loc[idx, 'cases'] = cases_county[j]
                df.loc[idx, 'deaths'] = deaths_county[j]
                j += 1

        aux = pd.concat([df_date, county, df.astype(int)], axis=1)

        if k == 0:

            df_ny = aux.copy()

        else:
            df_ny = pd.concat([df_ny,aux], axis=0)

        k += 1

    df_ny.reset_index(inplace = True, drop = True)

    return df_ny

def writingData(df,outfile):

    df.to_csv(outfile, index = False)

if __name__ == '__main__':

    source = 'NYT'

    df = readingData('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    df_ny = selectingData(df,source)
    writingData(df_ny,'../output/NYTimes/NYTraw_epidemiology_NY_std.csv')
