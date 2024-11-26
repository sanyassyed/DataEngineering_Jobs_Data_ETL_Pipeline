import boto3
import pandas as p
import os
import toml
import io

from aws_utils.aws_utils import connect_to_s3



def read_data(file_name:str, aws_bucket_name:str, aws_region:str) -> p.DataFrame:
    """
    Connects to AWS S3, downloads the mentioned parquet file from the mentioned bucket name in the mentioned region and converts into pandas dataframe

    Args:
        file_name (str): The name of the file to be downloaded.
        aws_bucket_name (str): AWS S3 bucket name where the file is located.
        aws_region (str): AWS region where the bucket is located.
    
    Returns:
        pandas.DataFrame: Reads the parquet file and returns it as a pandas dataframe
    """
    s3, s3_client = connect_to_s3()
    buffer = io.BytesIO()
    object = s3.Object(aws_bucket_name, file_name)
    object.download_fileobj(buffer)
    df = p.read_parquet(buffer)
    return df


def main() -> None:
    """
    Extracts AWS S3 info from config.toml and orchestrates the extraction of the parquet file from s3 into local system as csv
 
    """
    # Load configs
    app_config = toml.load('config.toml')

    # AWS config
    file_name = app_config['aws']['file_name']
    aws_bucket_name = app_config['aws']['bucket_name']
    aws_region = app_config['aws']['region']

    # output folder path
    output_folder_name = app_config['project']['output_folder']
    output_folder_path = os.path.join(os.getcwd(), output_folder_name)
    output_file_path = os.path.join(output_folder_path, 'output.csv')

    # Check and create 'output' folder
    if not os.path.exists(output_folder_path):
        print(f"Creating output folder at: {output_folder_path}")
        os.mkdir(output_folder_path)

    df = read_data(file_name, aws_bucket_name, aws_region)
    #print(df.head())
    df.to_csv(output_file_path, encoding='utf-8-sig', index=False)
    print(f"Data written to {output_file_path}.")

if __name__=="__main__":
    main()