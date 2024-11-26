import boto3
import pandas as p
import os
import toml
import io

from aws_utils.aws_utils import connect_to_s3



def read_data(aws_bucket_name, aws_region):
    s3, s3_client = connect_to_s3()
    file_name = 'jobs_20241126-164558.parquet'
    buffer = io.BytesIO()
    object = s3.Object(aws_bucket_name, file_name)
    object.download_fileobj(buffer)
    df = p.read_parquet(buffer)
    return df


def main():
    # Load configs
    app_config = toml.load('config.toml')

    # AWS config
    aws_bucket_name = app_config['aws']['bucket_name']
    aws_region = app_config['aws']['region']

    df = read_data(aws_bucket_name, aws_region)
    print(df.head())
    df.to_csv('output.csv', encoding='utf-8-sig', index=False)

if __name__=="__main__":
    main()