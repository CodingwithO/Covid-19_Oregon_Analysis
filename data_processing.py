import os
import pandas as pd

def process_data_chunks(metric, date):
    directory = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    filename_confirmed = 'time_series_covid19_confirmed_US.csv'
    filename_deaths = 'time_series_covid19_deaths_US.csv'
    file_path_confirmed = os.path.join(directory, filename_confirmed)
    file_path_deaths = os.path.join(directory, filename_deaths)

    confirmed_chunks = pd.read_csv(file_path_confirmed, chunksize=1000)
    deaths_chunks = pd.read_csv(file_path_deaths, chunksize=1000)

    processed_chunks = []

    for confirmed_chunk, deaths_chunk in zip(confirmed_chunks, deaths_chunks):
        confirmed_chunk = preprocess_data(confirmed_chunk)
        deaths_chunk = preprocess_data(deaths_chunk)

        print("Columns in confirmed_chunk:")
        print(confirmed_chunk.columns)

        print("First few rows of confirmed_chunk:")
        print(confirmed_chunk.head())  # prints first 5 rows

        print("Columns in deaths_chunk:")
        print(deaths_chunk.columns)

        print("First few rows of deaths_chunk:")
        print(deaths_chunk.head())  # prints first 5 rows

        processed_chunk = merge_data(confirmed_chunk, deaths_chunk)

        processed_chunks.append(processed_chunk)

    processed_df = pd.concat(processed_chunks)

    # Filter dataframe according to the metric and date
    filtered_df = processed_df[processed_df['Date'] == date][['Admin2', metric]]

    return filtered_df

def preprocess_data(df):
    df = df[['Admin2'] + list(df.columns[-7:])]

    date_columns = df.columns[1:]
    new_columns = ['Date'] + [pd.to_datetime(col).strftime('%Y-%m-%d') for col in date_columns]
    df.columns = new_columns

    return df

def merge_data(confirmed_df, deaths_df):
    merged_df = pd.merge(confirmed_df, deaths_df, on='Admin2', suffixes=('_confirmed', '_deaths'))

    most_recent_date = merged_df.columns[-1]
    merged_df.rename(columns={most_recent_date + '_confirmed': 'Total Confirmed Cases', most_recent_date + '_deaths': 'Total Deaths'}, inplace=True)

    return merged_df
