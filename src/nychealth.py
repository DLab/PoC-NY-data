# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:58:35 2020

@author: abarr
"""

import pandas as pd
import requests
import pdb

## covid-like-illness-csv
## data-by-day-csv
## tests.csv
## Opendata: COVID-19 Outcomes by Testing Cohorts: Cases, Hospitalizations, and Deaths
## Opendata: COVID-19 Daily Counts of Cases, Hospitalizations, and Deaths

class Minedata:
    
    def File(self,url):
        df = pd.read_csv(url)
        #change of format date
        df['date_of_interest'] = pd.to_datetime(df['date_of_interest']).dt.strftime('%Y-%m-%d') 
        df = df.drop(['INCOMPLETE','DEATH_COUNT_PROBABLE'], axis=1)
        
        df.columns = df.columns.str.lower()
        df.columns = [item.replace('count', 'cnt') for item in df.columns]
        df.columns = [item.replace('_7day_', '_') for item in df.columns]
        df.columns = [item.replace('bk', 'kg') for item in df.columns]
        df.columns = [item.replace('mn', 'ny') for item in df.columns]
        df.columns = [item.replace('si', 'rd') for item in df.columns]
        
        df=df.rename(columns = {'date_of_interest': 'date', 'case_cnt':'nyc_case_cnt', 'hospitalized_cnt':'nyc_hospitalized_cnt', 'death_cnt':'nyc_death_cnt', 'case_cnt_avg':'nyc_case_cnt_avg', 'hosp_cnt_avg':'nyc_hosp_cnt_avg', 'death_cnt_avg':'nyc_death_cnt_avg'})
        
        self.nyc = df[['date','nyc_case_cnt','nyc_hospitalized_cnt','nyc_death_cnt','nyc_case_cnt_avg','nyc_hosp_cnt_avg','nyc_death_cnt_avg']]
        
        self.borougth = df.drop(['nyc_case_cnt','nyc_hospitalized_cnt','nyc_death_cnt','nyc_case_cnt_avg','nyc_hosp_cnt_avg','nyc_death_cnt_avg'], axis=1)
        
    def writing(self,outfile1,outfile2):
        
        self.nyc.to_csv(outfile1, index= False)
        
        self.borougth.to_csv(outfile2, index = False)
        
        #pdb.set_trace()
        


if __name__== '__main__':
    
    data = Minedata() 
    data.File('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/data-by-day.csv') 
    data.writing('NYChealthraw_epidemiology_NYC_std.csv','NYChealthraw_epidemiology_BOROUGTH_std.csv')

















