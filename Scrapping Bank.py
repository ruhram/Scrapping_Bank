import pandas as pd 
import numpy as np 
import requests
from bs4 import BeautifulSoup as bs
import os 

url = 'https://nominatim.openstreetmap.org/search.php?q='
#bank_name = ['Bank Mandiri', 'Bank BNI', 'Bank BRI', 'Bank BCA', 'Maybank Indonesia', 'HSBC Indonesia']
bank_name = ['Bank Mandiri']

for i in range(len(bank_name)) :
    label = bank_name[i]
    s = bank_name[i].split()
    q = s[0]+'+'+s[1]
    
    print('Scrapping '+label+' starting :')
    #q = 'Bank+Mandiri'
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
            print('row_count :', len(dfs), end='\r')
        else :
            endpoint = url+q+'&'+"exclude_place_ids="
            for i in range(len(id)-1):
                endpoint = endpoint + str(id[i]) + '%2C'
            endpoint = endpoint + str(id[len(id)-1])+'&format='+format
            response = requests.get(endpoint)
            resp = response.json()
            if resp[0]['display_name'].split(',')[0].upper() == 'BANK MANDIRI' :
                for i in range(len(resp)-1):
                    id.append(resp[i]['place_id'])
                df = pd.DataFrame(resp)
                dfs.append(df)
                print('row_count :', len(dfs), end='\r')
            else :
                break

    data = pd.concat(dfs, ignore_index=True)
    database = data[['display_name','type','lat','lon']]
    database = database.loc[database['type'] == 'bank']
    database = database.reset_index(drop=True)
    display_name = database['display_name'].str.split(',')

    #split Label name
    alamat = []
    country = []
    provinsi = []
    kota = []
    zip = []
    bank = []

    city_one = ['Bali','Lampung','Maluku','Banten','Riau','Aceh','Bengkulu','Jambi']

    for i in range(len(display_name)):
        bank.append(display_name[i][0].strip().upper())
        if len(display_name[i][-2].strip().split(' ')) != 1 :
            zip.append('0')
        else :
            zip.append(display_name[i][-2].strip())
        country.append(display_name[i][-1].strip())
        if len(display_name[i][1].strip().split(' ')) == 1 :
            alamat.append(display_name[i][2].strip())
        else : 
            alamat.append(display_name[i][1].strip())
        if len(display_name[i][-3].strip().split(' ')) == 1 and display_name[i][-3].strip() not in city_one:
            if len(display_name[i][-2].strip().split(' ')) == 2 or display_name[i][-2].strip() in city_one :
                kota.append(display_name[i][-3].strip())
                provinsi.append(display_name[i][-2].strip())
            else :
                kota.append(display_name[i][-5].strip())
                provinsi.append(display_name[i][-4].strip())
        else :
            kota.append(display_name[i][-4].strip())
            provinsi.append(display_name[i][-3].strip())

    database['alamat'] = alamat
    database['zip'] = zip
    database['bank'] = bank 
    database['country'] = country
    database['provinsi'] = provinsi
    database['kota'] = kota

    os.remove(label+'.csv')
    database.to_csv(label+'.csv', index=False)
    
    print('Scrapping '+label+' Has Finished')