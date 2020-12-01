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

    # This function reads the input file. This is a raw file of the GIT repository
    # The file contains the history of the data for coronavirus in the US for all counties


    df = pd.read_csv(inputFile)
    print(df.columns.to_list())

    return df

def selectingData(df,source):

    # This function reads the list of the counties searched and ordered by C. Valdenegro
    # for the state of New York. This file is a modification of the original,
    # considering that NYT source consider the NY city as a unit. The FIPS for
    # the City of New York was assigned as 99999 for convenience
    # (FIPS for this unit are empty from source). Moreover, the FIPS for the
    # "Unknown" county is chosen as 90036 for keeping consistency with JH data ("Unnasigned" county)

    county = utils.counties(source)

    temp = df.loc[df['state'] == 'New York'].copy()
    temp.drop(columns = 'state', inplace = True)
    aux1 = temp['fips'].loc[temp['county'] == 'Unknown'].fillna(90036)
    temp['fips'].loc[temp['county'] == 'Unknown'] = aux1.copy()
    aux2 = temp['fips'].loc[temp['county'] == 'New York City'].fillna(99999)
    temp['fips'].loc[temp['county'] == 'New York City'] = aux2.copy()
    date_list = temp['date'].unique()

    print(temp['county'].unique())


    # Data in the source is reported for counties and dates with infected cases. Counties
    # with no infected cases (in a certain date) does not appeared in the file.
    # For consistency and standardization counties with no infected people at a given date
    # are filled with zeroes

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

    # The data is concatened in a single file

    df_ny.reset_index(inplace = True, drop = True)

    return df_ny

def writingData(df,outfile):

    # data is written to a single output file

    df.to_csv(outfile, index = False)

if __name__ == '__main__':

    # Establish the source to read
    source = 'NYT'

    # provide the URL of the raw file of the github repository to read

    df = readingData('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    df_ny = selectingData(df,source)

    # provide the name of the output file
    writingData(df_ny,'../output/NYTimes/NYTraw_epidemiology_NY_std.csv')
