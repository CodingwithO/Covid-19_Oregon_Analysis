import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

# Import the processed data from data_processing.py
from data_processing import process_data_chunks

# Generate the Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("COVID-19 Cases Dashboard"),

    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Total Confirmed Cases', 'value': 'confirmed'},
            {'label': 'Total Deaths', 'value': 'deaths'}
        ],
        value='confirmed',
        style={"width": "50%"}
    ),

    dcc.DatePickerSingle(
        id='date-picker',
        min_date_allowed='2023-02-15',
        max_date_allowed='2023-03-09',
        initial_visible_month='2023-03-09',
        date='2023-03-09'
    ),

    dcc.Graph(id='covid-graph'),

], style={"padding": "20px"})

@app.callback(
    Output('covid-graph', 'figure'),
    Input('metric-dropdown', 'value'),
    Input('date-picker', 'date')
)
def update_graph(metric, date):
    data = process_data_chunks()
    filtered_df = data[metric]
    fig = px.bar(filtered_df, x='Admin2', y=date,
                 hover_data=[date],
                 labels={'Admin2': 'County', date: metric.capitalize()},
                 title=f'{metric.capitalize()} on {date}')
    fig.update_layout(autosize=False, width=1000, height=500, xaxis={'categoryorder': 'total descending'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
