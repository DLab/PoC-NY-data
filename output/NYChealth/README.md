# New York City health-data

Contains standardized raw data the New York City. 

# Files

## NYChealraw_epidemiology_NYC_std

This file contains citywide of NYC daily counts of confirmed cases, hospitalizations, and deaths.

## NYChealraw_epidemiology_BOROUGT_std

This file contains borough-specific daily counts of confirmed cases, hospitalizations, and deaths.


### Data definition by columns

- `date:` Date of diagnosis (cases), date of admission (hospitalizations), date of death (deaths).
- `case:` Count of confirmed cases. 
- `hospilalized:` Count of hospitalized cases citywide
- `case_avg`: 7-day average of count of confirmed cases.
- `hospitalized_avg`: 7-day average of count of hospitalized cases.
- `death_avg`: 7-day average of count of confirmed deaths.


# Note

| BOROUGH | COUNTY | CONTRACTION |
|---------|---------|--------------|
| Bronx | Bronx | bx |
| Brooklyn | Kings | kg |
| Manhattan | New York | ny |
| Queens | Queens | qn |
| Staten Island | Richmond | rd | |


# Source:

https://github.com/nychealth

In particular:
https://github.com/nychealth/coronavirus-data/blob/master/trends/data-by-day.csv

