# New York City health-data

Contains standardized raw data the New York City. 

# Files

## NYChealraw_epidemiology_NYC_std

This file contains citywide of NYC daily counts of confirmed cases, hospitalizations, and deaths.

### Data definition by columns

- `date:` Date of diagnosis (cases), date of admission (hospitalizations), date of death (deaths).
- `nyc_case_cnt:` Count of confirmed cases citywide. 
- `nyc_hospilalized_cnt:` Count of hospitalized cases citywide.
- `nyc_death_cnt:` Count of confirmed deaths citywide.
- `nyc_case_cnt_avg`: 7-day average of count of confirmed cases citywide.
- `nyc_hosp_cnt_avg`: 7-day average of count of hospitalized cases citywide.
- `nyc_death_cnt_avg`: 7-day average of count of confirmed deaths citywide.

## NYChealraw_epidemiology_BOROUGT_std

This file contains borough-specific daily counts of confirmed cases, hospitalizations, and deaths.
To each borough we use the name of the county. The following table summarizes the equivalence between borought name and county name.

| BOROUGH | COUNTY | CONTRACTION |
|---------|---------|--------------|
| Bronx | Bronx | bx |
| Brooklyn | Kings | kg |
| Manhattan | New York | ny |
| Queens | Queens | qn |
| Staten Island | Richmond | rd | |

### Data definition by columns

- `date:` Date of diagnosis (cases), date of admission (hospitalizations), date of death (deaths).
- `"Borough contraction"_case_cnt` Count of confirmed cases in the Borough contraction. 
- `"Borough contraction"_hospitalized_cnt:` Count of hospitalized cases in the Borough contraction.
- `"Borough contraction"_death_cnt:` Count of confirmed deaths in the Borough contraction.
- `"Borough contraction"_case_cnt_avg`: 7-day average of count of confirmed cases in the Borough contraction.
- `"Borough contraction"_hospitalized_cnt_avg`: 7-day average of count of hospitalized cases in the Borough contraction.
- `"Borough contraction"_death_cnt_avg`: 7-day average of count of confirmed deaths in the Borough contraction.

# Source:

https://github.com/nychealth

In particular:
https://github.com/nychealth/coronavirus-data/blob/master/trends/data-by-day.csv
