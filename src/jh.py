import pandas as pd
import numpy as np
import glob
import datetime

df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/10-27-2020.csv')
county = pd.read_csv('../input/population_NY_2019.csv')

county.drop(columns = ['state', 'population'], inplace = True)

df_us = df.loc[df['Country_Region'] == 'US']
df_us_ny = df_us.loc[df_us['Province_State'] == 'New York']


print(df_us_ny['Admin2'].to_list())

today = '2020-10-28'
first_date = '2020-01-22'

total_days = (pd.to_datetime(today)-pd.to_datetime(first_date)).days

d = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

df_total = pd.DataFrame()

k = 0
for i in range(total_days + 1):

    date = (pd.to_datetime(first_date)+pd.DateOffset(i)).strftime('%m-%d-%Y')
    print('Processing ' + date)
    temp = pd.read_csv(d + date + '.csv')
    temp.columns = temp.columns.str.replace('/','_')
    temp.columns = temp.columns.str.replace(' ','_')
    temp.columns = temp.columns.str.lower()

    if 'province_state' in temp.columns:
        temp.rename(columns = {'province_state': 'state', 'country_region': 'country'}, inplace = True)

    flag = 0
    if 'admin2' in temp.columns:
        temp.rename(columns = {'admin2': 'county'}, inplace = True)
        flag = 1

    temp_us = temp.loc[temp['country'] == 'US']
    temp_us_ny = temp_us.loc[temp_us['state'] == 'New York']


    date = pd.to_datetime(date).strftime('%Y-%m-%d')

    temp_us_ny['last_update'] = pd.to_datetime(temp_us_ny['last_update'], infer_datetime_format=True)
    temp_us_ny['last_update'] = pd.to_datetime(temp_us_ny['last_update']).dt.strftime('%Y-%m-%d')
    temp_us_ny.reset_index(inplace=True, drop=True)

    if flag == 1:

        df = pd.DataFrame(np.zeros((len(county), 4)), columns=['cases','deaths','active','recovered'])
        cases_county = temp_us_ny['confirmed'].copy()
        deaths_county = temp_us_ny['deaths'].copy()
        active_county = temp_us_ny['active'].copy()
        recovered_county = temp_us_ny['recovered'].copy()

        t = [date]*len(county)
        df_date = pd.DataFrame(data={'date':t})

        j = 0
        for row in temp_us_ny['county']:
            idx = county.loc[county['county'] == row].index.values
            if idx.size > 0:
                df.loc[idx, 'cases'] = cases_county[j]
                df.loc[idx, 'deaths'] = deaths_county[j]
                df.loc[idx, 'active'] = active_county[j]
                df.loc[idx, 'recovered'] = recovered_county[j]
                if active_county[j] < 0:
                    print('Actives are negative in this county: ', row, date)

            j += 1


        aux = pd.concat([df_date, county, df.astype(int)], axis=1)

        if k == 0:

            df_total = aux.copy()

        else:
            df_total = pd.concat([df_total,aux], axis=0)

        k += 1

df_total.reset_index(inplace=True, drop=True)
print(len(df_total))
print(df_total)
df_total.to_csv('../output/raw_JH_epidemiology_NY_std.csv', index = False)

