import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure
import numpy as np
import united_states

from src.Core.styles import graphStyle, dropdownStyle
from src.Core.data_provider import get_df

dash.register_page(__name__,  path='/', name="Introduction")

us = united_states.UnitedStates()

TITLE = 'Data Visualizations incoming'
Questions = {
    "1": "Is there a relation between time periods in the day and certain types of accidents?",
    "2": "Is there an increase or decrease in certain types of accidents in the last 9 years?",
    "3": "Do certain types of accidents occur more often in certain environments?"
}

df = get_df()

# List for Event Graph
eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))


layout = html.Div([
    html.Div([
        # TITLE
        html.H1(children=TITLE, style={'textAlign': 'center'}),
        html.Br(),


        # QUESTION 2
        html.H2(children=Questions.get("2"), style={'textAlign': 'center'}),
        # BAR GRAPH
        html.H3(children="Graph showing amount of events", style={'textAlign': 'center'}),
        dcc.Graph(id='bar-event-graph', style=graphStyle),
        # EVENT GRAPH
        html.H3(children="Events per year", style={'textAlign': 'center'}),
        dcc.Dropdown(eventsList, 'Collision', id='event-dropdown-selection', style=dropdownStyle),
        dcc.Graph(id='event-graph', style=graphStyle),

        # SOME GRAPH
        html.H2(children=Questions.get("3"), style={'textAlign': 'center'}),
    ], style={'width': '60%'}),
],
    style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
)


# EVENT GRAPH #################################################################
@callback(
    Output('event-graph', 'figure'),
    Input('event-dropdown-selection', 'value')
)
def update_event_graph(value: str) -> Figure:
    # Create list from year column
    list_of_years = df['Year'].unique().tolist()
    list_of_years.sort()

    # Create new dataframe to store data
    out = pd.DataFrame()

    # Add year column from original data starting from the lowest year to highest
    out['Year'] = list_of_years

    # Calculate number of events per year one event type
    counts = df[df['Event Type Group'] == value]['Year'].value_counts()
    counts.sort_index(inplace=True, ascending=True)

    # Add event type column to new dataframe
    out[value] = counts.values

    return px.line(out, x='Year', y=value, markers=True, labels={
        value: "Amount of events",
        "Year": "Years",
    })


# BAR GRAPH #################################################################
@callback(
    Output('bar-event-graph', 'figure'),
    Input('bar-event-graph', 'figure')
)
def update_bar_event_graph(value: str) -> Figure:
    # Y akse baby
    y_akse = pd.DataFrame()
    temp_data = df['Event Type Group'].value_counts().sort_index()
    temp_data.drop('Non-RGX Collision', inplace=True)  # Remove Non-RGX Collision from list
    y_akse['Event Type Group'] = temp_data.values

    # X akse baby
    x_akse_raw = df['Event Type Group'].unique()
    x_akse = np.delete(x_akse_raw, np.where(x_akse_raw == "Non-RGX Collision"))  # Remove Non-RGX Collision from list
    x_akse.sort()

    return px.bar(x=x_akse, y=y_akse['Event Type Group'])



