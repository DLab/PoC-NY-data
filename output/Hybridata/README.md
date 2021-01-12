# Hybrid data 

Standardized raw data for all New York counties from March 22, 2019 to the last report. Includes the cumulative count of confirmed cases and deaths.

Hybrid data is the union of data from two different sources; Jhon Hopking and Nychealth. 

In addition, hybrid data includes the results of three interpolation models applied to the data. Polynomial regression, cubic spline and least squares. 

# Level of segregation

Counties (from 2020-03-22)

# Frequency: 

Daily

# Data definition by columns (NY data)

- `date:` Date on which data was collected.
- `days:` A numeric value assigned to each date.
- `county:` County name
- `cases:` Standardized cumulative confirmed cases with Z-score method.
- `deaths:` Standardized cumulative confirmed deaths with Z-score method.
- `fit_cases_Zreg:` Polynomial Regression of Standardized confimed cumulative cases with the Z-score method.
- `fit_deaths_Zreg:` Polynomial Regression of Standardized confimed cumulative deaths with the Z-score method.
- `cases_wthn:` Non-standardized confirmed cumulative cases.
- `deaths_wthn:` Non-standardized confirmed cumulative deaths.
- `fit_cases_Oreg:` Polynomial Regression of Standardized non-standardized confimed cumulative cases.
- `fit_deaths_Oreg:` Polynomial Regression of Standardized non-standardized confimed cumulative deaths.
- `fit_cases_sp:` Cubic Spline of Standardized non-standardized confimed cumulative cases.
- `fit_deaths_sp:` Cubic Spline of Standardized non-standardized confimed cumulative deaths.
- `fit_cases_ls:` Least squares of Standardized non-standardized confimed cumulative cases.
- `fit_deaths_ls:` Least squares of Standardized non-standardized confimed cumulative deaths.

# Sources:

1) https://github.com/nychealth/coronavirus-data

2) https://github.com/CSSEGISandData/COVID-19