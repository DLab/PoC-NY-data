# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:26:29 2020

@author: abarr
"""
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt 
import datetime 
from matplotlib.dates import MonthLocator, DateFormatter
import pdb


class datatest:
    
    def makefile(self,url):
        
        JH = pd.read_csv(url[0])
        nyc_hboro = pd.read_csv(url[1])
        
        ### we create a table of data disaggregated by borough from nychealth data
        self.counties=np.unique(nyc_hboro['county'].values)
        nychealth_by_boro=nyc_hboro[['date', 'fips', 'county', 'daily_cases']].copy()
        
        for i in range(0,len(self.counties)):
            one_borough= nychealth_by_boro[nychealth_by_boro.county==self.counties[i]].copy()
            inds=nychealth_by_boro.loc[nychealth_by_boro.county==self.counties[i]].copy()
            nychealth_by_boro.loc[inds.index, 'cases']=one_borough['daily_cases'].cumsum()
            
        nychealth_by_boro=nychealth_by_boro.drop(['daily_cases'], axis=1)
        nychealth_by_boro.index=nychealth_by_boro['date']
        nychealth_by_boro=nychealth_by_boro.drop(['date'], axis=1)
        
        print('nyc by borough from nychealth data')
        self.nychealth_by_boro=nychealth_by_boro
        
        nycJH_by_boro=pd.DataFrame()
        k = 0
        for i in range(0,len(self.counties)):
            boro = JH[JH.county==self.counties[i]][['date','fips','county','cases']]
            if k==0:
                nycJH_by_boro=boro
            else:
                nycJH_by_boro=pd.concat([nycJH_by_boro,boro], axis=0)
            k +=1
            
        
        nycJH_by_boro.index=nycJH_by_boro['date']
        nycJH_by_boro=nycJH_by_boro.drop(['date'], axis=1)
        
        print('nyc by borough from JH data')
        self.nycJH_by_boro=nycJH_by_boro
        
            
    def makehybridata(self):
        
        hybrid_data=pd.DataFrame()
        
        k=0
        for i in range(0,len(self.counties)):
            jh_date=self.nycJH_by_boro[(self.nycJH_by_boro.county==self.counties[i]) & (self.nycJH_by_boro.cases == 0)].index[-1]
            day=datetime.datetime(pd.to_datetime(jh_date).year, pd.to_datetime(jh_date).month, pd.to_datetime(jh_date).day+1).strftime('%Y-%m-%d')
            nychealthboro = self.nychealth_by_boro[self.nychealth_by_boro.county==self.counties[i]].loc[self.nychealth_by_boro.index[0]:jh_date]
            
            nycjhboro = self.nycJH_by_boro[self.nycJH_by_boro.county==self.counties[i]].loc[day:]
            hybrid = pd.concat([nychealthboro,nycjhboro], axis=0)
            
            if k==0:
                hybrid_data=hybrid.copy()
            else:
                hybrid_data=pd.concat([hybrid_data, hybrid], axis=0)
                
            k = k+1
            
            self.hybrid_data=hybrid_data
            
    
    def graph(self):
        sns.set_theme(style="whitegrid")
            
        for i in range(0,len(self.counties)):
            nychealthboro = self.nychealth_by_boro[self.nychealth_by_boro.county==self.counties[i]]['cases']
            nycjhboro = self.nycJH_by_boro[self.nycJH_by_boro.county==self.counties[i]]['cases']
                
            fig = plt.figure(figsize=[14, 4])
            ax = fig.add_subplot(111)
            sns.lineplot(data=nychealthboro, palette="tab10" ,linewidth=4, 
                         label='nychealth_' + self.counties[i])
            sns.lineplot(data=nycjhboro, palette="tab10", linewidth=4, 
                         label='jh_' + self.counties[i])
            ax.xaxis.set_major_locator(MonthLocator())
            plt.title('cases')
            plt.legend()
            plt.show()
            
        dataset_hybrid=pd.DataFrame(index=np.unique(self.hybrid_data.index), columns=self.counties)
        for i in range(0,len(self.counties)):
            dataset_hybrid[self.counties[i]]=self.hybrid_data[self.hybrid_data.county==self.counties[i]]['cases'].values
            
            
        fig = plt.figure(figsize=(20,8))
        ax = fig.add_subplot(111)
        sns.lineplot(data=dataset_hybrid, linewidth=4)
        ax.xaxis.set_major_locator(MonthLocator())
        plt.title("Hybrid data")
        plt.show()
        
    def comparison(self):
        ### JH (hybrid)/nychealth
        
        dataset_hybrid=pd.DataFrame(index=np.unique(self.hybrid_data.index), columns=self.counties)
        for i in range(0,len(self.counties)):
            dataset_hybrid[self.counties[i]]=self.hybrid_data[self.hybrid_data.county==self.counties[i]]['cases'].values
        
        dataset_health=pd.DataFrame(index=np.unique(self.hybrid_data.index), columns=self.counties) 
        comparison=pd.DataFrame(index=np.unique(self.hybrid_data.index), columns=self.counties) 
        for i in range(0,5):
            dataset_health[self.counties[i]]= self.nychealth_by_boro[self.nychealth_by_boro.county==self.counties[i]].loc['2020-02-29':'2020-11-19',
                                                                                              'cases'].values
            comparison[self.counties[i]] = dataset_hybrid[self.counties[i]]/dataset_health[self.counties[i]]
            comparison[self.counties[i]] = comparison[self.counties[i]].fillna(1)
  

        sns.set_theme(style="whitegrid")
        fig = plt.figure(figsize=(20, 8))
        ax = fig.add_subplot(111)
        sns.lineplot(data=comparison, linewidth=4)
        ax.xaxis.set_major_locator(MonthLocator())
        #ax.xaxis.set_major_formatter(DateFormatter('%b %d'))
        plt.title("Hybrid data")
        plt.show()
        
        #pdb.set_trace()
        
    




PATHJH = 'C:/Users/abarr/Documents/GitHub/PoC-NY-data/output/JHopkins/'
PATHNYC = 'C:/Users/abarr/Documents/GitHub/PoC-NY-data/output/NYChealth/'

hybrid=datatest()

hybrid.makefile([PATHJH + 'JHraw_epidemiology_NY_std.csv', PATHNYC + 'NYChealthraw_epidemiology_BOROUGT_std.csv'])
hybrid.makehybridata()
hybrid.graph()
hybrid.comparison()
## JH , nyc_hboro

