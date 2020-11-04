# PoC-NY-data
This a proof of concept of the standardised data for the State of New York. Only includes Daily Infected ('cases') and deceased ('deaths').

# Level of segregation

Counties.

**Note 1:** The City of New York is an aggregation of 5 counties: Bronx, Kings, New York, Queens, Richmond. They also correspond to boroughs: Bronx, Brooklyn, Manhattan, Queens and Staten Island.

**Note 2:** the fips code associated to the New York City is 99999. This is substituing the NaN code given in the source, as it is not a political unit.

**Note 3:** Data for the state of New York starts on 2020-03-01

# Frequency: 

Daily

# Source:

https://github.com/nytimes/covid-19-data

In particular:
https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv
