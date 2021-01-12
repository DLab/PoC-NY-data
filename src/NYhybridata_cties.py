# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:46:16 2021

@author: abarr
"""
import pdb
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
from numpy import median
from matplotlib import pyplot as plt 
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.pipeline import make_pipeline
from matplotlib.dates import MonthLocator, DateFormatter

from scipy.interpolate import CubicSpline


class DataNY:
    
    def MakeFiles(self,url):
        print('Loading Hybrid data of the New York...')
        JH = pd.read_csv(url[0])
        nyc_hboro = pd.read_csv(url[1])
        nyc_h = pd.read_csv(url[2])
        
        
        self.cties = np.unique(JH['county'].values)
        self.cties_nyc = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond', 'New York City']
        
        # Step 1: Make cumulative data of cases and death from nychealth
        # Explication : nyc_hboro_cum includes three new columns with cumulative 
        #               confirmed cases, cumulative deaths and cumulative hospitalized to each borough of nyc
        #               It starts from 2020-03-22. 
        nyc_hboro_hosp_deaths = nyc_hboro[['date', 'fips', 'county', 'daily_cases', 'daily_hospitalized', 'daily_deaths']]
        
        nyc_hboro_cum = pd.DataFrame()
        k = 0
        grupos_cnty = nyc_hboro_hosp_deaths.groupby('county')
        for name, data in grupos_cnty:
            data['cases'] = data['daily_cases'].cumsum()
            data['hospitalized'] = data['daily_hospitalized'].cumsum()
            data['deaths'] = data['daily_deaths'].cumsum()
            if k==0:
                nyc_hboro_cum = data
            else:
                nyc_hboro_cum = pd.concat([nyc_hboro_cum, data], axis=0)
            k=k+1
            
        #### nyc_hboro_cum file concatenates information about the five borough of the nyc and nyc total    
        nyc_h['cases'] = nyc_h['daily_cases'].cumsum()
        nyc_h['hospitalized'] = nyc_h['daily_hospitalized'].cumsum()
        nyc_h['deaths'] = nyc_h['daily_deaths'].cumsum()
        nyc_hboro_cum = pd.concat([nyc_hboro_cum,nyc_h[['date','fips','county','daily_cases','daily_hospitalized',
                                                        'daily_deaths','cases','hospitalized','deaths']]], axis=0)
        # Step 2: Reorganize databases ans unify by dates. jh and nyt. 
        # Explication: The organizing process consists of sorting 
        #              the databases by counties and deleting the data before 2020-03-22.
        # NOTE: The JH database starts the day 2020-03-22.
        
    
        #NYT_rogze = pd.DataFrame()
        #NYT_Fboro = pd.DataFrame()
        
        cnty = np.unique(JH['county'].values)
        cnty_nyc = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond', 'New York City']
        
        JH_rogze = pd.DataFrame()
        JH_Fboro = pd.DataFrame()
        
        k = 0
        for i in range(0,len(cnty)):
            onecnty = JH[JH.county==cnty[i]]
            if k==0:
                JH_rogze = onecnty.copy()
            else:
                JH_rogze = pd.concat([JH_rogze,onecnty],axis=0)
                
            k=k+1
            
        for i in range(0,len(cnty_nyc)):
            onecnty_nyc = JH[JH.county==cnty_nyc[i]]
            if k==0:
                JH_Fboro = onecnty_nyc.copy()
            else:
                JH_Fboro = pd.concat([JH_Fboro,onecnty_nyc],axis=0)
            k = k+1
        
            
        JH_Fboro.index=JH_Fboro['date']
        JH_Fboro = JH_Fboro.drop(['date'], axis=1)
        
        nyc_hboro_cum.index = nyc_hboro_cum['date']
        nyc_hboro_cum = nyc_hboro_cum.drop(['date'], axis=1)
        
        self.JH_rogze = JH_rogze
        self.JH_Fboro = JH_Fboro
        self.nyc_hboro_cum = nyc_hboro_cum
        
        
    
    def HybridData(self):
        ## Step 3: HYBRID DATA: joining data JH and NYC-health for the five boroughs of NYC then 
        #         we merge hybrid data with JH data of the other counties. 
        
        counties = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']
        
        jh_dates = []
        jh_dates_death = []
        
        
        for i in range(0, len(counties)):
            
            jh_dates.append(self.JH_Fboro[(self.JH_Fboro.county==counties[i]) & (self.JH_Fboro.cases==0)].index[-1])
            
            jh_dates_death.append(self.JH_Fboro[(self.JH_Fboro.county==counties[i]) & (self.JH_Fboro.deaths == 0)].index[-1])
            
        
        
        #pdb.set_trace()
        ### HYBRIDATION: hybrid confirmed cases data & hybrid deaths data
        
        hybriddat_boro = pd.DataFrame()
        
        day = datetime.datetime(pd.to_datetime(jh_dates[0]).year,
                     pd.to_datetime(jh_dates[0]).month,
                     pd.to_datetime(jh_dates[0]).day+1).strftime('%Y-%m-%d')
        
        k = 0
        for i in range(0,len(counties)):
            nychealthboro = self.nyc_hboro_cum[self.nyc_hboro_cum.county==counties[i]].loc[self.nyc_hboro_cum.index[0]:jh_dates[0]]
            nycjhboro = self.JH_Fboro[self.JH_Fboro.county==counties[i]].loc[day:]
            hybrid = pd.concat([nychealthboro, nycjhboro], axis=0)
            
            if k==0:
                hybriddat_boro = hybrid.copy()
            else:
                hybriddat_boro = pd.concat([hybriddat_boro,hybrid],axis=0)
            k=k+1
            
        self.hybrid_boro = hybriddat_boro[['fips', 'county', 'cases', 'deaths']] # It is the hybrid data
        
        
        dataset_hybrid_cases = pd.DataFrame(index=np.unique(self.hybrid_boro.index), columns=counties)
        dataset_hybrid_deaths = pd.DataFrame(index=np.unique(self.hybrid_boro.index), columns=counties)
        
        #pdb.set_trace()
        for i in range(0,5):
            #pdb.set_trace()
            dataset_hybrid_cases[counties[i]]=self.hybrid_boro[self.hybrid_boro.county==counties[i]]['cases'].values
            dataset_hybrid_deaths[counties[i]]=self.hybrid_boro[self.hybrid_boro.county==counties[i]]['deaths'].values
        
        #### graphics visualization using dataset_hybrid_cases and dataset_hybrid_deaths.
        #pdb.set_trace()
        
        
        
        
    def Merge(self):
        
        self.hybrid_boro = self.hybrid_boro.reset_index()
        #pdb.set_trace()
        hybrid_ny = pd.DataFrame(columns=['date', 'fips', 'county', 'cases', 'deaths'])
        
        counties = ['Bronx','Kings','New York','Queens','Richmond']
        all_cnties = np.unique(self.JH_rogze['county'].values)
        
        k = 0
        for i in range(0, len(all_cnties)):
            cty = all_cnties[i]
            aux = cty in counties
            if aux==False:
                if k==0:
                    hybrid_ny = self.JH_rogze[self.JH_rogze.county==cty][['date', 'fips', 'county', 'cases', 'deaths']].copy()
                else: 
                    hybrid_ny = pd.concat([hybrid_ny, self.JH_rogze[self.JH_rogze.county==cty][['date', 'fips', 'county', 'cases', 'deaths']].copy()], axis=0)
                k = k+1
                
            else:
                if k==0:
                    hybrid_ny=self.hybrid_boro[self.hybrid_boro.county==cty][['date', 'fips', 'county', 'cases', 'deaths']].copy()
                else:
                    hybrid_ny=pd.concat([hybrid_ny, self.hybrid_boro[self.hybrid_boro.county==cty][['date', 'fips', 'county', 'cases', 'deaths']].copy()], axis=0)
                k = k+1
                
        
        
        #self.hybrid_ny = hybrid_ny
        
        def Zscore(hybrid_ny):
            #pdb.set_trace()
            vec=np.unique(hybrid_ny['county'].to_list())
            hybrid_ny.reset_index(inplace = True, drop = True)
            HZdf = pd.DataFrame(columns=['date', 'fips', 'county', 'cases', 'deaths'])
            
            k = 0
            for cty in vec:
                Zscor_cty = pd.DataFrame(columns=['date', 'fips', 'county', 'cases', 'deaths'])
                aux = hybrid_ny[hybrid_ny.county == cty].copy()
                
                mean_aux_c = aux['cases'].mean()
                std_aux_c = aux['cases'].std()
                numerador_c = aux['cases'] - mean_aux_c
                
                Zscor_cty['date'] = aux['date'].copy()
                Zscor_cty['fips'] = aux['fips'].copy()
                Zscor_cty['county'] = aux['county'].copy()
                Zscor_cty['cases'] = numerador_c.div(std_aux_c)
                
                Zscor_cty['cases_not_norm'] = aux['cases'].values 
                
                mean_aux_d = aux['deaths'].mean()
                std_aux_d = aux['deaths'].std()
                numerador_d = aux['deaths'] - mean_aux_d
                
                Zscor_cty['deaths'] = numerador_d.div(std_aux_d)
                
                Zscor_cty['deaths_not_norm'] = aux['deaths'].values 
                
                if k==0: 
                    HZdf = Zscor_cty.copy()
                else:
                    HZdf = pd.concat([HZdf, Zscor_cty], axis=0)
                    
                k = k+1
                
            return HZdf
                
    
        self.Hybrid=Zscore(hybrid_ny)
        
        ### days columns
        
        day1 = self.Hybrid.loc[0,'date']
        days = (pd.to_datetime(self.Hybrid['date']) - pd.to_datetime(day1))/np.timedelta64(1, 's')
        days = days/3600/24
        x = days.to_numpy()
        self.Hybrid['days'] = x
        self.Hybrid.to_csv('../output/Hybridata/NY_hybridata_COUNTIES_std.csv', index=False)
        print('Done')
        
        return self.Hybrid
        

class SmoothingHybrid:
    
    def __init__(self, df_HRZ):
        self.df_HRZ=df_HRZ
        #pdb.set_trace()
    
    def polyreg(self, alp, degree): 
        
        def model(degree,alp):
            model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=alp, fit_intercept=False)) 
            return model
        
        idx = self.df_HRZ[self.df_HRZ.county=='Unassigned'].index
        self.df_HRZ.drop(idx, inplace = True)
        HRZ = pd.DataFrame()
        self.cties = np.unique(self.df_HRZ['county'])
        k=0
        for cty in self.cties:
            print('POLYNOMIAL REGRESSION PROCESSING ' + str(cty))
            temp = pd.DataFrame(columns=['date', 'days', 'county', 'fit_cases', 'deaths', 'fit_deaths'])
            
            aux = self.df_HRZ[self.df_HRZ.county==cty].copy()
            
            d = aux['days'].copy()
            x = d.to_numpy()
            
            X = x[:,np.newaxis]
            y = aux['cases'].to_numpy()
            y_d = aux['deaths'].to_numpy()
            
            model_test = model(degree, alp)
            
            model_test.fit(X,y)
            model_test.fit(X,y_d)
            
            y = model_test.predict(X)
            y_d = model_test.predict(X)
            
            #scr = model_test.score(X,y)
            #scr_d = model_test.score(X,y_d)
            
            temp['date'] = aux['date'].copy()
            temp['days'] = aux['days'].copy()
            temp['county'] = aux['county'].copy()
            temp['cases'] = aux['cases'].copy()
            temp['deaths'] = aux['deaths'].copy()
            temp['fit_cases'] = pd.Series(y_d).values
            temp['fit_deaths'] = pd.Series(y_d).values 
            temp['cases_not_norm'] = aux['cases_not_norm'].copy()
            temp['deaths_not_norm'] = aux['deaths_not_norm'].copy()
            
            if k==0:
                HRZ = temp.copy()
                k = k+1
            else:
                HRZ = pd.concat([HRZ, temp], axis=0)
            
           
        return HRZ
    
    def CuSpline(self, wdw, wdw_d):
        idx = self.df_HRZ[self.df_HRZ.county=='Unassigned'].index
        self.df_HRZ.drop(idx, inplace = True)
        vctr = np.unique(self.df_HRZ['county'].values)
        cub_sp_cties = pd.DataFrame()
        
        for i in range(0,len(vctr)):
            cty = vctr[i]
            print('CUBIC SPLINE PROCESSING ' + str(cty))
            aux = self.df_HRZ[self.df_HRZ.county==vctr[i]].reset_index()
            aux = aux.drop(['index'], axis=1)
            aux['days']=aux.index
            
            
            idx = [i for i in range(0,len(aux.index)) if i%wdw==0]
            idx_d = [i for i in range(0,len(aux.index)) if i%wdw_d==0]
            
            if idx[-1]==aux.index[-1]:
                sub_aux = aux.loc[idx]
            else:
                idx.append(aux.index[-1])
                sub_aux=aux.loc[idx]
                
            if idx_d[-1]==aux.index[-1]:
                sub_aux_d = aux.loc[idx_d]
            else:
                idx_d.append(aux.index[-1])
                sub_aux_d = aux.loc[idx_d]
            
            xx = aux['days'].values
            yy = aux['cases_wthn'].values
            yy_d = aux['deaths_wthn'].values
            
            
            x = sub_aux['days'].values
            x_d = sub_aux_d['days'].values
            
            y = sub_aux['cases_wthn'].values
            y_d = sub_aux_d['deaths_wthn'].values
            
            #print(str(cty))
            #if cty=='Bronx':
            #    pass
            #pdb.set_trace()
            cs = CubicSpline(x,y)
            cs_d = CubicSpline(x_d,y_d)
            
            aux['fit_cases_sp']=cs(xx)
            aux['fit_deaths_sp']=cs_d(xx)
            
            if i==0:
                cub_sp_cties = aux.copy()
            else:
                cub_sp_cties = pd.concat([cub_sp_cties, aux], axis=0)
        
        return cub_sp_cties
    
    def LeastSquares(self,g_c,g_d):
        idx = dfaux[dfaux.county=='Unassigned'].index
        dfaux.drop(idx, inplace = True)
        cty=np.unique(dfaux['county'].values)
        interpolations = pd.DataFrame()
        k=0
        for cy in cty:
            print('LEAST SQUARES PROCESSING ' + str(cy))
            dataux = dfaux[dfaux.county==cy].copy()
            
            x = dataux['days'].values
            y = dataux['cases_wthn'].values
            
            y_d = dataux['deaths_wthn'].values
            
            coeff = np.polyfit(x,y,g_c)
            coeff_d = np.polyfit(x,y_d,g_d)
            
            p = np.poly1d(coeff)
            p_d = np.poly1d(coeff_d)
            
            dataux['fit_cases_ls'] = p(x)
            dataux['fit_deaths_ls'] = p_d(x)
            
            if k==0:
                interpolations = dataux.copy()
                k=k+1
            else:
                interpolations = pd.concat([interpolations, dataux], axis=0)
        
        return interpolations
            
        
        


PATHJH = '../output/JHopkins/'
PATHNYC = '../output/NYChealth/historical/'

hybrid=DataNY()
hybrid.MakeFiles([PATHJH + 'JHraw_epidemiology_NY_std.csv', PATHNYC + 'NYChealthraw_epidemiology_BOROUGT_std.csv', PATHNYC + 'NYChealthraw_epidemiology_NYC_std.csv'])
hybrid.HybridData()
HRZ=hybrid.Merge()   ### It is the hibrid database for all counties of the NY. 

#Result = SmoothingHybrid(HRZ)
#HRZreg=Result.polyreg(20,3) ## Polynomial Regression on the hibrid database.

def errorReg(HRZ,alpha,degrees):
    
    E_cases = pd.DataFrame()
    E_deaths = pd.DataFrame()
    
    #j=0
    
    cties = np.unique(HRZ['county'].values)
    l=0
    for cty in cties:
        print('POLYNOMIAL REGRESSION ERROR ' + str(cty))
        cases = pd.DataFrame(columns=['county', 'alpha', 'k', 'Loss', 'L2_norm', 'L1_norm'])
        deaths = pd.DataFrame(columns=['county', 'alpha', 'k', 'Loss', 'L2_norm', 'L1_norm'])
        
        cases['k'] = degrees
        deaths['k'] = degrees
        cases['county'] = [cty]*len(degrees)
        deaths['county'] = [cty]*len(degrees)
        
        for alp in alpha:
            cases['alpha'] = [alp]*len(degrees)
            deaths['alpha'] = [alp]*len(degrees)
            
            for d in degrees:
                MethodReg = SmoothingHybrid(HRZ)
                HRZreg = MethodReg.polyreg(alp,d)
                
                aux = HRZreg[HRZreg.county==cty]
                
                vec1 = aux['cases']
                vec2 = aux['deaths']
                
                L = sum((vec1-aux['fit_cases'].values)**2/len(vec1))
                L_d = sum((vec2-aux['fit_deaths'].values)**2/len(vec2))
                
                L2_norm = np.sum(np.power((vec1-aux['fit_cases'].values),2))
                L2_norm_d = np.sum(np.power((vec2-aux['fit_deaths'].values),2))
                
                L1_norm = np.linalg.norm((vec1-aux['fit_cases'].values), ord=1)
                L1_norm_d = np.linalg.norm((vec2-aux['fit_deaths']), ord=1)
                
                cases.loc[d-2, 'Loss'] = L
                deaths.loc[d-2, 'Loss'] = L_d
                cases.loc[d-2, 'L2_norm'] = L2_norm
                deaths.loc[d-2, 'L2_norm'] = L2_norm_d
                cases.loc[d-2, 'L1_norm'] = L1_norm
                deaths.loc[d-2, 'L1_norm'] = L1_norm_d
                
            if l==0:
                E_cases = cases.copy()
                E_deaths = deaths.copy()
                l = l+1
            else:
                E_cases = pd.concat([E_cases,cases], axis=0)
                E_deaths = pd.concat([E_deaths,deaths], axis=0)
                
    return E_cases, E_deaths 


alpha = [10, 20, 30, 40, 50]
degrees = [2,3,4,5,6,7,8] 
Ereg=errorReg(HRZ,alpha,degrees) ## It calculates the error for different polynomial degrees and alpha values.

## The ToChoose() function chooses the values of alpha and degree which we obtain the lower error

def ToChoose_Reg(E):
    ## The best parameters; alpha and k to each county
    cties = np.unique(E[0]['county'].values)
    ## we go through all the counties
    cty_opt_dat_cases = pd.DataFrame()
    cty_opt_dat_deaths = pd.DataFrame()
    
    k=0
    for cty in cties:
        print('CHOOSING THE BEST PARAMETERS ' + str(cty))
        aux_cases = E[0][E[0].county==cty]
        aux_deaths = E[1][E[1].county==cty]
        
        opt = aux_cases[aux_cases.Loss==aux_cases['Loss'].min()]
        optt = aux_deaths[aux_deaths.Loss==aux_deaths['Loss'].min()]
        
        if k==0:
            cty_opt_dat_cases = opt
            cty_opt_dat_deaths = optt
            k=k+1
        else:
            cty_opt_dat_cases = pd.concat([cty_opt_dat_cases, opt], axis=0)
            cty_opt_dat_deaths = pd.concat([cty_opt_dat_deaths, optt], axis=0)
            
    return cty_opt_dat_cases, cty_opt_dat_deaths


param_opt = ToChoose_Reg(Ereg)

def OptPoly(param_opt, HRZ):
    cties = param_opt[0]['county'].values
    Result_opt_cty_cases = pd.DataFrame()
    Result_opt_cty_deaths = pd.DataFrame()
    k=0
    for cty in cties:
        print('POLYNOMIAL REGRESSION WITH THE OPTIMAL PARAMETERS ' + str(cty))
        aux_opt_cases = param_opt[0]
        aux_opt_deaths = param_opt[1]
        
        alpha_opt = aux_opt_cases[aux_opt_cases.county==cty]['alpha'].values[0]
        degree_opt = aux_opt_cases[aux_opt_cases.county==cty]['k'].values[0]
        
        alpha_opt_d = aux_opt_deaths[aux_opt_deaths.county==cty]['alpha'].values[0]
        degree_opt_d = aux_opt_deaths[aux_opt_deaths.county==cty]['k'].values[0]
        
        MethodReg = SmoothingHybrid(HRZ)
        HRZreg_pre_result = MethodReg.polyreg(alpha_opt,degree_opt)
        HRZreg_pre_result_d = MethodReg.polyreg(alpha_opt_d, degree_opt_d)
        
        result_cty = HRZreg_pre_result[HRZreg_pre_result.county==cty]
        result_cty_d = HRZreg_pre_result_d[HRZreg_pre_result_d.county==cty]
        
        if k==0:
            Result_opt_cty_cases = result_cty
            Result_opt_cty_deaths = result_cty_d
            k=k+1
        else: 
            Result_opt_cty_cases = pd.concat([Result_opt_cty_cases, result_cty], axis=0)
            Result_opt_cty_deaths = pd.concat([Result_opt_cty_deaths,result_cty_d], axis=0)
    
    
    # we tour Result_opt_cty_cases and modify the columns fit_deaths
    
    cties = np.unique(Result_opt_cty_cases['county'].values)
    
    for cty in cties:
        auxx = Result_opt_cty_cases[Result_opt_cty_cases.county==cty]['fit_deaths'].reset_index()
        idx = auxx['index'].values
        Result_opt_cty_cases[Result_opt_cty_cases.county==cty].loc[idx,'fit_deaths']=Result_opt_cty_deaths[Result_opt_cty_deaths.county==cty]['fit_deaths'].values.copy()
    
    Result_opt_cty = Result_opt_cty_cases.copy()
    
    def ComeBack(Result_opt_cty):
        df_HRZ = Result_opt_cty.copy()
        ## to each county
        df_HRZ_cb = pd.DataFrame()
        vec = np.unique(df_HRZ['county'].values)
        for i in range(0,len(vec)):
            aux = df_HRZ[df_HRZ.county==vec[i]].copy()
            
            std = aux['cases_not_norm'].std()
            mn = aux['cases_not_norm'].mean()
            
            std_d = aux['deaths_not_norm'].std()
            mn_d = aux['deaths_not_norm'].mean()
            
            aux['fit_cases_ori'] = std*aux['fit_cases'].copy() + mn
            aux['fit_deaths_ori'] = std_d*aux['fit_deaths'].copy() + mn_d
            
            if i == 0:
                df_HRZ_cb = aux.copy()
                
            else:
                df_HRZ_cb = pd.concat([df_HRZ_cb, aux], axis=0)
        
        return df_HRZ_cb
    
    df_HRZ_cb = ComeBack(Result_opt_cty)
    df_HRZ_cb = df_HRZ_cb.rename(columns={'fit_cases':'fit_cases_Zreg', 'fit_deaths':'fit_deaths_Zreg', 'fit_cases_ori':'fit_cases_Oreg', 'fit_deaths_ori':'fit_deaths_Oreg','cases_not_norm':'cases_wthn','deaths_not_norm':'deaths_wthn'})
    
    df = df_HRZ_cb.reset_index()
    df = df.drop('index', axis=1)
    
    return df

Result_reg = OptPoly(param_opt, HRZ)
#pdb.set_trace()

#MethodSpline = SmoothingHybrid(Result_reg)
#testing = MethodSpline.CuSpline(30,8)

def errorSp(df,W):
    idx = df[df.county=='Unassigned'].index
    df.drop(idx, inplace = True)
    Error = pd.DataFrame()
    errores = pd.DataFrame(columns=['county', 'wdw_cases', 'Loss_cases', 'wdw_deaths', 'Loss_deaths'])
    errores['wdw_cases'] = W
    errores['wdw_deaths'] = W
    u=0
    for county in np.unique(df['county'].values):
        errores['county'] = [county]*len(W)
        for i,j in zip(W,W):
            MethodSpline = SmoothingHybrid(df)
            int_df = MethodSpline.CuSpline(i,j)
            intdf_by_cty = int_df[int_df.county==county]
            ## cases_wthn, deaths_wthn, fit_cases_sp, fit_deaths_sp
            vec = intdf_by_cty['cases_wthn'].values
            sp = intdf_by_cty['fit_cases_sp'].values
            L = sum((vec-sp)**2/len(vec))
            errores.loc[errores.wdw_cases==i, 'Loss_cases'] = L
            
            vec_d = intdf_by_cty['deaths_wthn'].values
            sp_d = intdf_by_cty['fit_deaths_sp'].values 
            L_d = sum((vec_d-sp_d)**2/len(vec_d))
            errores.loc[errores.wdw_deaths==j, 'Loss_deaths'] = L_d
            
        if u == 0:
            Error = errores.copy()
        else:
            Error = pd.concat([Error, errores], axis=0)
        u = u+1
    
    return Error

W = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
Esp = errorSp(Result_reg,W)

def ToChooseSp(E):
    cties = np.unique(E['county'].values)
    Bestwdw = pd.DataFrame(columns=['county', 'bwdw_cases', 'bwdw_deaths'])
    Bestwdw['county'] = cties
    for cty in cties: 
        e_cty = E[E.county==cty]
        bwdw_cases = median(e_cty[e_cty.Loss_cases==e_cty['Loss_cases']]['wdw_cases'])
        bwdw_deaths = median(e_cty[e_cty.Loss_deaths==e_cty['Loss_deaths']]['wdw_deaths'])
        Bestwdw.loc[Bestwdw.county==cty, 'bwdw_cases'] = bwdw_cases
        Bestwdw.loc[Bestwdw.county==cty, 'bwdw_deaths'] = bwdw_deaths
    
    recurrent_c = Bestwdw['bwdw_cases'].mode().values[0]
    recurrent_d = Bestwdw['bwdw_deaths'].mode().values[0]
    
    return recurrent_c, recurrent_d

opt_wdw = ToChooseSp(Esp)
MethodSpline = SmoothingHybrid(Result_reg)
data_result_sp = MethodSpline.CuSpline(opt_wdw[0],opt_wdw[1])

dfaux = data_result_sp.copy()
df = dfaux.reset_index()

df = df.drop('index', axis=1)

#MethodLsquares = SmoothingHybrid(df)
#testing = MethodLsquares.LeastSquares(3,3)
    

def errorLsquares(dfaux,K):
    idx = dfaux[dfaux.county=='Unassigned'].index
    dfaux.drop(idx, inplace = True)
    Error = pd.DataFrame()
    errores = pd.DataFrame(columns=['county', 'k_cases', 'Loss_cases', 'k_deaths', 'Loss_deaths'])
    errores['k_cases'] = K
    errores['k_deaths'] = K
    u = 0
    for county in np.unique(dfaux['county'].values):
        errores['county'] = [county]*len(K)
        for i,j in zip(K,K):
            MethodLsquares = SmoothingHybrid(dfaux)
            int_df = MethodLsquares.LeastSquares(i,j)
            intdf_by_cty = int_df[int_df.county==county]
            ## cases_wthn, deaths_wthn, fit_cases_ls, fit_deaths_ls
            vec = intdf_by_cty['cases_wthn'].values
            ls = intdf_by_cty['fit_cases_ls'].values
            L = sum((vec-ls)**2/len(vec))
            errores.loc[errores.k_cases==i, 'Loss_cases'] = L
            
            vec_d = intdf_by_cty['deaths_wthn'].values
            ls_d = intdf_by_cty['fit_deaths_ls'].values
            L_d = sum((vec_d-ls_d)**2/len(vec_d))
            errores.loc[errores.k_deaths==j, 'Loss_deaths'] = L_d
        
        if u == 0:
            Error = errores.copy()
        else: 
            Error = pd.concat([Error, errores], axis=0)
        u=u+1
    
    return Error

K = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
E = errorLsquares(df,K)

def ToChooseLsquares(E):
    cties = np.unique(E['county'].values)
    Bestdeegre = pd.DataFrame(columns=['county', 'bdeegre_cases', 'bdeegre_deaths'])
    Bestdeegre['county']=cties
    
    for cty in cties:
        e_cty = E[E.county==cty]
        bd_cases = e_cty[e_cty.Loss_cases==e_cty['Loss_cases'].min()]['k_cases'].values[0]
        bd_deaths = e_cty[e_cty.Loss_deaths==e_cty['Loss_deaths'].min()]['k_deaths'].values[0]
        Bestdeegre.loc[Bestdeegre.county==cty, 'bdeegre_cases'] = bd_cases
        Bestdeegre.loc[Bestdeegre.county==cty, 'bdeegre_deaths'] = bd_deaths
    
    recurrent_c = Bestdeegre['bdeegre_cases'].mode().values[0]
    recurrent_d = Bestdeegre['bdeegre_deaths'].mode().values[0]
    return recurrent_c, recurrent_d

opt_k = ToChooseLsquares(E)
MethodLsquares = SmoothingHybrid(df)
data_result_final = MethodLsquares.LeastSquares(opt_k[0],opt_k[1])

def DebuggingData(data):
    cties = np.unique(data['county'].values)
    Result = pd.DataFrame()
    k=0
    for cty in cties:
        auxdf = data[data.county==cty].copy()
        
        if len(auxdf[auxdf.fit_cases_Oreg < 0]) > 0: 
            last0_idx = auxdf[auxdf.fit_cases_Oreg < 0].index[-1]
            auxdf.loc[0:last0_idx, 'fit_cases_Oreg'] = 0
            
        elif len(auxdf[auxdf.fit_deaths_Oreg < 0]) > 0:            
            last1_idx = auxdf[auxdf.fit_deaths_Oreg < 0].index[-1]
            auxdf.loc[0:last1_idx, 'fit_deaths_Oreg'] = 0
        elif len(auxdf[auxdf.fit_cases_sp < 0]) > 0:
            last2_idx = auxdf[auxdf.fit_cases_sp < 0].index[-1]
            auxdf.loc[0:last2_idx, 'fit_cases_sp'] = 0
        elif len(auxdf[auxdf.fit_deaths_sp < 0]) > 0:
            last3_idx = auxdf[auxdf.fit_deaths_sp < 0].index[-1]
            auxdf.loc[0:last3_idx, 'fit_deaths_sp'] = 0
        elif len(auxdf[auxdf.fit_cases_ls < 0]) > 0:
            last4_idx = auxdf[auxdf.fit_cases_ls < 0].index[-1]
            auxdf.loc[0:last4_idx, 'fit_cases_ls'] = 0
        elif len(auxdf[auxdf.fit_deaths_ls < 0]) > 0:
            last5_idx = auxdf[auxdf.fit_deaths_ls < 0].index[-1]
            auxdf.loc[0:last5_idx, 'fit_deaths_ls'] = 0
            
        if k==0:
            Result = auxdf.copy()
        else:
            Result = pd.concat([Result, auxdf], axis=0)
        k=k+1
    
    return Result

data = data_result_final.copy()
Result = DebuggingData(data)
Regpoly_CuSpline_LeSquares=Result.copy()
Regpoly_CuSpline_LeSquares.to_csv('../output/Hybridata/HybridData_Regpoly_Cuspline_LeSquares_epidemiology_NYCties_std.csv', index= False)
    
     
       
        
    

            
    




