import requests
import pandas as p
import unicodedata
from dotenv import load_dotenv
import os
import toml
import logging
import boto3
import time
import io
import pyarrow
import argparse


# loading secrets from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
AWS_ACCESS_KEY=os.getenv('ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('SECRET_KEY')

# loading env variables
LOG_FILE = os.getenv('LOG_FILE_PYTHON')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')

logging.basicConfig(
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s : %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename=LOG_FILE,
                   )

logging.info(f"LOG FILE FOR THIS PYTHON SCRIPT IS AT: {LOG_FILE}")

def extract(url, pagination_param, page_number):
    params = {
              pagination_param : page_number,
              "api_key": API_KEY
             }
    try:
        logging.info(f"Making API request to URL: {url} with params: {params}")
        response = requests.get(url, params)
        # raise an error for HTTP status codes 4xx or 5xx 
        # testing use response.headers, response.url, response.status_code
        response.raise_for_status()
        # r.json() is of type dictionary with keys ['page', 'page_count', 'items_per_page', 'took', 'timed_out', 'total', 'results', 'aggregations']
        # 'results' contains the text or the actual data needed
        # .get() function assigns the default value [] if results key is not present
        data = response.json().get('results', [])
        # normalise results into a dataframe
        df = p.json_normalize(data)

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occured while making the GET request: {e}")
        df = p.DataFrame()

    except KeyError:
        logging.error("The expected 'results' key is missing from the response")
        df = p.DataFrame

    if not df.empty:
        columns_raw = ['company.name', 'locations', 'name', 'type', 'publication_date']
        logging.info(f"Columns before clean: {df.columns}")
        df_clean = df[columns_raw]
        logging.info(f"Columns after clean: {df_clean.columns}")
    else:
        logging.warning('Dataframe is empty, no data extracted')
        return df

    return df_clean

# Function to remove accents/diacritics
def remove_diacritics(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

def save_data(df, file_name):
    # Remove accents/diacritics
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
    logging.info(f"Columns after renaming: {df.columns}")

    # city - extract the city name
    # country - extract the country name
    # location column has the structure dict inside a list. The dict has key 'name' which has the data we need
    df[['city', 'country']] = df['location'].apply(lambda row: p.Series([item.strip() for item in row[0]['name'].split(',')]))
    df.drop('location', axis=1, inplace=True)
    
    # only keep date and remove time and other elements
    df['date'] = p.to_datetime(df['date']).dt.date

    return df

def save_to_s3(df, output_file_name, bucket_name, region='us-east-2'):
    session = boto3.Session(
                                aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_SECRET_KEY
                            )

    s3 = session.resource('s3')
    s3_client = session.client('s3')

    # Check & create s3 bucket
    if not s3.Bucket(bucket_name) in s3.buckets.all():
        logging.info(f"{bucket_name} BUCKET DOES NOT EXIST IN S3; SO CREATING IT")
        s3_client.create_bucket(
                                Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint':region}
                                )
        logging.info(f"{bucket_name} BUCKET CREATED ON S3")

    # Convert DataFrame to CSV in memory
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine='pyarrow')

    logging.info(f"Uploading data to S3 bucket: {bucket_name} in region: {region}")
    try:
        s3_client.put_object(Bucket=bucket_name, Key=output_file_name, Body=parquet_buffer.getvalue())
        logging.info(f"{output_file_name} DATA UPLOADED TO S3 AS PARQUET")
    except Exception as e:
        logging.error(f"DATA UPLOAD FAILED DUE TO: {e}")
    
    return

def main(test_run: bool) -> None:
    if test_run:
        logging.info("Running in test mode...")

    else:
        logging.info("Running in production mode...")

    # Load configs
    app_config = toml.load('config.toml')

    # API config
    url = app_config['api']['url']
    pagination_param = app_config['api']['pagination_param']
    page_number = app_config['api']['page_number']

    # AWS config
    aws_bucket_name = app_config['aws']['bucket_name']
    aws_region = app_config['aws']['region']

    # Check and create 'output' folder
    if test_run and not os.path.exists(OUTPUT_FOLDER):
        logging.info(f"Creating output folder at: {OUTPUT_FOLDER}")
        os.mkdir(OUTPUT_FOLDER)

    if test_run:
        raw_data_file = os.path.join(OUTPUT_FOLDER, 'data_raw.csv')
        clean_data_file = os.path.join(OUTPUT_FOLDER, 'data_clean.csv')
    
    output_file_name = f"jobs_{time.strftime('%Y%m%d-%H%M%S')}.parquet"


    # Extract data
    df = extract(url, pagination_param, page_number)
    if df.empty:
        logging.warning(f"No data extracted. Terminating the script")
        return

    logging.info(f"The dataset of shape {df.shape} is extracted")

    if test_run:
        save_data(df, raw_data_file)
        logging.info(f"Raw data is saved to {raw_data_file}")
    
    # testing
    #df = read_data()

    # Tranform data
    df_clean = transform(df)
    logging.info('Data is cleaned!')

    if test_run:
        save_data(df_clean, clean_data_file)
        logging.info(f"Clean data is saved to {clean_data_file}")

    # Upload to S3
    save_to_s3(df_clean, output_file_name, aws_bucket_name, aws_region)
    logging.info(f"ETL Complete!")



if __name__=="__main__":
    parser =  argparse.ArgumentParser(description="Run the script with optional test mode.")
    parser.add_argument('--test_run', 
                        action = 'store_true',
                        help="Run the script in test mode (default: False)")
    args = parser.parse_args()

    main(args.test_run)

