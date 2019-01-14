
# Marco Remane

# # Idealista API to CSV

import datetime
import requests
import pandas as pd
from time import sleep
from pandas.io.json import json_normalize

auth_token = '' # idealista API token
hed = {'Authorization': 'Bearer ' + auth_token}

content = []

for i in range(1,62):
    # Search Parameters (i.e - garage rentals in Barcelona)
    payload = {'propertyType': "garages",
        'operation': "rent",
        'center': "41.3851,2.1734",
        'distance': "15000",
        'numPage': i,
        'maxItems': "50"}
    url = 'https://api.idealista.com/3.5/es/search'
    response = requests.post(url, data=payload, headers=hed)
    print(i, ' page(s) processed. Status code - ',response.status_code, '. Error - ',response.raise_for_status())
    json = response.json()
    content.append(json_normalize(json['elementList'])) # store flat list
    sleep(2) # bypass 1req/sec threshold limit


# Create data frames for each array returned by API and merge all information into one frame.
df = pd.concat([pd.DataFrame(array) for array in content])
df.shape # Check if shape corresponds to amount of data..
df.reset_index(drop=True, inplace=True) #Reset the index.
df.head(1) #Check if all is well.

now = datetime.datetime.now()
date = now.strftime("-%Y-%b-%d-%H%M")
df.to_csv('idealistaAPI-'+date+'.csv', sep=',', encoding='utf-8') #save CSV