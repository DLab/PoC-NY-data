# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:58:35 2020

@author: abarr
"""

import pandas as pd
import numpy as np
import requests
import utils
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
        
        #pdb.set_trace()
        
    def CorrectFormat(self,source):
        cf_nyc = pd.DataFrame(np.zeros((len(self.nyc.date),9)), columns=['date','fips','county','case','hospitalized','death','case_avg','hospitalized_avg','death_avg'])
        
        fips = utils.counties(source)
        fip_nyc = [fips[fips['county']=='New York City'].fips.values[0]]*len(self.nyc.date)
        #pdb.set_trace()
        date_nyc = self.nyc['date'].copy()
        county_name = [fips[fips.fips==fip_nyc[0]]['county'].values[0]]*len(self.nyc.date)
        
        cf_nyc['date'] = date_nyc
        cf_nyc['fips'] = fip_nyc
        cf_nyc['county'] = county_name
        cf_nyc['case'] = self.nyc['nyc_case_cnt'].copy()
        cf_nyc['hospitalized'] = self.nyc['nyc_hospitalized_cnt'].copy()
        cf_nyc['death'] = self.nyc['nyc_death_cnt'].copy()
        cf_nyc['case_avg'] = self.nyc['nyc_case_cnt_avg'].copy()
        cf_nyc['hospitalized_avg'] = self.nyc['nyc_hosp_cnt_avg'].copy()
        cf_nyc['death_avg'] = self.nyc['nyc_death_cnt_avg'].copy()
        
        self.nyc_cf = cf_nyc
        
        self.borougth_cf = pd.DataFrame()
        #pdb.set_trace()
        Cnty = ['Bronx','Kings','New York','Queens','Richmond']
        abb = ['bx','kg','ny','qn','rd']
        
        k = 0
        
        for i in range(0,5):
            cf_boro = pd.DataFrame(np.zeros((len(self.borougth.date),9)),columns=['date','fips','county','case','hospitalized','death','case_avg','hospitalized_avg','death_avg'])
            
            date_boro = self.borougth['date'].copy()
            
            fip_boro = [fips[fips['county']==Cnty[i]].fips.values[0]]*len(self.borougth.date)
            county_name = [fips[fips.fips==fip_boro[0]]['county'].values[0]]*len(self.borougth.date)
            
            cf_boro['date'] = date_boro
            cf_boro['fips'] = fip_boro
            cf_boro['county'] = county_name
            
            str_boro=abb[i]
            #spike_cols =[x for x in self.borougth.columns[self.borougth.columns.str.contains(str_boro)]] 
            cf_boro['case'] = self.borougth[ str_boro + '_case_cnt'].copy()
            cf_boro['hospitalized'] = self.borougth[str_boro + '_hospitalized_cnt'].copy()
            cf_boro['death'] = self.borougth[ str_boro + '_death_cnt'].copy()
            cf_boro['case_avg'] = self.borougth[ str_boro + '_case_cnt_avg'].copy()
            cf_boro['hospitalized_avg'] = self.borougth[ str_boro + '_hospitalized_cnt_avg'].copy()
            cf_boro['death_avg'] = self.borougth[ str_boro + '_death_cnt_avg'].copy()
            
            
            if k == 0:
                self.borougth_cf = cf_boro.copy()
                
            else:
                self.borougth_cf = pd.concat([self.borougth_cf,cf_boro], axis=0)
            
            k +=1
            #pdb.set_trace()
            
            
        
        
    def writing(self,outfile1,outfile2):
        
        self.nyc_cf.to_csv(outfile1, index= False)
        
        self.borougth_cf.to_csv(outfile2, index = False)
        


if __name__== '__main__':
    
    source = 'JH'
    
    data = Minedata() 
    data.File('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/data-by-day.csv') 
    data.CorrectFormat(source)
    data.writing('NYChealthraw_epidemiology_NYC_std.csv','NYChealthraw_epidemiology_BOROUGT_std.csv')

















