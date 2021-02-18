import pandas as pd
import sys
import numpy as np
import utils
import re

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

    def __init__(self, url):

        self.url = url
        self.file_name = self.url

        date = re.search("\d{8}", self.file_name).group(0)
        print(date)

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
                print('There is a new Hospital in the state. Please complte the file ../input/utilities/list_hospital_NY.csv')

        self.ny_hosp['fips'] = self.ny_hosp['fips'].astype(int)

        self.ny_hosp.reset_index(inplace=True)
        self.ny_hosp.drop(columns={'index'}, axis=1, inplace=True)
        temp = list(self.ny_hosp.columns)
        cols = temp[0:2] + [temp[-1]] + temp[2:-1]
        self.ny_hosp = self.ny_hosp[cols]

    def groupCounty(self):

        ny_hospital = utils.dataDrop(self.ny_hosp)
        print(ny_hospital)

        identifiers = ['date', 'fips', 'county', 'hospital_pk']
        variables = [x for x in ny_hospital.columns if x not in identifiers]

        self.listDates = ny_hospital['date'].unique()

        self.lim = [1.0, 4.0]

        for n in range(2):
            self.ny_hosp2 = ny_hospital.replace(to_replace=-999999.0, value=self.lim[n],
                                                 inplace=False, method=None)
            hosp_county_sum = pd.DataFrame()

            i = 0
            for row in self.listDates:
                aux1 = self.ny_hosp2.loc[self.ny_hosp2['date'] == row].copy()
                for code in self.cnt_data['fips']:
                    temp = aux1[variables].loc[aux1['fips'] == code].multiply(7.0)
                    idx1 = temp.sum(axis=0)
                    idx1 = idx1.div(7).round(1)
                    idx3 = aux1[identifiers].loc[aux1['fips'] == code].copy()
                    if idx3.size == 0:
                        cnt = self.cnt_data['county'].loc[self.cnt_data['fips'] == code].item()
                        date = self.ny_hosp2['date'].loc[self.ny_hosp2['date'] == row].copy()
                        idx3[identifiers] = [date, code, cnt, 'NA']

                    idx3['boundary'] = self.lim[n]

                    if idx1.size > 0:
                        aux2 = pd.concat([idx3.iloc[0], idx1], axis=0)
                    else:
                        aux2 = pd.DataFrame(np.zeros(1, len(variables)))
                        aux2 = pd.concat([idx3, aux2], axis=0)

                    aux4 = aux2.to_frame().T
                    if i == 0:
                        hosp_county_sum = aux4
                        i += 1
                    else:
                        hosp_county_sum = pd.concat([hosp_county_sum,aux4], axis=0)

            if n == 0:
                self.county_sum = hosp_county_sum
            else:
                self.county_sum = pd.concat([self.county_sum, hosp_county_sum], axis=0)

        self.county_sum.drop(columns=['hospital_pk'], inplace=True)
        self.county_sum.reset_index(drop=True, inplace=True)

    def groupState(self):

        identifiers = ['date', 'fips', 'county', 'boundary']
        variables = [x for x in self.county_sum.columns if x not in identifiers]

        hosp_state_sum = pd.DataFrame()

        j = 0
        for row in self.listDates:
            i = 0
            for l in self.lim:
                aux1 = self.county_sum.loc[self.county_sum['boundary'] == l]
                aux2 = aux1[variables].loc[aux1['date'] == row].sum(axis=0)
                idx1 = aux1[['date','boundary']].loc[aux1['date'] == row].copy()

                idx1.reset_index(drop=True, inplace=True)
                aux4 = pd.concat([idx1.iloc[0],aux2], axis=0)

                aux4 = aux4.to_frame().T
                aux4.reset_index(drop=True, inplace=True)

                if i == 0:
                    hosp_state_sum = aux4
                    i += 1
                else:
                    hosp_state_sum = pd.concat([hosp_state_sum, aux4], axis=0)

            if j == 0:
                self.state_sum = hosp_state_sum
                j += 1
            else:
                self.state_sum = pd.concat([self.state_sum, hosp_state_sum], axis=0)

        self.state_sum.sort_values(by=['boundary'], inplace=True)

    def writeData(self):

        label = ['Hospital', 'County', 'State']

        self.ny_hosp.to_csv('../output/Hospital-Data/raw_hospitalData_' + label[0] + '_NY.csv', index=False)

        self.county_sum.to_csv('../output/Hospital-Data/hospitalData_' + label[1] + '_NY.csv', index=False)

        self.state_sum.to_csv('../output/Hospital-Data/hospitalData_' + label[2] + '_NY.csv', index=False)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_url = sys.argv[1]
        hosp_data = hospitalData(my_url)
        hosp_data.retrieveLastFileData()
        hosp_data.groupCounty()
        hosp_data.groupState()
        hosp_data.writeData()


