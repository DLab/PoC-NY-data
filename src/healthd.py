import pandas as pd
#import sys
import requests
import numpy as np
import utils
from sodapy import Socrata
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

    def __init__(self):

        client = Socrata("healthdata.gov", None)

        self.results = client.get("anag-cw7u", limit=170000)


    def retrieveLastFileData(self):


        print('reading file...')
        df = pd.DataFrame.from_records(self.results)
        print('file read')

        self.cnt_data = pd.read_csv('../input/utilities/population_NY_2019_versionJH.csv')
        self.hosp_list = pd.read_csv('../input/utilities/list_hospital_NY.csv')

        df2 = utils.hospitalData(df)

        temp_ny = df2.loc[df['state'] == 'NY'].copy()
        temp_ny.sort_values('fips', inplace=True)
        temp_ny['county'] = temp_ny['fips'].copy()

        temp_ny['fips'] = temp_ny['fips'].astype(np.int64)
        temp_ny['hospital_pk'] = temp_ny['hospital_pk'].astype(np.int64)

        temp_ny['date'] = pd.to_datetime(temp_ny['date'], infer_datetime_format=True)
        temp_ny['date'] = pd.to_datetime(temp_ny['date']).dt.strftime('%Y-%m-%d')

        temp_ny.reset_index(drop = True, inplace = True)

        i = 0
        for row in self.cnt_data['fips']:

            idx = temp_ny['fips'].loc[temp_ny['fips'] == row].index

            temp_ny.loc[idx, 'county'] = self.cnt_data.loc[i, 'county']

            i += 1

        ny_h = temp_ny.sort_values(by=['date', 'fips'])

        for row in self.hosp_list['fips']:
            idx = temp_ny.loc[temp_ny['fips'] == row].index

            if len(idx) == 0:
                print('There is a new Hospital in the state. Please complte the file ../input/utilities/list_hospital_NY.csv')

        ny_h['fips'] = ny_h['fips'].astype(int)

        ny_h.reset_index(drop=True,inplace=True)
        temp = list(ny_h.columns)
        cols = temp[0:2] + [temp[-1]] + temp[2:-1]
        ny_h = ny_h[cols]

        file1 = pd.read_csv('../output/Hospital-Data/raw_hospitalData_Hospital_NY.csv')
        temp_hosp = pd.concat([file1,ny_h], axis=0)
        temp_hosp.sort_values(by=['date','fips','hospital_pk'], inplace=True)

        identifiers = ['date', 'fips', 'county', 'hospital_pk']
        variables = [x for x in temp_hosp.columns if x not in identifiers]
        self.ny_hosp = temp_hosp.copy()
        self.ny_hosp[variables] = temp_hosp[variables].astype(float)

        self.ny_hosp.drop_duplicates(subset=['date','hospital_pk'], inplace=True)
        self.ny_hosp.sort_values(by=['date','fips','hospital_pk'], inplace=True)
        #print(self.ny_hosp.head())
        #self.ny_hosp = ny_h.copy()
        #self.ny_hosp[variables] = self.ny_hosp[variables].astype(float)


    def groupCounty(self):

        ny_hospital = utils.dataDrop(self.ny_hosp)

        identifiers = ['date', 'fips', 'county', 'hospital_pk']
        variables = [x for x in ny_hospital.columns if x not in identifiers]

        self.listDates = ny_hospital['date'].unique()

        self.lim = [1.0, 4.0]

        for n in range(2):
            self.ny_hosp2 = ny_hospital.replace(to_replace='-999999.0', value=self.lim[n],
                                                 inplace=False, method=None)
            hosp_county_sum = pd.DataFrame()

            i = 0
            for row in self.listDates:
                aux1 = self.ny_hosp2.loc[self.ny_hosp2['date'] == row].copy()
                for code in self.cnt_data['fips']:
                    temp = aux1[variables].loc[aux1['fips'] == code].copy()
                    idx1 = temp.astype(float).sum(axis=0)
                    idx1 = idx1.round(2)
                    idx3 = aux1[identifiers].loc[aux1['fips'] == code].copy()
                    if idx3.size == 0:
                        aux6 = self.cnt_data['county'].loc[self.cnt_data['fips'] == code].copy()
                        cnt = aux6.item()
                        date = self.ny_hosp2['date'].loc[self.ny_hosp2['date'] == row].copy()
                        day = date.unique().item()
                        lista = pd.DataFrame([day, code, cnt, 'NA']).T
                        idx3[identifiers] = lista


                    idx3['boundary'] = self.lim[n]
                    idx3.reset_index(drop=True,inplace=True)

                    if idx1.size > 0:
                        idx1_t = idx1.to_frame().T
                        idaux = idx3.loc[0:0,:]
                        aux2 = pd.concat([idaux, idx1_t], axis=1)
                    else:
                        s = np.zeros((len(idx3),len(variables)), dtype='object')
                        aux2 = pd.DataFrame(s, columns = variables)
                        idx3.reset_index(drop=True,inplace=True)
                        aux2 = pd.concat([idx3, aux2], axis=1)

                    if i == 0:
                        hosp_county_sum = aux2.copy()
                        i += 1
                    else:
                        hosp_county_sum = pd.concat([hosp_county_sum,aux2.copy()], axis=0)

            if n == 0:
                self.county_sum = hosp_county_sum.copy()
            else:
                self.county_sum = pd.concat([self.county_sum, hosp_county_sum.copy()], axis=0)

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
                aux2 = aux2.round(2)
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

    #if len(sys.argv) == 2:
    #    my_url = sys.argv[1]

    hosp_data = hospitalData()
    hosp_data.retrieveLastFileData()
    hosp_data.groupCounty()
    hosp_data.groupState()
    hosp_data.writeData()


