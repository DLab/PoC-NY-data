# New York City health-data

Contains standardized raw data the New York City. 

# Historical files

## 1] NYChealraw_epidemiology_NYC_std

This file contains citywide of NYC daily counts of confirmed cases, hospitalizations, and deaths.

## 2] NYChealraw_epidemiology_BOROUGT_std

This file contains borough-specific daily counts of confirmed cases, hospitalizations, and deaths.


### Data definition by columns

Files NYChealraw_epidemiology_NYC_std and NYChealraw_epidemiology_BOROUGT_std share the following column names:

- `date:` Date of diagnosis (cases), date of admission (hospitalizations), date of death (deaths).
- `daily_cases:`  Daily count of confirmed cases. 
- `daily_hospilalized:` Daily count of hospitalized cases.
- `daily_deaths:` Daily count of deaths cases.
- `daily_cases_avg`: 7-day average of daily count of confirmed cases.
- `daily_hospitalized_avg`: 7-day average of daily count of hospitalized cases.
- `daily_deaths_avg`: 7-day average of daily count of confirmed deaths.


## 3] tests_NYChealthraw_epidemiology_NYC_std.csv

This file contains the number of people who received PCR test, the number of people with positive results, and the percentage of people tested who tested positive, stratified by day. The dates shown in this table reflect the date of specimen collection (i.e., when someone went to a healthcare provider for a test).

### Data definition by columns 

- `date:` Date of specimen collection.
- `daily_tests:` Number of people who received a PCR test. 
- `daily_positive_tests:` Number of people with a positive result on a PCR test.
- `daily_per_positive:` Percentage of people tested with a PCR test who tested positve. 
- `daily_tests_avg:` 7-day average of number of people who received a PCR test.
- `daily_positive_tests_avg:` 7-day average of number of people with positive results.
- `daily_per_positive_avg:` 7-day average of percentage of people tested with a PCR test who tested positive.


# Cumulative files

## 1] Groupdata_NYChealthraw_epidemiology_BOROUGT_std.csv

This file contains borough-specific daily counts of confirmed cases, hospitalizations, and deaths and rates of confirmed cases, hospitalixacions and deaths, by age group, race/ethnicity group, and sex. Rates are:

 * Cumulative since the start of the outbreak (2020-2-29)

 * Per 100,000 people by borough of residence and demographic groups

### Data definition by columns
- `group:` Group type: Age, Race_ethinicity and Sex.
- `subgroup:` Indicates the age group in years, race/ethnicity group, or sex of stratification.
- `case_cnt:` Number of confirmed cases by indicated group
- `hospitalized_cnt:` Number of hospitalized cases by indicated group
- `death_cnt:` Number of confirmed deaths by indicated group
- `case_rate:`Rate of confirmed cases per 100,000 people by indicated group.
- `hospitalized_rate:` Rate of hospitalized cases per 100,000 people by indicated group
- `death_rate:` Rate of confirmed deaths per 100,000 people by indicated group.


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

