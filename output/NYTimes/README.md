# NY Times-data
Standardised raw data for the State of New York. Only includes Daily Infected ('cases') and deceased ('deaths').

# Level of segregation

Counties.

**Note 1:** The City of New York is an aggregation of 5 counties: Bronx, Kings, New York, Queens, Richmond. They also correspond to boroughs: Bronx, Brooklyn, Manhattan, Queens and Staten Island.

**Note 2:** the fips code associated to the New York City is 99999. This is substituing the NaN code given in the source, as it is not a political unit.

**Note 3:** Data for the state of New York starts on 2020-03-01

**Note 4:** The file contains data up to the current day, but does not include it. The numbers in the `NYTraw_epidemiology_NY_std.csv` file are the final counts at the end of each day and each row of data reports the cumulative number of coronavirus cases and deaths

# Frequency: 

Daily

# Data definition by columns (NY data)

- `Cases:` Total number of cases of Covid-19, confirmed cases plus probable cases. 
- `Deaths:` Total number of deaths from Covid-19, confrimed cases plus probable cases. 
- `fips:` County FIPS code
- `county:` County name
- `Date`: Date on which data was collected.

# Source:

https://github.com/nytimes/covid-19-data

In particular:
https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv
