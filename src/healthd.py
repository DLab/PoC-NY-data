import pandas as pd
import sys
import numpy as np
import utils
import re
from itertools import groupby

'''
MIT License

Copyright (c) 2021 Faviola Molina - dLab - Fundación Ciencia y Vida

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

class hospitalData:
    def __init__(self, url, output):

        # store used variables
        self.url = url
        # init stuff
        self.file_name = self.url

        self.date = re.search("\d{8}", self.file_name).group(0)
        print(self.date)

    def retrieveLastFileData(self):

        csv_path = self.url

        print('reading file...')
        df = pd.read_csv(csv_path)
        print('file read')

        self.cnt_data = pd.read_csv('../input/utilities/population_NY_2019_versionJH.csv')
        self.hosp_list = pd.read_csv('../input/utilities/list_hospital_NY.csv')

        df2 = utils.hospitalData(df)

        ny = df2.loc[df['state'] == 'NY']
        ny.sort_values('fips', inplace=True)
        ny['county'] = ny['fips'].copy()

        for row in self.cnt_data['fips'].index:

            idx = ny.loc[ny['fips'] == self.cnt_data['fips'].iloc[row]].index
            ny.loc[idx, 'county'] = self.cnt_data.loc[row, 'county']

        self.ny_hosp = ny.sort_values(by=['date', 'fips'])

        for row in self.hosp_list['fips']:
            idx = ny.loc[ny['fips'] == row].index

            if len(idx) == 0:
                print('There is a new Hospital in the state. Please complete the file ../input/utilities/list_hospital_NY.csv')

        self.ny_hosp['fips'] = self.ny_hosp['fips'].astype(int)

    def groupCounty(self):

        identifiers = ['date', 'fips', 'county', 'hospital_pk']
        variables = [x for x in self.ny_hosp.columns if x not in identifiers]

        self.listDates = self.ny_hosp['date'].unique()

        lim = [0.0, 4.0]

        for n in range(2):
            self.ny_hosp2 = self.ny_hosp.replace(to_replace=-999999.0, value=lim[n],
                                                 inplace=False, method=None)
            if n == 0:
                tag = 'Linf'
            elif n == 1:
                tag = 'Lsup'

            self.hosp_county_sum = pd.DataFrame()
            hosp_county_avg = pd.DataFrame()

            i = 0
            for row in self.listDates:
                aux1 = self.ny_hosp2.loc[self.ny_hosp2['date'] == row].copy()
                for code in self.cnt_data['fips']:
                    idx1 = aux1[variables].loc[aux1['fips'] == code].sum(axis=0)
                    idx2 = idx1.div(7).round(2)
                    idx3 = aux1[identifiers].loc[aux1['fips'] == code].copy()
                    if idx3.size == 0:
                        cnt = self.cnt_data['county'].loc[self.cnt_data['fips'] == code].item()
                        date = self.ny_hosp2['date'].loc[self.ny_hosp2['date'] == row].copy()
                        idx3[identifiers] = [date, code, cnt, 'NA']
                    if idx1.size > 0:
                        aux2 = pd.concat([idx3.iloc[0], idx1], axis=0)
                        aux3 = pd.concat([idx3.iloc[0], idx2], axis=0)
                    else:
                        aux2 = pd.DataFrame(np.zeros(1, len(variables)))
                        aux2 = pd.concat([idx3, aux2], axis=0)

                        aux3 = pd.DataFrame(np.zeros(1, len(variables)))
                        aux3 = pd.concat([idx3, aux3], axis=0)

                    aux4 = aux2.to_frame().T
                    aux5 = aux3.to_frame().T
                    if i == 0:
                        self.hosp_county_sum = aux4
                        hosp_county_avg = aux5
                        i += 1
                    else:
                        self.hosp_county_sum = pd.concat([self.hosp_county_sum,aux4], axis=0)
                        hosp_county_avg = pd.concat([hosp_county_avg,aux5], axis=0)

            self.hosp_county_sum.drop(columns=['hospital_pk'], inplace=True)
            hosp_county_avg.drop(columns=['hospital_pk'], inplace=True)
            self.hosp_county_sum.reset_index(drop=True, inplace=True)
            hosp_county_avg.reset_index(drop=True, inplace=True)

            self.hosp_county_sum.to_csv('../output/Hospital-Data/hospital_capacity_countyNY_sum_' + tag + '.csv', index=False)
            hosp_county_avg.to_csv('../output/Hospital-Data/hospital_capacity_countyNY_avg_' + tag + '.csv', index=False)

    def groupState(self):

        identifiers = ['date', 'fips', 'county']
        variables = [x for x in self.hosp_county_sum.columns if x not in identifiers]

        self.hosp_state_sum = pd.DataFrame()

        i = 0
        for row in self.listDates:
            aux1 = self.hosp_county_sum[variables].loc[self.hosp_county_sum['date'] == row].sum(axis=0)
            aux2 = aux1.div(7).round(2)

            aux3 = aux1.to_frame().T
            aux3.reset_index(drop=True, inplace=True)

            aux4 = aux2.to_frame().T
            aux4.reset_index(drop=True, inplace=True)

            if i == 0:
                self.hosp_state_sum = aux3
                self.hosp_state_avg = aux4
                i += 1
            else:
                self.hosp_state_sum = pd.concat([self.hosp_state_sum, aux3], axis=0)
                self.hosp_state_avg = pd.concat([self.hosp_state_avg, aux4], axis=0)

        dates = pd.Series(self.listDates, name='date')
        print(dates.shape, self.hosp_state_sum.shape)
        self.hosp_state_sum.reset_index(drop=True, inplace=True)
        self.hosp_state_sum = pd.concat([dates, self.hosp_state_sum], axis=1)

        self.hosp_state_avg.reset_index(drop=True, inplace=True)
        self.hosp_state_avg = pd.concat([dates, self.hosp_state_avg], axis=1)

        self.hosp_state_sum.to_csv('../output/Hospital-Data/hospital_capacity_NY_sum_Lsup.csv', index=False)
        self.hosp_state_avg.to_csv('../output/Hospital-Data/hospital_capacity_NY_avg_Lsup.csv', index=False)

    def writeData(self, label):

        if label == 'Hospital':
            self.ny_hosp.reset_index(inplace=True)
            self.ny_hosp.drop(columns={'index'}, axis=1, inplace=True)

            self.ny_hosp.to_csv('../output/Hospital-Data/raw_hospitalData_' + label + '_NY_std.csv', index=False)

        print('ALLES CLAAAARRRRRR')


if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_url = sys.argv[1]
        hosp_data = hospitalData(my_url, '../output/HealthGov/HealthGovraw_hospital_NY_std.csv')
        hosp_data.retrieveLastFileData()
        hosp_data.groupCounty()
        hosp_data.groupState()
        hosp_data.writeData('Hospital')
