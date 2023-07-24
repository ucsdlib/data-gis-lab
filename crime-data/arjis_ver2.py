import os
import pandas as pd
import numpy as np
import math
from urllib.request import Request, urlopen, urlretrieve
import re
import requests
import io
import argparse
#get data, may need to copy paste new link if download changes
link = "https://opendata.sandag.org/api/views/inmb-xi9i/rows.csv?accessType=DOWNLOAD"
r = requests.get(link)
url_content = r.content
csv_file = open("arjis_data.csv", "wb")
csv_file.write(url_content)
csv_file.close()
#open csv
crime = pd.read_csv("arjis_data.csv")
#adjust columnsm add new ones
crime["Year"] = pd.DatetimeIndex(crime['Date']).year
crime['Month'] = pd.DatetimeIndex(crime['Date']).month
crime["State"] = ['CALIFORNIA'] *len(crime)
#fixing zip codes
codes = []
for x in list(crime["ZIP Code"]):
    if math.isnan(x):
        codes.append(np.nan)
    else:
        cut = re.sub("[^0-9]", "", str(round(x)))
        codes.append(cut)
crime["ZIP Code"] = codes
crime["City"] = crime["Community"]
#reorganize columns
cols_reordered = ['Crime Category','Agency','Charge Description','Date','Year','Month', 'State',
                  'Block Address','ZIP Code','Community', 'City']
crime = crime[cols_reordered]
crime
#save new csv
crime.to_csv("arjis_data.csv", index = False)
