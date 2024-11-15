import requests
import json
import pandas as p

def data_download():
    url = 'https://www.themuse.com/api/public/jobs?page=50'
    r = requests.get(url)
    print(r.status_code)
    data = json.loads(r.text)
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    df = p.json_normalize(data['results'])
    #print(df.shape)
    #print(df.head())
    #df.to_csv('data.csv')


df = p.read_csv('data.csv')
columns_raw = ['company.name', 'locations', 'name', 'type', 'publication_date']
df_clean = df[columns_raw]
print(df_clean.shape)
print(df_clean.columns)