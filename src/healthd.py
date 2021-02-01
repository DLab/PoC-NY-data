import pandas as pd
import sys
import numpy as np
import datetime
import re
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
        #self.output = output
        # init stuff
        self.file_name = self.url

        self.date = re.search("\d{8}", self.file_name).group(0)
        print(self.date)
        #self.date = pd.to_datetime(self.date).strftime('%Y-%m-%d')

    def retrieveLastFileData(self):

        #print(response)
        csv_path = self.url
        #csv_path = '~/Datos-MinCiencia/notebooks/dLab/reported_hospital_capacity_admissions_facility_level_weekly_average_timeseries_20210124.csv'

        print('reading file...')
        df = pd.read_csv(csv_path)
        print('file read')
        cnt_data = pd.read_csv('../input/utilities/population_NY_2019_versionJH.csv')

        ny = df.loc[df['state'] == 'NY']
        ny.sort_values('fips_code', inplace=True)
        ny['county'] = ny['fips_code'].copy()

        i = 0
        for row in cnt_data['fips'].index:
            idx = ny.loc[ny['fips_code'] == cnt_data['fips'].iloc[row]].index
            ny.loc[idx, 'county'] = cnt_data.loc[row, 'county']

        ny.sort_values(by='collection_week', inplace=True)

        ny_ss = ny[['collection_week', 'fips_code', 'county', 'hospital_pk', 'is_metro_micro', 'hospital_subtype',
                    'all_adult_hospital_inpatient_beds_7_day_sum', 'inpatient_beds_used_7_day_sum',
                    'total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_sum',
                    'total_adult_patients_hospitalized_confirmed_covid_7_day_sum', 'total_icu_beds_7_day_sum',
                    'icu_beds_used_7_day_sum', 'total_staffed_adult_icu_beds_7_day_sum',
                    'staffed_adult_icu_bed_occupancy_7_day_sum',
                    'staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_sum',
                    'staffed_icu_adult_patients_confirmed_covid_7_day_sum']].copy()

        ny_ss.rename(columns={'collection_week': 'date', 'is_metro_micro': 'metro_micro', 'fips_code': 'fips',
                              'all_adult_hospital_inpatient_beds_7_day_sum': 'total_adult_inpatient_sum',
                              'inpatient_beds_used_7_day_sum': 'used_inpatient_sum',
                              'total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_sum': 'total_adult_confirmed_and_suspected_covid_sum',
                              'total_adult_patients_hospitalized_confirmed_covid_7_day_sum': 'total_adult_confirmed_covid_sum',
                              'total_icu_beds_7_day_sum': 'total_icu_sum', 'icu_beds_used_7_day_sum': 'used_icu_sum',
                              'total_staffed_adult_icu_beds_7_day_sum': 'total_staffed_adult_icu_sum',
                              'staffed_adult_icu_bed_occupancy_7_day_sum': 'used_staffed_adult_icu_sum',
                              'staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_sum': 'staffed_icu_adult_confirmed_and_suspected_covid_sum',
                              'staffed_icu_adult_patients_confirmed_covid_7_day_sum': 'staffed_icu_adult_confirmed_covid_sum'},
                     inplace=True)


        #nHosp = [len(list(group)) for key, group in groupby(df['collection_week'])]
        #ny = df.loc[df['state'] == 'NY']
        #print(len(ny['fips_code'].unique()))
        #print(len(ny['hospital_pk'].unique()))
        #print(ny['total_beds_7_day_avg'].head(), ny['total_beds_7_day_sum'].div(7).head())
        #print(nHosp)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_url = sys.argv[1]
        hosp_data = hospitalData(my_url, '../output/HealthGov/HealthGovraw_hospital_NY_std.csv')
        hosp_data.retrieveLastFileData()
