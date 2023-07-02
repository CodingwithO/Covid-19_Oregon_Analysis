import os
import pandas as pd

def process_data_chunks():
    directory = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    filename_confirmed = 'time_series_covid19_confirmed_US.csv'
    filename_deaths = 'time_series_covid19_deaths_US.csv'
    file_path_confirmed = os.path.join(directory, filename_confirmed)
    file_path_deaths = os.path.join(directory, filename_deaths)

    confirmed_chunks = pd.read_csv(file_path_confirmed, chunksize=1000)
    deaths_chunks = pd.read_csv(file_path_deaths, chunksize=1000)

    processed_chunks = []

    for confirmed_chunk, deaths_chunk in zip(confirmed_chunks, deaths_chunks):
        # Perform data processing steps on each chunk
        confirmed_chunk = preprocess_confirmed_data(confirmed_chunk)
        deaths_chunk = preprocess_deaths_data(deaths_chunk)

        processed_chunk = merge_data(confirmed_chunk, deaths_chunk)

        processed_chunks.append(processed_chunk)

    # Concatenate the processed chunks into a single DataFrame
    processed_df = pd.concat(processed_chunks)

    # Return the processed DataFrame
    return processed_df

def preprocess_confirmed_data(confirmed_df):
    # Select only the necessary columns
    confirmed_df = confirmed_df[['Admin2'] + list(confirmed_df.columns[-7:])]

    # Rename columns for readability
    date_columns = confirmed_df.columns[1:]
    new_columns = ['Date'] + [pd.to_datetime(col).strftime('%Y-%m-%d') for col in date_columns]
    confirmed_df.columns = new_columns

    return confirmed_df

def preprocess_deaths_data(deaths_df):
    # Select only the necessary columns
    deaths_df = deaths_df[['Admin2'] + list(deaths_df.columns[-7:])]

    # Rename columns for readability
    date_columns = deaths_df.columns[1:]
    new_columns = ['Date'] + [pd.to_datetime(col).strftime('%Y-%m-%d') for col in date_columns]
    deaths_df.columns = new_columns

    return deaths_df

def merge_data(confirmed_df, deaths_df):
    # Merge the confirmed and deaths DataFrames on 'Admin2' to get total confirmed cases and deaths in one DataFrame.
    # You may need to adapt this depending on how your deaths DataFrame is named and structured
    merged_df = pd.merge(confirmed_df, deaths_df, on='Admin2', suffixes=('_confirmed', '_deaths'))

    # Rename columns for readability
    most_recent_date = merged_df.columns[-1]
    merged_df.rename(columns={most_recent_date + '_confirmed': 'Total Confirmed Cases', most_recent_date + '_deaths': 'Total Deaths'}, inplace=True)

    return merged_df
