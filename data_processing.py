import os
import pandas as pd

def process_data():
    directory = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    filename_confirmed = 'time_series_covid19_confirmed_US.csv'
    filename_deaths = 'time_series_covid19_deaths_US.csv'
    file_path_confirmed = os.path.join(directory, filename_confirmed)
    file_path_deaths = os.path.join(directory, filename_deaths)

    confirmed_df = pd.read_csv(file_path_confirmed)
    deaths_df = pd.read_csv(file_path_deaths)

    # Perform data processing steps as needed
    # ...

    # Return the processed data as a dictionary
    processed_data = {
        'confirmed': confirmed_df,
        'deaths': deaths_df
    }

    return processed_data

processed_data = process_data()
