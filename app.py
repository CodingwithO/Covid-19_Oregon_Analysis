import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from data_processing import process_data
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

# Import the processed data from data_processing.py
processed_data = process_data()
confirmed_df_oregon = processed_data['confirmed']
deaths_df_oregon = processed_data['deaths']

# Identify the most recent date in the dataset
most_recent_date = confirmed_df_oregon.columns[-1]

# Create the Dash app
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
        min_date_allowed=pd.to_datetime(most_recent_date),
        max_date_allowed=pd.to_datetime(most_recent_date),
        initial_visible_month=pd.to_datetime(most_recent_date),
        date=pd.to_datetime(most_recent_date)
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
    filtered_df = confirmed_df_oregon[['Admin2', date]].rename(columns={date: 'Value'})
    fig = px.bar(filtered_df, x='Admin2', y='Value',
                 hover_data=['Value'],
                 labels={'Admin2': 'County', 'Value': metric},
                 title=f'{metric} on {date.strftime("%Y-%m-%d")}')
    fig.update_layout(autosize=False, width=1000, height=500, xaxis={'categoryorder': 'total descending'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
