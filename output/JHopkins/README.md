# Johns Hopkins-data
Standardised raw data for the State of New York. Includes Daily Infected ('cases'), deceased ('deaths'), active cases ('active) and recovered ('recovered).

# Level of segregation

Counties (from 2020-03-22)

**Note 1:** This dataset consider the City of New York as an aggregation of 5 counties: Bronx, Kings, New York, Queens, Richmond until 2020-08-30. (These counties also correspond to boroughs: Bronx, Brooklyn, Manhattan, Queens and Staten Island)

**Note 2:** From 2020-08-31 the source segregated New York City into its 5 counties: Bronx, Kings, New York, Queens, and Richmond.

**Note 3:** the fips code associated to the New York City is still to be standardized. Currently is taking the code from the county of New York: 36061 until we find a solution for the conflict.

**Note 4:** The file contains data up to the current day, but does not include it. The numbers in the `JHraw_epidemiology_NY_std.csv` file are the final counts at the end of each day and each row of data reports the cumulative number of coronavirus cases and deaths

# Frequency: 

Daily

# Data definition by columns (NY data)

- `cases:` Total number of cases of Covid-19, confirmed cases plus probable cases. 
- `deaths:` Total number of deaths from Covid-19, confrimed cases plus probable cases. 
- `fips:` County FIPS code
- `county:` County name
- `date`: Date on which data was collected.

# Source:

https://github.com/nytimes/covid-19-data

In particular:
https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv
