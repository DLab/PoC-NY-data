import pandas as pd
import sys
import numpy as np
import datetime
import re
import requests
from itertools import groupby

'''
MIT License

Copyright (c) 2021 Faviola Molina - dLab - Fundación Ciencia y Vida

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

class hospitalData:
    def __init__(self, url, output):

        # store used variables
        self.url = url
        self.output = output
        # init stuff
        self.file_name = self.url

        self.date = re.search("\d{8}", self.file_name).group(0)
        print(self.date)
        #date = datetime.strptime(self.date, "%d%m%Y") + timedelta(days=1)
        self.date = pd.to_datetime(self.date).strftime('%Y-%m-%d')
        #self.date = datetime.strftime(self.date, "%Y-%m-%d")

    def retrieveLastFileData(self):

        response = requests.get(self.url)
        csv_path = self.file_name

        df = pd.read_csv(csv_path)
        nHosp = [len(list(group)) for key, group in groupby(df['collection_week'])]
        print(df['fips_code'].unique())
        print(nHosp)



if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_url = sys.argv[1]
        hosp_data = hospitalData(my_url, '../output/HealthGov/HealthGovraw_hospital_NY_std.csv')
        hosp_data.retrieveLastFileData()