# Hospitalization data
Standadised raw data for Hospital information of the State of New York. It includes weekly cesus of hospital beds different categories and occupancy of each category.

# Level of segregation

Hospitals, Counties and State

# Frequency: 

Weekly

# Data definition by columns (NY data)

- `date:` ('collection_week') It indicates the start of the period of reporting (starting Friday). 
- `fips:` County FIPS code
- `county:` County name
- `boundary`: When there are fewer than 4 patients in a data field, the cell is redacted and replaced with -999999.0 from origin (for annonimization purposes). This value can be found on Hospital segregation level. However, in order to add up and make averages over Counties or the State, we chose two bounding values: 0.0 as a lower limit of patients and 4.0 as an upper limit of posible patients in an annonimized data field. 

  For `boundary`= 0.0, all data fields originally taken as -999999.0 will be replaced with 0.0. Same logic for `boundary`= 4.0


