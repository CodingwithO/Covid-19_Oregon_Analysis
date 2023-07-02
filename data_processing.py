import os
import pandas as pd

def process_data_chunks(metric, date):
    directory = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    filename_confirmed = 'time_series_covid19_confirmed_US.csv'
    filename_deaths = 'time_series_covid19_deaths_US.csv'

    confirmed_df = read_preprocess_data(directory, filename_confirmed)
    deaths_df = read_preprocess_data(directory, filename_deaths)

    print_dataset_info(confirmed_df, "confirmed")
    print_dataset_info(deaths_df, "deaths")

    if 'Admin2' in confirmed_df.columns and 'Admin2' in deaths_df.columns:
        processed_df = merge_data(confirmed_df, deaths_df)
    else:
        print("Cannot merge dataframes: 'Admin2' column doesn't exist in both dataframes")
        return None

    # Filter dataframe according to the metric and date
    filtered_df = processed_df[processed_df['Date'] == date][['Admin2', metric]]

    return filtered_df

def read_preprocess_data(directory, filename):
    file_path = os.path.join(directory, filename)
    chunks = pd.read_csv(file_path, chunksize=1000)
    processed_chunks = [preprocess_data(chunk) for chunk in chunks]
    df = pd.concat(processed_chunks)
    return df

def preprocess_data(df):
    df = df[['Admin2'] + list(df.columns[-7:])]

    date_columns = df.columns[1:]
    new_columns = ['Date'] + [pd.to_datetime(col).strftime('%Y-%m-%d') for col in date_columns]
    df.columns = new_columns

    return df

def print_dataset_info(df, data_type):
    print(f"Columns in {data_type}_chunk:")
    print(df.columns)

    print(f"First few rows of {data_type}_chunk:")
    print(df.head())  # prints first 5 rows

def merge_data(confirmed_df, deaths_df):
    merged_df = pd.merge(confirmed_df, deaths_df, on='Admin2', suffixes=('_confirmed', '_deaths'))

    most_recent_date = merged_df.columns[-1]
    merged_df.rename(columns={most_recent_date + '_confirmed': 'Total Confirmed Cases', most_recent_date + '_deaths': 'Total Deaths'}, inplace=True)

    return merged_df
