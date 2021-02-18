# Hospitalization data
Standardized raw data for Hospital information of the State of New York. It includes weekly (Friday to Thursday) census the COVID-19
facility-level capacity data of hospital beds, initially released the week of Dec 7th, 2020. 

These data are derived from reports with facility-level granularity across two main sources: 1) Department of Health &
Human Services (HHS) TeleTracking, and 2) reporting provided directly to HHS Protect by state/territorial health 
departments on behalf of their healthcare facilities.

This repository includes two more levels of aggregation, county and state levels.

At facility level, reported elements include an append of either "_sum" or "_avg". The suffixes are:

- ´_sum´: denotes the sum of the reports provided for that facility for that element during the week
- ´_avg´: denotes the average of the reports provided for that facility for that element during the week. This average
is calculated from the ´_sum´ divided by the "coverage" reported in the source. If a facility does not report data for a
given field on a given week the coverage = 0. If a facility reports data for a given field all the days of the week
the coverage = 7. 

Therefore, it is important to highlight that the sum of a given field does not necessarily represent the total. No 
statistical analysis is applied to impute no-response.

At 

# Timeline

Data is available starting on July 31, 2020.

# Level of segregation

Hospitals (facilities), Counties and State

# Frequency:

Weekly (Friday to Thursday)

# Data definition by columns (NY data)

## Identifiers:

- `date:` ('collection_week') It indicates the start of the period of reporting (starting Friday).
- `fips:` County FIPS code
- `county:` County name
- `hospital_pk:` This unique key for the given hospital that will match the Centers for Medicare & Medicaid Services 
(CMS) Certification Number (CCN) of the given facility if it exists, otherwise, it is a derived unique key.

- `boundary` This field exists at County and State level only.
    
   When there are fewer than 4 patients in a data 
field in the Hospitals segregated data, the cell is redacted and replaced with -999999.0 from origin (for anonymization 
purposes). This value can be found on Hospital segregation level. However, in order to add up and make averages over 
Counties or the State, we chose two bounding values: 0.0 as a lower limit of patients and 4.0 as an upper limit of 
possible patients in an anonymized data field.

    For `boundary`= 0.0, all data fields originally taken as -999999.0 will be replaced with 0.0. Same logic for 
    `boundary`= 4.0
    
## Variables:

- `total_adult_inpatient:`
- `used_inpatient:`
- `total_adult_confirmed_and_suspected_covid:`
- `total_adult_confirmed_covid:`
- `total_icu:`
- `used_icu:`
- `total_staffed_adult_icu:`
- `used_staffed_adult_icu:`
- `staffed_icu_adult_confirmed_and_suspected_covid:`
- `staffed_icu_adult_confirmed_covid:`

