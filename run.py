import requests
import json
import pandas as p

url = 'https://www.themuse.com/api/public/jobs?page=50'

# def data_download(url):
#     r = requests.get(url)
#     print(r.status_code)
#     data = json.loads(r.text)
#     with open('data.json', 'w') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
#     df = p.json_normalize(data['results'])
#     #print(df.shape)
#     #print(df.head())
#     #df.to_csv('data.csv')

# def read_local():
#     df = p.read_csv('data.csv')
#     columns_raw = ['company.name', 'locations', 'name', 'type', 'publication_date']
#     df_clean = df[columns_raw]
#     print(df_clean.shape)
#     print(df_clean.columns)

# data_download(url)
# r.json() is of type dictionary with keys ['page', 'page_count', 'items_per_page', 'took', 'timed_out', 'total', 'results', 'aggregations']
# 'results' contains the text or the actual data needed
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json().get('results', [])
    df = p.json_normalize(data)

except requests.exceptions.RequestException as e:
    print(f"An error occured while making the GET request: {e}")
    df = p.DataFrame()

except KeyError:
    print("The expected 'results' key is missing from the response")
    df = p.DataFrame

if not df.empty:
    columns_raw = ['company.name', 'locations', 'name', 'type', 'publication_date']
    df_clean = df[columns_raw]
    print(df_clean.shape)
    print(df_clean.columns)
