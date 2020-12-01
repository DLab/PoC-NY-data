# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:58:35 2020

@author: abarr
"""

import pandas as pd
import numpy as np
import datetime
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
        
        if url.find("group-hosp-by-boro") > -1:
            df = pd.read_csv(url)
            todrop = df.loc[df['group'] == 'Boroughwide']
            df.drop(todrop.index, inplace=True)
            
            df.columns = df.columns.str.lower()
            df.columns = [item.replace('count', 'cnt') for item in df.columns]
            df.columns = [item.replace('bk', 'kg') for item in df.columns]
            df.columns = [item.replace('mn', 'ny') for item in df.columns]
            df.columns = [item.replace('si', 'rd') for item in df.columns]
            
            self.hosp_boro=df
        
        elif url.find("tests.csv") > -1:
            df = pd.read_csv(url)
            df = df.drop(['INCOMPLETE'], axis=1)
            df.columns = df.columns.str.lower()
            df = df.rename(columns = {'total_tests':'cnt_test', 'positive_tests':'cnt_positive_test', 'percent_positive':'per_positive', 'total_tests_7days_avg':'cnt_tests_avg', 'positive_tests_7days_avg':'cnt_positive_tests_avg', 'percent_positive_7days_avg':'per_positive_avg'})
            df['date'] = pd.to_datetime(df['date'].values).strftime('%Y-%m-%d')
            df['fips']=np.zeros((len(df),1))
            df['county']=['New York City']*len(df)
            
            cols = list(df)
            cols.insert(1, cols.pop(cols.index('fips')))
            cols.insert(2, cols.pop(cols.index('county')))
            
            df=df[cols]
            
            fips = utils.counties(source)
            fip_nyc = [fips[fips['county']=='New York City'].fips.values[0]]*len(df)
            
            df['fips']=fip_nyc
            
            self.tests=df
            
        
        else:
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
    
    def CorrectFormatBoro_hosp(self,source): 
        
        self.hosp_boro_cf=pd.DataFrame()
        
        Cnty = ['Bronx','Kings','New York','Queens','Richmond']
        abb = ['bx','kg','ny','qn','rd']
        
        k = 0
        
        for i in range(0,5):
            cf_boro_hosp = pd.DataFrame(columns=['group', 'subgroup', 'fips', 'county', 'hospitalized_cnt', 'hospitalized_rate'])
            
            cf_boro_hosp['group']=self.hosp_boro['group'].copy()
            cf_boro_hosp['subgroup']=self.hosp_boro['subgroup'].copy()
            
            fips = utils.counties(source)
            fip = [fips[fips.county==Cnty[i]]['fips'].values[0]]*len(self.hosp_boro['group'])
            cf_boro_hosp['fips']=fip
            
            cf_boro_hosp['county']=[Cnty[i]]*len(self.hosp_boro['group'])
            
            str_boro=abb[i]
            cf_boro_hosp['hospitalized_cnt'] = self.hosp_boro[str_boro + '_hospitalized_cnt'].copy()
            cf_boro_hosp['hospitalized_rate'] = self.hosp_boro[str_boro + '_hospitalized_rate'].copy()
            
            if k==0:
                self.hosp_boro_cf = cf_boro_hosp.copy()
                
            else:
                self.hosp_boro_cf = pd.concat([self.hosp_boro_cf,cf_boro_hosp], axis=0)
            
            k +=1
    
        self.hosp_boro_cf=self.hosp_boro_cf.reset_index() 
        self.hosp_boro_cf=self.hosp_boro_cf.drop(['index'], axis=1)

        
    def WritingBoro_hosp(self,outfile):
        
        self.hosp_boro_cf.to_csv(outfile, index=False)
        
    def WritingNYC_tests(self,outfile):
        
        self.tests.to_csv(outfile, index=False)
        
        
        
        
    def CorrectFormat(self,source):
        
        cf_nyc = pd.DataFrame(np.zeros((len(self.nyc.date),9)), columns=['date','fips','county','daily_cases','daily_hospitalized','daily_deaths','daily_cases_avg','daily_hospitalized_avg','daily_deaths_avg'])
        
        fips = utils.counties(source)
        fip_nyc = [fips[fips['county']=='New York City'].fips.values[0]]*len(self.nyc.date)
        #pdb.set_trace()
        date_nyc = self.nyc['date'].copy()
        county_name = [fips[fips.fips==fip_nyc[0]]['county'].values[0]]*len(self.nyc.date)
        
        cf_nyc['date'] = date_nyc
        cf_nyc['fips'] = fip_nyc
        cf_nyc['county'] = county_name
        cf_nyc['daily_cases'] = self.nyc['nyc_case_cnt'].copy()
        cf_nyc['daily_hospitalized'] = self.nyc['nyc_hospitalized_cnt'].copy()
        cf_nyc['daily_deaths'] = self.nyc['nyc_death_cnt'].copy()
        cf_nyc['daily_cases_avg'] = self.nyc['nyc_case_cnt_avg'].copy()
        #pdb.set_trace()
        cf_nyc['daily_hospitalized_avg'] = self.nyc['nyc_hosp_cnt_avg'].copy()
        cf_nyc['daily_deaths_avg'] = self.nyc['nyc_death_cnt_avg'].copy()
        
        self.nyc_cf = cf_nyc
        
        self.borougth_cf = pd.DataFrame()
        #pdb.set_trace()
        Cnty = ['Bronx','Kings','New York','Queens','Richmond']
        abb = ['bx','kg','ny','qn','rd']
        
        k = 0
        
        for i in range(0,5):
            cf_boro = pd.DataFrame(np.zeros((len(self.borougth.date),9)),columns=['date','fips','county','daily_cases','daily_hospitalized','daily_deaths','daily_cases_avg','daily_hospitalized_avg','daily_deaths_avg'])
            
            date_boro = self.borougth['date'].copy()
            
            fip_boro = [fips[fips['county']==Cnty[i]].fips.values[0]]*len(self.borougth.date)
            county_name = [fips[fips.fips==fip_boro[0]]['county'].values[0]]*len(self.borougth.date)
            
            cf_boro['date'] = date_boro
            cf_boro['fips'] = fip_boro
            cf_boro['county'] = county_name
            
            str_boro=abb[i]
            #spike_cols =[x for x in self.borougth.columns[self.borougth.columns.str.contains(str_boro)]] 
            cf_boro['daily_cases'] = self.borougth[ str_boro + '_case_cnt'].copy()
            cf_boro['daily_hospitalized'] = self.borougth[str_boro + '_hospitalized_cnt'].copy()
            cf_boro['daily_deaths'] = self.borougth[ str_boro + '_death_cnt'].copy()
            cf_boro['daily_cases_avg'] = self.borougth[ str_boro + '_case_cnt_avg'].copy()
            cf_boro['daily_hospitalized_avg'] = self.borougth[ str_boro + '_hospitalized_cnt_avg'].copy()
            cf_boro['daily_deaths_avg'] = self.borougth[ str_boro + '_death_cnt_avg'].copy()
            #pdb.set_trace()
            
            if k == 0:
                self.borougth_cf = cf_boro.copy()
                
            else:
                self.borougth_cf = pd.concat([self.borougth_cf,cf_boro], axis=0)
            
            k +=1
            #pdb.set_trace()
            
            
        
        
    def writing(self,outfile):
        
        self.nyc_cf.to_csv(outfile[0], index= False)
        
        self.borougth_cf.to_csv(outfile[1], index = False)
        


if __name__== '__main__':
    
    source = 'JH'
    
    data0 = Minedata() 
    data0.File('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/data-by-day.csv') 
    data0.CorrectFormat(source)
    data0.writing(['../output/NYChealth/NYChealthraw_epidemiology_NYC_std.csv','../output/NYChealth/NYChealthraw_epidemiology_BOROUGT_std.csv'])

    ### dataset with previous information. 
    
    data1 = Minedata()
    data1.File('https://raw.githubusercontent.com/nychealth/coronavirus-data/9d4dc17a508b271804ca7ecea2aaca2f77b2493a/trends/data-by-day.csv')
    data1.CorrectFormat(source)
    data1.writing(['../output/NYChealth/PreUpdate_NYChealthraw_epidemiology_NYC_std.csv','../output/NYChealth/PreUpdate_NYChealthraw_epidemiology_BOROUGT_std.csv'])

    data2 = Minedata()
    data2.File('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/group-hosp-by-boro.csv')
    data2.CorrectFormatBoro_hosp(source)
    data2.WritingBoro_hosp('../output/NYChealth/HospBoro_NYChealthraw_epidemiology_BOROUGT_std.csv')
    
    data3 = Minedata()
    data3.File('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/tests.csv')
    data3.WritingNYC_tests('../output/NYChealth/tests_NYChealthraw_epidemiology_NYC_std.csv')









