#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Data Analysis for Oregon State
# 
# In this project, we analyze the number of confirmed COVID-19 cases and deaths in Oregon, USA. We will use the data available publicly by Johns Hopkins University.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Here we are importing the necessary libraries that will be used throughout the project.

# In[2]:


confirmed_df = pd.read_csv('C:/Users/ogbom/COVID-19_Dashboard_Project/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')



# In[3]:


deaths_df = pd.read_csv('C:/Users/ogbom/COVID-19_Dashboard_Project/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')



# We load the data related to confirmed cases and deaths from the respective CSV files.

# In[4]:


confirmed_df_oregon = confirmed_df[confirmed_df['Province_State'] == 'Oregon']


# In[5]:


deaths_df_oregon = deaths_df[deaths_df['Province_State'] == 'Oregon']


# We filter out the data for the state of Oregon only.

# In[6]:


confirmed_df_oregon.isnull().sum()


# In[7]:


deaths_df_oregon.isnull().sum()


# We are checking for null values in our dataset. This is a part of the data cleaning process.

# In[8]:


print(confirmed_df_oregon.dtypes)


# In[9]:


print(deaths_df_oregon.dtypes)


# We print the data types of each column. This gives us an idea of the kind of data we are dealing with in each column.

# In[10]:


print(confirmed_df_oregon.columns.tolist())


# In[11]:


pd.set_option('display.max_columns', None)


# In[12]:


print(confirmed_df_oregon)


# In[13]:


print(confirmed_df_oregon.columns)


# In[14]:


print(confirmed_df_oregon.head())


# These commands give us a broad view of our dataset, allowing us to see all columns and the first few rows of data.

# In[15]:


total_confirmed_by_county = pd.DataFrame({'County': confirmed_df_oregon['Admin2'], 'TotalConfirmed': confirmed_df_oregon.iloc[:, 11:].sum(axis=1)})


# We calculate the total confirmed cases by county.

# In[16]:


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


# We identify the most recent date in the dataset and create a new dataframe with only the county name and the most recent date. We then plot a bar graph to visualize the confirmed cases and deaths as of the most recent date, by county.
# 

# In[17]:


import plotly.express as px

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


# We merge the confirmed cases and deaths dataframes to create a unified dataframe for further analysis and visualization. We use the merged dataframe to create an interactive bar plot using Plotly.
# 

# In[18]:


# Make a copy of the dataframe
confirmed_df_oregon_copy = confirmed_df_oregon.copy()

# Calculate daily increases
confirmed_df_oregon_copy['Daily Increase'] = confirmed_df_oregon_copy[most_recent_date] - confirmed_df_oregon_copy[most_recent_date].shift(1)

# Plot daily increases
fig, ax = plt.subplots(figsize=(12,8))
confirmed_df_oregon_copy.plot(kind='bar', x='Admin2', y='Daily Increase', ax=ax)
plt.title('Daily Increase in Confirmed Cases by County')
plt.show()



# The following lines of code will create a new dataframe which will provide us the daily increase in the confirmed cases for each county. This will give us an idea about the daily growth of the COVID-19 virus in Oregon.
# We now plot a bar graph to visualize the daily increase in confirmed cases by county. This plot can give us a better understanding of how the virus is spreading on a daily basis.
# 

# In[19]:


import plotly.express as px
import pandas as pd
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

app = Dash(__name__)

# Melt the DataFrame to have dates in a separate column for confirmed cases
melted_df = confirmed_df_oregon.melt(id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
    'Country_Region', 'Lat', 'Long_', 'Combined_Key'], var_name='Date', value_name='Total Confirmed Cases')

# Clean up the DataFrame Melt the DataFrame to have dates in a separate column for confirmed cases
melted_df = melted_df[melted_df['Date'] != 'Population']
melted_df['Date'] = pd.to_datetime(melted_df['Date'])
melted_df.set_index('Date', inplace=True)

# Do the same for the deaths dataframe
deaths_melted_df = deaths_df_oregon.melt(id_vars=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State',
   'Country_Region', 'Lat', 'Long_', 'Combined_Key'], var_name='Date', value_name='Total Deaths')

#  Clean up the DataFrame and Melt the DataFrame to have dates in a separate column for death cases
deaths_melted_df = deaths_melted_df[deaths_melted_df['Date'] != 'Population']
deaths_melted_df['Date'] = pd.to_datetime(deaths_melted_df['Date'])
deaths_melted_df.set_index('Date', inplace=True)

# After melting both dataframes, we can merge them:
merged_df = pd.merge(melted_df, deaths_melted_df, on=['Date', 'Admin2'])


# Define app layout
app.layout = html.Div([
    html.H1("COVID-19 Cases Dashboard"),

    dcc.Dropdown(id='metric-dropdown',
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


# The next section is dedicated to preparing our data and building an interactive dashboard using Dash, a productive Python framework for building web applications. This will allow users to view the COVID-19 data dynamically based on their chosen parameters.
# 
# First, we need to reshape our data so that it suits the format we need for the interactive dashboard. We will do this using the melt function to transform our confirmed and death cases datasets into a long format where each row represents one observation per date.
# 
# With our data now ready, we can proceed to define the layout of our dashboard. It will consist of a dropdown menu for selecting the metric (confirmed cases or deaths), a date picker for selecting the date of interest, and a graph that will update based on the chosen parameters.
# 
# Finally, we define a callback function that will be triggered each time the user interacts with the dropdown menu
# 

# In[20]:


def df_quality_report(df):
    """Generates a quality report for a Pandas DataFrame"""
    quality_report = pd.DataFrame(index=[df.columns])

    quality_report['Dtype'] = df.dtypes.values
    quality_report['Total Values'] = len(df)
    quality_report['Unique Values'] = df.nunique().values
    quality_report['Missing Values'] = df.isnull().sum().values
    quality_report['% Missing Values'] = (df.isnull().sum() / len(df)) * 100

    # Only calculate min, max, mean, and median for numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for column in numeric_columns:
        quality_report.loc[column, 'Min'] = df[column].min()
        quality_report.loc[column, 'Max'] = df[column].max()
        quality_report.loc[column, 'Mean'] = df[column].mean()
        quality_report.loc[column, 'Median'] = df[column].median()

    return quality_report

# Generate the report
quality_report_merged = df_quality_report(merged_df)

# Display the report
print('Data Quality Report for Merged Data:')
display(quality_report_merged)


# ### Data Quality Report
# This data quality report provides an overview of the Total Confirmed Cases by County and Total Deaths by County datasets used in our COVID-19 analysis for Oregon.
# 
# #### Total Confirmed Cases by County
# This dataset contains information about the total confirmed COVID-19 cases for 38 counties in Oregon.
# 
# **Admin2 (County):** This is an object type field that contains the names of the counties. There are no missing values in this field, and each county name is unique.
# 
# **Total Confirmed Cases:** This is an integer type field that contains the total confirmed COVID-19 cases for each county. There are no missing values in this field. The number of confirmed cases ranges from a minimum of 0 to a maximum of 171,526. The average number of confirmed cases is approximately 25,356.95, with a median of 9,194.5 cases.
# 
# #### Total Deaths by County
# This dataset contains information about the total COVID-19 related deaths for the same 38 counties in Oregon.
# 
# **Admin2 (County):** Similar to the Confirmed Cases dataset, this is an object type field that contains the names of the counties. There are no missing values in this field, and each county name is unique.
# 
# **Total Deaths:** This is an integer type field that contains the total COVID-19 related deaths for each county. There are no missing values in this field. The number of deaths ranges from a minimum of 0 to a maximum of 1,480. The average number of deaths is approximately 246.66, with a median of 101.5 deaths.
# 
# For both datasets, the fact that there are no missing values implies that they are relatively clean and well-maintained. The wide range in the number of confirmed cases and deaths suggests a high variability in the impact of COVID-19 across different counties in Oregon. Further analysis could examine potential factors contributing to this variability.
# 
# This report provides a useful summary of the quality and characteristics of our data, helping inform subsequent analyses and ensure they are built on a reliable foundation.

# In[ ]:




