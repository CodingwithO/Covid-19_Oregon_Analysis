import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from data_processing import processed_data
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

# Import the processed data from data_processing.py
confirmed_df_oregon = processed_data['confirmed']
deaths_df_oregon = processed_data['deaths']

confirmed_df_oregon.isnull().sum()
deaths_df_oregon.isnull().sum()

print(confirmed_df_oregon.dtypes)
print(deaths_df_oregon.dtypes)

print(confirmed_df_oregon.columns.tolist())

pd.set_option('display.max_columns', None)

print(confirmed_df_oregon)
print(confirmed_df_oregon.columns)
print(confirmed_df_oregon.head())

total_confirmed_by_county = pd.DataFrame({'County': confirmed_df_oregon['Admin2'], 'TotalConfirmed': confirmed_df_oregon.iloc[:, 11:].sum(axis=1)})

# Identify the most recent date in your dataset
# Exclude the non-date columns
date_columns = confirmed_df_oregon.columns[11:]
most_recent_date = date_columns[-1]  # This assumes that the last column in your DataFrame is the most recent date.

# Create a new DataFrame with only the county name and the most recent date
recent_df = confirmed_df_oregon[['Admin2', most_recent_date]]

# Plot a bar graph using the new DataFrame
recent_df.plot(x='Admin2', y=most_recent_date, kind='bar', figsize=(15, 7))
plt.title('Confirmed Cases/Deaths as of ' + most_recent_date)
plt.ylabel('Number of Confirmed Cases/Deaths')
plt.xlabel('County Name')
plt.xticks(rotation=45)  # This will make the county names easier to read
plt.tight_layout()  # This will ensure that all labels fit into the figure
plt.show()


# Merge the confirmed and deaths DataFrames on 'Admin2' to get total confirmed cases and deaths in one DataFrame.
# You may need to adapt this depending on how your deaths DataFrame is named and structured
merged_df = pd.merge(confirmed_df_oregon[['Admin2', most_recent_date]], deaths_df_oregon[['Admin2', most_recent_date]], on='Admin2', suffixes=('_confirmed', '_deaths'))

# Rename columns for readability
merged_df.rename(columns={f'{most_recent_date}_confirmed': 'Total Confirmed Cases', f'{most_recent_date}_deaths': 'Total Deaths'}, inplace=True)

# Create the bar plot
fig = px.bar(merged_df, x='Admin2', y='Total Confirmed Cases',
             hover_data=['Total Confirmed Cases', 'Total Deaths'], # this is where the hover feature is defined
             labels={'Admin2':'County', 'Total Confirmed Cases':'Confirmed Cases'}, # rename labels
             title=f'Confirmed COVID-19 Cases as of {most_recent_date}')

# This line automatically arranges the county names along the x-axis in descending order of confirmed cases.
fig.update_layout(autosize=False, width=1000, height=500, xaxis={'categoryorder':'total descending'})

fig.show()


# Make a copy of the dataframe
confirmed_df_oregon_copy = confirmed_df_oregon.copy()

# Calculate daily increases
confirmed_df_oregon_copy['Daily Increase'] = confirmed_df_oregon_copy[most_recent_date] - confirmed_df_oregon_copy[most_recent_date].shift(1)

# Plot daily increases
fig, ax = plt.subplots(figsize=(12,8))
confirmed_df_oregon_copy.plot(kind='bar', x='Admin2', y='Daily Increase', ax=ax)
plt.title('Daily Increase in Confirmed Cases by County')
plt.show()


# Reshape the data for visualization using Plotly
melted_df = confirmed_df_oregon.melt(
    id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
             'Country_Region', 'Lat', 'Long_', 'Combined_Key'],
    var_name='Date',
    value_name='Total Confirmed Cases'
)

# Clean up the melted DataFrame
melted_df = melted_df[melted_df['Date'] != 'Population']
melted_df['Date'] = pd.to_datetime(melted_df['Date'])
melted_df.set_index('Date', inplace=True)

# Reshape the deaths data for visualization using Plotly
deaths_melted_df = deaths_df_oregon.melt(
    id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
             'Country_Region', 'Lat', 'Long_', 'Combined_Key'],
    var_name='Date',
    value_name='Total Deaths'
)

# Clean up the deaths melted DataFrame
deaths_melted_df = deaths_melted_df[deaths_melted_df['Date'] != 'Population']
deaths_melted_df['Date'] = pd.to_datetime(deaths_melted_df['Date'])
deaths_melted_df.set_index('Date', inplace=True)

# Merge the melted and deaths melted DataFrames
merged_df = pd.merge(melted_df, deaths_melted_df, on=['Date', 'Admin2'])

# Generate the Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("COVID-19 Cases Dashboard"),

    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Total Confirmed Cases', 'value': 'Total Confirmed Cases'},
            {'label': 'Total Deaths', 'value': 'Total Deaths'}
        ],
        value='Total Confirmed Cases',
        style={"width": "50%"}
    ),

    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed=merged_df.index.min().strftime('%Y-%m-%d'),
        max_date_allowed=merged_df.index.max().strftime('%Y-%m-%d'),
        initial_visible_month=merged_df.index.max().strftime('%Y-%m-%d'),
        date=merged_df.index.max().strftime('%Y-%m-%d')
    ),

    dcc.Graph(id='covid-graph'),

], style={"padding": "20px"})

@app.callback(
    Output('covid-graph', 'figure'),
    Input('metric-dropdown', 'value'),
    Input('date-picker', 'date')
)
def update_graph(metric, date):
    date = pd.to_datetime(date)
    filtered_df = merged_df[merged_df.index == date]
    fig = px.bar(filtered_df, x='Admin2', y=metric,
                 hover_data=['Total Confirmed Cases', 'Total Deaths'],
                 labels={'Admin2': 'County', metric: metric},
                 title=f'{metric} on {date.strftime("%Y-%m-%d")}')
    fig.update_layout(autosize=False, width=1000, height=500, xaxis={'categoryorder': 'total descending'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
