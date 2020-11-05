import base64
import requests
import pandas as pd


url = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    df = pd.DataFrame(req.json())
    todrop = df.loc[df['name'] == '.gitignore']
    df.drop(todrop.index, inplace = True)
    todrop = df.loc[df['name'] == 'README.md']
    df.drop(todrop.index, inplace = True)

    dates = [item.replace('.csv','') for item in df['name']]
    print(dates)
else:
    print('Content was not found.')
