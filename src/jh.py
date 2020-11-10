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

class MineData:

    def findingFiles(self,url):

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

        self.county = utils.counties(source)

        self.df_total = pd.DataFrame()

        k = 0
        i = 0
        for date in self.dates:

            print('Processing ' + date)
            temp = pd.read_csv(self.downURL[i])
            temp.columns = temp.columns.str.replace('/','_')
            temp.columns = temp.columns.str.replace(' ','_')
            temp.columns = temp.columns.str.lower()

            if 'province_state' in temp.columns:
                temp.rename(columns = {'province_state': 'state', 'country_region': 'country'}, inplace = True)

            flag = 0
            flag2 = 0
            if 'admin2' in temp.columns:
                temp.rename(columns = {'admin2': 'county'}, inplace = True)
                #temp['county'].replace({'New York City': 'New York'}, inplace=True)
                flag = 1

                list_county = temp['county'].to_list()
                if 'New York' in list_county:
                    if flag2 == 0: print('NYC segregated: ', date)
                    flag2 = 1

            temp_us = temp.loc[temp['country'] == 'US']
            temp_us_ny = temp_us.loc[temp_us['state'] == 'New York']


            date2 = pd.to_datetime(date).strftime('%Y-%m-%d')

            temp_us_ny['last_update'] = pd.to_datetime(temp_us_ny['last_update'], infer_datetime_format=True)
            temp_us_ny['last_update'] = pd.to_datetime(temp_us_ny['last_update']).dt.strftime('%Y-%m-%d')
            temp_us_ny.reset_index(inplace=True, drop=True)


            if flag == 1:
                df = pd.DataFrame(np.zeros((len(self.county), 4)), columns=['cases','deaths','active','recovered'])
                cases_county = temp_us_ny['confirmed'].copy()
                deaths_county = temp_us_ny['deaths'].copy()
                active_county = temp_us_ny['active'].copy()
                recovered_county = temp_us_ny['recovered'].copy()

                t = [date2]*len(self.county)
                df_date = pd.DataFrame(data={'date': t})

                j = 0
                for row in temp_us_ny['county']:
                    idx = self.county.loc[self.county['county'] == row].index.values
                    if idx.size > 0:
                        #print(row, idx, cases_county[j])
                        df.loc[idx, 'cases'] = cases_county[j]
                        df.loc[idx, 'deaths'] = deaths_county[j]
                        df.loc[idx, 'active'] = active_county[j]
                        df.loc[idx, 'recovered'] = recovered_county[j]
                        if active_county[j] < 0:
                            print('Actives are negative in this county: ', row,' on date: ', date2)

                        j += 1

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

                    print(df)


                aux = pd.concat([df_date, self.county, df.astype(int)], axis=1)

                if k == 0:

                    self.df_total = aux.copy()

                else:
                    self.df_total = pd.concat([self.df_total,aux], axis=0)

                k += 1
            i += 1

    def writingData(self,outfile):

        self.df_total.reset_index(inplace=True, drop=True)
        self.df_total.to_csv(outfile, index = False)

if __name__ == '__main__':

    source = 'JH'

    data = MineData()
    data.findingFiles('https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports')
    data.readingData(source)
    data.writingData('../output/JHopkins/JHraw_epidemiology_NY_std.csv')