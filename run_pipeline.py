from data.generate_data import *
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def run_pipeline():

    file_path = "data/raw_sales.csv"

    df = extract_data(file_path)

    transformed_df = transform_data(df)

    load_data(transformed_df)

    print("ETL Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()