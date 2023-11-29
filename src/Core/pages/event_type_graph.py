import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure
import numpy as np

from src.Core.main import df

# List for event-graph
eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))

dash.register_page(__name__)

layout = html.Div([
    html.H1('This is our Event type page'),
    html.Br(),
    html.H2(children="Graph showing amount of events", style={'textAlign': 'center'}),
    dcc.Dropdown(eventsList, 'Collision', id='event-dropdown-selection'),
    dcc.Graph(id='event-graph'),
])


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
