import pandas as pd 
import numpy as np 
import requests
from bs4 import BeautifulSoup as bs
import os 

url = 'https://nominatim.openstreetmap.org/search.php?q='
q = 'Bank+Mandiri'
format = 'jsonv2'
id = []
dfs = []
s = 0

while True :
    if len(id) == 0 :
        endpoint = url+q+'&'+'format='+format
        response = requests.get(endpoint)
        resp = response.json()
        for i in range(len(resp)-1):
            id.append(resp[i]['place_id'])
        df = pd.DataFrame(resp)
        dfs.append(df)
    else :
        endpoint = url+q+'&'+"exclude_place_ids="
        for i in range(len(id)-1):
            endpoint = endpoint + str(id[i]) + '%2C'
        endpoint = endpoint + str(id[len(id)-1])+'&format='+format
        response = requests.get(endpoint)
        resp = response.json()
        if len(resp) > 0 :
            for i in range(len(resp)-1):
                id.append(resp[i]['place_id'])
            df = pd.DataFrame(resp)
            dfs.append(df)
        else :
            break

data = pd.concat(dfs, ignore_index=True)
database = data[['display_name','type','lat','lon']]
database = database.loc[database['type'] == 'bank']
database = database.reset_index(drop=True)


#split Label name
alamat = []
country = []
provinsi = []
kota = []
zip = []
bank = []

for i in range(len(display_name)):
    if len(display_name[i]) == 10 :
        if len(display_name[i][1]) <= 2 :
            alamat.append(display_name[i][2].strip())
        else : 
            alamat.append(display_name[i][1].strip())
        country.append(display_name[i][-1].strip())
        provinsi.append(display_name[i][-4].strip())
        kota.append(display_name[i][-5].strip())
        zip.append(display_name[i][-2].strip())
        bank.append(display_name[i][0].strip().upper())
    if len(display_name[i]) == 9 :
        alamat.append(display_name[i][1].strip())
        country.append(display_name[i][-1].strip())
        zip.append(display_name[i][-2].strip())
        bank.append(display_name[i][0].strip().upper())
        if len(display_name[i][-3]) < 10 : 
            if len(display_name[i][-4]) < 8 : 
                provinsi.append(display_name[i][-5].strip())
                kota.append(display_name[i][-6].strip())
            else : 
                provinsi.append(display_name[i][-4].strip())
                kota.append(display_name[i][-5].strip())
        else :
            provinsi.append(display_name[i][-3].strip())
            kota.append(display_name[i][-4].strip())
    if len(display_name[i]) == 8 :
        alamat.append(display_name[i][1].strip())
        country.append(display_name[i][-1].strip())
        zip.append(display_name[i][-2].strip())
        bank.append(display_name[i][0].strip().upper())
        if len(display_name[i][-3].split()) == 2:
            provinsi.append(display_name[i][-3].strip())
            kota.append(display_name[i][-4].strip())
        elif len(display_name[i][-3].split()) == 1 : 
            provinsi.append(display_name[i][-4].strip())
            kota.append(display_name[i][-5].strip())
        else :
            provinsi.append(display_name[i][-3].strip())
            kota.append(display_name[i][-4].strip())
    if len(display_name[i]) == 7 :
        alamat.append(display_name[i][1].strip())
        country.append(display_name[i][-1].strip())
        provinsi.append(display_name[i][-3].strip())
        kota.append(display_name[i][-4].strip())
        zip.append(display_name[i][-2].strip())
        bank.append(display_name[i][0].strip().upper())

        
database['alamat'] = alamat
database['provinsi'] = provinsi
database['kota'] = kota
database['zip'] = zip
database['bank'] = bank 

os.remove('Bank Mandiri.csv')
database.to_csv('Bank Mandiri.csv', index=False)