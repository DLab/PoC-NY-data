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
import pandas as pd

"""
Generic utilities
"""

def counties(source):

    filename = '../input/utilities/population_NY_2019_version' + source + '.csv'
    county = pd.read_csv(filename)
    county.drop(columns=['state', 'population'], inplace=True)

    return county

def hospitalData(df):

    df2 = df[['collection_week','fips_code','hospital_pk',
              'all_adult_hospital_inpatient_beds_7_day_sum',
              'inpatient_beds_used_7_day_sum',
              'total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_sum',
              'total_adult_patients_hospitalized_confirmed_covid_7_day_sum','total_icu_beds_7_day_sum',
              'icu_beds_used_7_day_sum','total_staffed_adult_icu_beds_7_day_sum',
              'staffed_adult_icu_bed_occupancy_7_day_sum',
              'staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_sum',
              'staffed_icu_adult_patients_confirmed_covid_7_day_sum']].copy()

    df2.rename(columns = {'collection_week': 'date', 'fips_code': 'fips',
                          'all_adult_hospital_inpatient_beds_7_day_sum': 'total_adult_inpatient_sum',
                          'inpatient_beds_used_7_day_sum': 'used_inpatient_sum',
                          'total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_sum': 'total_adult_confirmed_and_suspected_covid_sum',
                          'total_adult_patients_hospitalized_confirmed_covid_7_day_sum': 'total_adult_confirmed_covid_sum',
                          'total_icu_beds_7_day_sum': 'total_icu_sum',
                          'icu_beds_used_7_day_sum': 'used_icu_sum',
                          'total_staffed_adult_icu_beds_7_day_sum': 'total_staffed_adult_icu_sum',
                          'staffed_adult_icu_bed_occupancy_7_day_sum': 'used_staffed_adult_icu_sum',
                          'staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_sum': 'staffed_icu_adult_confirmed_and_suspected_covid_sum',
                          'staffed_icu_adult_patients_confirmed_covid_7_day_sum': 'staffed_icu_adult_confirmed_covid_sum'},
               inplace = True)

    return df2