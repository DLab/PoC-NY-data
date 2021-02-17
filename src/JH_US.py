import pandas as pd

outpath = '../output/JH_US/'
cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
# there are some counties without fips, but I am adding the one that should be
cases['FIPS'] = cases['FIPS'].fillna(cases['UID']-84000000)
# there are counties that are called Unassigned and Out of [state] for each state,
# that blows up in my face when I try to take it as a county because
# there are inconsistencies in the count of cases and deceased. let's eliminate!
cases = cases[cases['Admin2']!='Unassigned']
cases = cases[~cases['Admin2'].astype(str).str.startswith('Out of ')]
# There are weird fips, 60, 88888, 99999, 66, 69 and 78 (cruises and states) without Admin 2 column, fill with Province_State
cases['Admin2'] = cases['Admin2'].fillna(cases['Province_State'])
# Irrelevant columns
drop_col = ['UID', 'iso2', 'iso3', 'code3', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', 'Admin2', 'Province_State']
rename_col = {'FIPS': 'fips'}
cases.rename(columns=rename_col, inplace=True)
new_cases = cases.drop(columns=drop_col).set_index('fips').T
new_cases.index = pd.to_datetime(new_cases.index)
new_cases.sort_index(inplace=True)
new_cases = new_cases.diff()
new_cases_raw = new_cases.copy()

deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')
# there are some counties without fips, but I am adding the one that should be
deaths['FIPS'] = deaths['FIPS'].fillna(deaths['UID']-84000000)
deaths[deaths['FIPS'].isna()]['FIPS']
# there are counties that are called Unassigned and Out of [state] for each state,
# that blows up in my face when I try to take it as a county because
# there are inconsistencies in the count of cases and deceased. let's eliminate!
deaths = deaths[deaths['Admin2']!='Unassigned']
deaths = deaths[~deaths['Admin2'].astype(str).str.startswith('Out of ')]
# There are weird fips, 60, 88888, 99999, 66, 69 and 78 (cruises and states) without Admin 2 column, fill with Province State
deaths['Admin2'] = deaths['Admin2'].fillna(deaths['Province_State'])
# Irrelevant columns
deaths.rename(columns=rename_col, inplace=True)
deaths_drop = deaths.drop(columns=drop_col + ['Population']).set_index('fips').T
deaths_drop.index = pd.to_datetime(deaths_drop.index)
deaths_drop.sort_index(inplace=True)
new_deaths = deaths_drop.diff()
new_deaths_raw = new_deaths.copy()

print('Routine to fix negative values')
# Routine to fix negative values
i = 1
for fips in new_deaths:
    ndeaths = new_deaths[fips]
    if any(ndeaths < 0):
        while any(ndeaths < 0):
            rest_bmatrix = ndeaths<0 
            rest_matrix = ndeaths[rest_bmatrix] # These are the negative values to be fixed
            sumneg_matrix = ndeaths[rest_bmatrix] * -1
            rest_matrix.index = rest_matrix.index - pd.DateOffset(1) # it is necessary to eliminate them from the previous day
            ndeaths = ndeaths.add(sumneg_matrix, fill_value=0) # We add what we are going to subtract on the day of the problem
            ndeaths = ndeaths.add(rest_matrix, fill_value=0) # We subtract the cases from the previous day
        new_deaths[fips] = ndeaths
    print(f'new_deaths: {i}/{len(new_deaths.columns)}', end='\r')
    i += 1
print()
print('Done new_deaths')
i = 1
for fips in new_cases:
    ncase = new_cases[fips]
    if any(ncase < 0):
        while any(ncase < 0):
            rest_bmatrix = ncase<0 
            rest_matrix = ncase[rest_bmatrix] # These are the negative values to be fixed
            sumneg_matrix = ncase[rest_bmatrix] * -1
            rest_matrix.index = rest_matrix.index - pd.DateOffset(1) # it is necessary to eliminate them from the previous day
            ncase = ncase.add(sumneg_matrix, fill_value=0) # We add what we are going to subtract on the day of the problem
            ncase = ncase.add(rest_matrix, fill_value=0) # We subtract the cases from the previous day
        new_cases[fips] = ncase
    print(f'new_cases: {i}/{len(new_cases.columns)}', end='\r')
    i += 1
print()
print('Done new_cases')


mergednewcases = pd.merge(new_cases.T, cases[['fips', 'Admin2']], left_index=True, right_on='fips')
mergednewcases.rename(columns={'Admin2': 'county'}, inplace=True)
mergednewcases.fillna(0, inplace=True)
mergednewcases_raw = pd.merge(new_cases_raw.T, cases[['fips', 'Admin2']], left_index=True, right_on='fips')
mergednewcases_raw.rename(columns={'Admin2': 'county'}, inplace=True)
mergednewcases_raw.fillna(0, inplace=True)
std_new_cases = pd.melt(mergednewcases, id_vars=['fips', 'county',], var_name='date', value_name='new_cases')
std_new_cases_raw = pd.melt(mergednewcases_raw, id_vars=['fips', 'county',], var_name='date', value_name='new_cases')

mergednew_deaths = pd.merge(new_deaths.T, cases[['fips', 'Admin2']], left_index=True, right_on='fips')
mergednew_deaths.rename(columns={'Admin2': 'county'}, inplace=True)
mergednew_deaths.fillna(0, inplace=True)
mergednew_deaths_raw = pd.merge(new_deaths_raw.T, cases[['fips', 'Admin2']], left_index=True, right_on='fips')
mergednew_deaths_raw.rename(columns={'Admin2': 'county'}, inplace=True)
mergednew_deaths_raw.fillna(0, inplace=True)
std_new_deaths = pd.melt(mergednew_deaths, id_vars=['fips', 'county',], var_name='date', value_name='new_death')
std_new_deaths_raw = pd.melt(mergednew_deaths_raw, id_vars=['fips', 'county',], var_name='date', value_name='new_death')


NYC = [36005, 36047, 36061, 36081, 36085] # you can add more fips to test 

good_job = True
for fips in NYC:
    cumcases = int(cases[cases['fips']==fips][cases.columns[-1]]) # This is the total cases direct of csv in github
    cumdeaths = int(deaths[deaths['fips']==fips][deaths.columns[-1]]) # This is the total deaths direct of csv in github
    test_county_cases = std_new_cases[std_new_cases['fips']==fips].set_index('date')
    test_county_deaths = std_new_deaths[std_new_deaths['fips']==fips].set_index('date')
    if test_county_cases['new_cases'].sum() != cumcases or \
            test_county_deaths['new_death'].sum() != cumdeaths:
        good_job = False
if good_job:
    print('All counties tested are congruent.\nContinue to merge and save')
else:
    print('NOOO! inconsistency error')


out_raw = pd.merge(std_new_cases_raw, std_new_deaths_raw)
out = pd.merge(std_new_cases, std_new_deaths)

out_raw.to_csv(outpath+'JH_US_raw_std.csv', index=False)
out.to_csv(outpath+'JH_US_std.csv', index=False)


NYC = [36005, 36047, 36061, 36081, 36085]
NYC_df = out[out['fips'].isin(NYC)][['date', 'new_cases', 'new_death']].groupby(['date']).sum()
NYC_df['county'] = 'NY-City (Bronx, Kings, New York, Queens and Richmond)'
NYC_df = NYC_df[['county', 'new_cases', 'new_death']]
NYC_df_raw = out_raw[out_raw['fips'].isin(NYC)][['date', 'new_cases', 'new_death']].groupby(['date']).sum()
NYC_df_raw['county'] = 'NY-City (Bronx, Kings, New York, Queens and Richmond)'
NYC_df_raw = NYC_df_raw[['county', 'new_cases', 'new_death']]

NYC_df_raw.to_csv(outpath+'JH_NYC_raw_std.csv', index=False)
NYC_df.to_csv(outpath+'JH_NYC_std.csv', index=False)

# disaggregated New York City
dNYC_df = out[out['fips'].isin(NYC)]
dNYC_df_raw = out_raw[out_raw['fips'].isin(NYC)]
dNYC_df = dNYC_df[['fips', 'date', 'county', 'new_cases', 'new_death']]
dNYC_df_raw = dNYC_df_raw[['fips', 'date', 'county', 'new_cases', 'new_death']]
dNYC_df.to_csv(outpath+'JH_disaggregated_NYC_raw_std.csv', index=False)
dNYC_df_raw.to_csv(outpath+'JH_disaggregated_NYC_std.csv', index=False)