# Hospitalization data
Standadised raw data for Hospital information of the State of New York. It includes weekly cesus of hospital beds 
different categories and occupancy of each category.

# Level of segregation

Hospitals, Counties and State

# Frequency:

Weekly

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

