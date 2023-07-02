import os

directory = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series'
filename = 'time_series_covid19_confirmed_US.csv'
file_path = os.path.join(directory, filename)

# Now you can use the 'file_path' variable to access the file.
# Add your data processing code here.

import pandas as pd

# Import the CSV file using the file_path
data = pd.read_csv(file_path)

# Print the first few rows of the data
print(data.head())
