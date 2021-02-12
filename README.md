# PoC-NY-data
This a proof of concept of the standardised data for the State of New York. Includes cummulative Infected ('cases') and cummulative deceased ('deaths') from New York Times source. 
From Johns Hopkins includes cummulative infected ('cases'), cummulative decesases ('deaths'), active cases ('active') and recovered ('recovered').

# Level of segregation

Counties.

# Frequency: 

Daily

# Data definition by columns (NY data)

- `cases:` Total number of cases of Covid-19, confirmed cases plus probable cases. 
- `deaths:` Total number of deaths from Covid-19, confrimed cases plus probable cases. 
- `fips:` County FIPS code
- `county:` County name
- `date`: Date on which data was collected.
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


