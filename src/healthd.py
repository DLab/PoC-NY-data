import pandas as pd
import sys
import numpy as np
import utils
import re
import math
import requests
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

        cnt_data = pd.read_csv('../input/utilities/population_NY_2019_versionJH.csv')
        hosp_list = pd.read_csv('../input/utilities/list_hospital_NY.csv')

        df2 = utils.hospitalData(df)

        ny = df2.loc[df['state'] == 'NY']
        ny.sort_values('fips', inplace=True)
        ny['county'] = ny['fips'].copy()

        for row in cnt_data['fips'].index:

            idx = ny.loc[ny['fips'] == cnt_data['fips'].iloc[row]].index
            ny.loc[idx, 'county'] = cnt_data.loc[row, 'county']

        self.ny_hosp = ny.sort_values(by='date')

        for row in hosp_list['fips']:
            idx = ny.loc[ny['fips'] == row].index

            if len(idx) == 0:
                print('There is a new Hospital in the state. Please complete the file ../input/utilities/list_hospital_NY.csv')



#    def groupCounty(self):

#    def groupState(self):

    def writeData(self, label):

        if label == 'Hospital':
            self.ny_hosp.reset_index(inplace = True)
            self.ny_hosp.drop(columns = {'index'}, axis = 1,inplace =  True)

            #self.ny_hosp.to_csv('../output/raw_hopitalData_' + label + '_NY_std.csv', float_format = '%.f', index = False)
            self.ny_hosp.to_csv('../output/raw_hopitalData_' + label + '_NY_std.csv', index = False)


        print('ALLES CLAAAARRRRRR')


if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_url = sys.argv[1]
        hosp_data = hospitalData(my_url, '../output/HealthGov/HealthGovraw_hospital_NY_std.csv')
        hosp_data.retrieveLastFileData()
        hosp_data.writeData('Hospital')
