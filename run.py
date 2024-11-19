import requests
import json
import pandas as p
import unicodedata
import ast

def extract(url):
    try:
        response = requests.get(url)
        # raise an error for HTTP status codes 4xx or 5xx 
        response.raise_for_status()
        # r.json() is of type dictionary with keys ['page', 'page_count', 'items_per_page', 'took', 'timed_out', 'total', 'results', 'aggregations']
        # 'results' contains the text or the actual data needed
        # .get() function assigns the default value [] if results key is not present
        data = response.json().get('results', [])
        # normalise results into a dataframe
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
        print(f"The shape of the downloaded data is : {df_clean.shape}")
        print(f"The columns in the downloaded data is {df_clean.columns}")
    return df_clean

# Function to remove accents/diacritics
def remove_diacritics(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

def save_data(df, file_name):
    # Apply to DataFrame
    df = df.map(remove_diacritics)
    df.to_csv(file_name, encoding='utf-8-sig', index=False) # otherwise it writes row numbers as a column

def read_data():
    df = p.read_csv('data.csv', encoding='utf-8')
    return df

    

def transform(df):
    renamed_columns =  {'company.name':'company_name',
                        'locations':'location', 
                        'name':'job_name', 
                        'type':'job_type', 
                        'publication_date':'date'}
    df.rename(columns=renamed_columns, inplace=True)
    print(df.columns)

    # city - extract the city name
    # country - extract the country name
    # location column has the structure dict inside a list. The dict has key 'name' which has the data we need
    df[['city', 'country']] = df['location'].apply(lambda row: p.Series([item.strip() for item in row[0]['name'].split(',')]))
    df.drop('location', axis=1, inplace=True)
    
    # date only remove time and other elements
    df['date'] = p.to_datetime(df['date']).dt.date

    return df

def main():
    url = 'https://www.themuse.com/api/public/jobs?page=50'
    
    df = extract(url)
    print('Data is extracted')
    
    save_data(df, 'data_raw.csv')

    # testing
    #df = read_data()

    print(f"The shape of the data loaded is : {df.shape}")
    print(f"The columns in the data loaded are: {df.columns}")

    df_clean = transform(df)
    print('Data is cleaned')

    save_data(df_clean, 'data_clean.csv')
    print('Data is saved')

    # TODO:
    # write data to s3 bucket

if __name__=="__main__":
    main()

