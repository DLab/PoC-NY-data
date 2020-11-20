import pandas as pd
import numpy as np
import glob
import datetime
import re
import requests
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
"""
This script reads the source from Johns Hopkins repository: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports

The source is separated in different files per day. This scripts concatenates the history for the state of New York
"""

class MineData:

    def findingFiles(self,url):

        # This function search for the directory of the daily reports through GitHub API.
        # It list the content and omit the "non-date" files in the directory. It returns
        # a list with the name of the files 'self.dates' (with no format ext), i.e. the
        # publication date and a list with the URL of each file to read

        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            df = pd.DataFrame(req.json())
            todrop = df.loc[df['name'] == '.gitignore']
            df.drop(todrop.index, inplace=True)
            todrop = df.loc[df['name'] == 'README.md']
            df.drop(todrop.index, inplace=True)

            self.dates = [item.replace('.csv', '') for item in df['name']]
            self.downURL = df['download_url'].to_list()
        else:
            print('Content was not found.')

    def readingData(self, source):

        # This function reads the file with the static information of the counties. It is
        # located in the input/utilities directory

        self.county = utils.counties(source)

        self.df_total = pd.DataFrame()

        k = 0
        i = 0
        flag3 = 0

        # starts reading the files in the source
        for date in self.dates:

            print('Processing ' + date)
            temp = pd.read_csv(self.downURL[i])

            # set a standard for the columns names. It is: all lower cases, '_' instead of blanks.
            # It also replace '_' for '/'

            temp.columns = temp.columns.str.replace('/','_')
            temp.columns = temp.columns.str.replace(' ','_')
            temp.columns = temp.columns.str.lower()

            #rename columns to the standar: 'state' and 'country'
            if 'province_state' in temp.columns:
                temp.rename(columns = {'province_state': 'state', 'country_region': 'country'}, inplace = True)

            flag = 0
            flag2 = 0

            # For the first days of the Pandemic reported for the US in this repository, the data
            # was not segregated by counties. From March the 22nd, they started to report counties under
            # the name 'admin2'. It is replace for the standard 'county'

            if 'admin2' in temp.columns:
                temp.rename(columns = {'admin2': 'county'}, inplace = True)
                flag = 1
                if flag3 == 0:
                    day1 = date
                    flag3 = 1

            # until Aug the 30th, Jonhs Hopkins reported the data aggregated to New York City. This is the
            # join data of the 5 counties: 'Bronx', 'Kings', 'New York', 'Queens' and 'Richmond' (equivalent to
            # the boroughs: 'Bronx', 'Brooklyn', 'Manhattan', 'Queens', and 'Staten Island')

                list_county = temp['county'].unique()
                if 'New York' in list_county:
                    if flag2 == 0: print('NYC segregated: ', date)
                    flag2 = 1

            # Select data only from the state of New York

            temp_us = temp.loc[temp['country'] == 'US']
            temp_us_ny = temp_us.loc[temp_us['state'] == 'New York']

            # format the date to the ISO standard: YYYY-mm-dd
            date2 = pd.to_datetime(date).strftime('%Y-%m-%d')

            # standardize the format of the update date provided in each file. However, there are different updates
            # to the same set of data (meaning same state). The publication date was chosen (the date of the name
            # of the file)
            temp_us_ny['last_update'] = pd.to_datetime(temp_us_ny['last_update'], infer_datetime_format=True)
            temp_us_ny['last_update'] = pd.to_datetime(temp_us_ny['last_update']).dt.strftime('%Y-%m-%d')

            if flag == 1:
                if len(temp_us_ny['county']) > 63:
                    print('WARNING: the length of counties in source (added a "new county") is larger than in origin. THIS MAY CAUSE AN ERROR!!!')
                if 'Out of NY' in list_county:
                    todrop = temp_us_ny.loc[temp_us_ny['county'] == 'Out of NY']
                    temp_us_ny.drop(todrop.index, inplace = True)

            temp_us_ny.reset_index(inplace=True, drop=True)

            # This flag is set to identify when the granularity of the data reaches the counties level
            # In order to set a common base for the dates, an array full of zeroes is created
            if flag == 1:
                df = pd.DataFrame(np.zeros((len(self.county), 4)), columns=['cases','deaths','active','recovered'])
                cases_county = temp_us_ny['confirmed'].copy()
                deaths_county = temp_us_ny['deaths'].copy()
                active_county = temp_us_ny['active'].copy()
                recovered_county = temp_us_ny['recovered'].copy()


                # Here the standard date is set, i.e. the publication date (in the name of each file)
                t = [date2]*len(self.county)
                df_date = pd.DataFrame(data={'date': t})

                # The zeroes array change if a value for that county is reported. Otherwise, it remains zero.
                # There is a judgment made here, zeroes where chosen instead of nulls
                j = 0
                for row in temp_us_ny['county']:
                    idx = self.county.loc[self.county['county'] == row].index.values
                    if idx.size > 0:
                        df.loc[idx, 'cases'] = cases_county[j]
                        df.loc[idx, 'deaths'] = deaths_county[j]
                        df.loc[idx, 'active'] = active_county[j]
                        df.loc[idx, 'recovered'] = recovered_county[j]
                        if active_county[j] < 0:
                            print('Actives are negative in this county: ', row,' on date: ', date2)

                        j += 1

                # From Aug the 31st, the granularity of data for the City of New York reached county levels.
                # For consistency, we keep storing the New York City entry by adding the data from the
                # individual boroughs
                if flag2 == 1:
                    list_NYC = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']
                    sum_cases = 0
                    sum_deaths = 0
                    sum_active = 0
                    sum_recovered = 0
                    for cnty in list_NYC:
                        idx = self.county.loc[self.county['county'] == cnty].index.values
                        sum_cases += df.loc[idx, 'cases'].item()
                        sum_deaths += df.loc[idx, 'deaths'].item()
                        sum_active += df.loc[idx, 'active'].item()
                        sum_recovered += df.loc[idx, 'recovered'].item()

                    idxNYC = self.county.loc[self.county['county'] == 'New York City'].index.values
                    df.loc[idxNYC,'cases'] = sum_cases
                    df.loc[idxNYC,'deaths'] = sum_deaths
                    df.loc[idxNYC,'active'] = sum_active
                    df.loc[idxNYC,'recovered'] = sum_recovered


                # The dates are concatenated into a single dataframe
                aux = pd.concat([df_date, self.county, df.astype(int)], axis=1)

                if k == 0:

                    self.df_total = aux.copy()

                else:
                    self.df_total = pd.concat([self.df_total,aux], axis=0)

                k += 1
            i += 1

            alert = self.df_total.isnull().values.any()
            if alert == True:
                print('CHANFLE ', date)

    def recoveredCases(self):

        # recovered cases are not reported by Johns Hopkins. They are read from the repository above.
        # This is keep reading them in the case the correct the report.
        # Meanwhile, the "MinSal" methodology is not shown but inferred that is:
        # "recovered(t) = cases(t - 14 days) - deaths(t)"
        # It is a good exercise to include hospitalized when the data will ingested
        # "recovered(t) = cases(t - 14 days) - deaths(t) - hopitalized(t)"

        day1 = self.df_total['date'].iloc[0]
        dates = self.df_total['date'].unique()
        counties = self.df_total['county'].unique()

        recovered1 = [0]*14*len(counties) # no recovered people during the first 14 days
        recovered2 = []
        for day in dates:
            total_days = (pd.to_datetime(day) - pd.to_datetime(day1)).days
            if total_days >= 14:
                active_start = (pd.to_datetime(day) - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
                aux1 = self.df_total['cases'].loc[self.df_total['date'] == active_start]
                aux1.reset_index(inplace=True, drop=True)
                aux2 = self.df_total['deaths'].loc[self.df_total['date'] == day]
                aux2.reset_index(inplace=True, drop=True)
                recovered2.append(aux1.subtract(aux2).to_list())

        flatList = [item for sublist in recovered2 for item in sublist]
        recovered = recovered1 + flatList

        self.df_recovered = pd.Series(recovered, name = 'recovered')

    def activeCases(self):

        # active cases are reported by Johns Hopkins using the WHO methodology:
        # "active(t) = cases - deaths - recovered"
        # However, as they always report zero recovered, it is equivalent to only
        # subtract accumulated deaths from accumulated cases. The active data is still
        # read from the repository above. This is keep reading them in the case the
        # correct their report.

        # Meanwhile, we use the WHO methodology above in order to calculate the
        # active cases, using our estimate of "recovered".

        dates = self.df_total['date'].unique()

        active = []
        for day in dates:
            aux1 = self.df_total['cases'].loc[self.df_total['date'] == day]
            aux2 = self.df_total['deaths'].loc[self.df_total['date'] == day]
            aux3 = self.df_total['recovered'].loc[self.df_total['date'] == day]
            aux4 = aux1.subtract(aux2)
            active.append(aux4.subtract(aux3).to_list())

        flatList = [item for sublist in active for item in sublist]

        self.df_active = pd.Series(flatList, name = 'active')


    def writingData(self,outfile):

        self.df_total.drop(columns=['recovered', 'active'], inplace = True)
        self.df_total.reset_index(inplace=True, drop=True)

        self.df_total2 = pd.concat([self.df_total, self.df_active, self.df_recovered], axis=1)


        # Data is writen to a csv file in the standard format.
        # column 0: 'date', column 1: 'fips', column 2: 'county', column 3: 'cases', column 4: 'deaths',
        # column 5: 'active', column 6: 'recovered'

        # Each line correspond to each county

        self.df_total2.to_csv(outfile, index = False)

if __name__ == '__main__':

    # Establish the source to read
    source = 'JH'

    # call each of the functions
    data = MineData()

    # provide the url of the GitHub API of the target directory to read in the repository
    data.findingFiles('https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports')
    data.readingData(source)
    data.recoveredCases()
    data.activeCases()

    # provide the name of the output file
    data.writingData('../output/JHopkins/JHraw_epidemiology_NY_std.csv')