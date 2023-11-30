import os
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure
import numpy as np
import united_states

us = united_states.UnitedStates()

print("fetch data")
if os.environ["fetch"] == "True":
    df = pd.read_csv('http://datadump.cryptobot.dk/Major_Safety_Events.csv', low_memory=False)
else:
    filename = f"{__file__[:-7]}data/cleaned_output.csv"
    df = pd.read_csv(filename)
    # df.apply(lambda x: x['Event Date'].format(name=x['name']), axis=1)
    df['Event Date'] = pd.to_datetime(df['Event Date'])
    df['Event Time'] = pd.to_datetime(df['Event Time'])
print("data fetched")
print(df.columns[12])
print(df["Event Time"])


TITLE = 'Data Visualizations incoming'
Questions = {
    "1": "Is there a relation between time periods in the day and certain types of accidents?",
    "2": "Is there an increase or decrease in certain types of accidents in the last 9 years?",
    "3": "Do certain types of accidents occur more often in certain environments?"
}

app = Dash(__name__)

server = app.server

# List for Event Graph
eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))

graphStyle = {'height': '60em'}
dropdownStyle = {}

app.layout = html.Div([
        html.Div([
            # TITLE
            html.H1(children=TITLE, style={'textAlign': 'center'}),
            html.Br(),
            # Link
            html.A("Link to slides", href="https://docs.google.com/presentation/d/1fhCPoXRcuAyMtLtjcIDdk0Hj8GH-Az2udhRZHSXvx28/edit?usp=sharing", target="_blank"),

            # 3D GRAPH
            html.H2(children=Questions.get("1"), style={'textAlign': 'center'}),
            dcc.Dropdown(df["Rail/Bus/Ferry"].unique(), 'Bus', id='3d-dropdown-selection', style=dropdownStyle),
            dcc.Graph(id='3d-graph', style=graphStyle),

            # MAP
            html.H2(children="Map of all accidents", style={'textAlign': 'center'}),
            dcc.Graph(id='accident-map', style=graphStyle),

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

# 3D GRAPH ###################################################################
@callback(
    Output('3d-graph', 'figure'),
    Input('3d-dropdown-selection', 'value')
)
def update_3d_plot(value: str) -> Figure:
    category_data = df[df["Rail/Bus/Ferry"] == value]
    marker_size = 3

    fig = px.scatter_3d(category_data, x='Event Date', y='Event Time', z='Total Injuries', labels={
        "Agency": "agency",
        "Year": "years",
    }, color="Total Injuries")

    fig.update_traces(marker=dict(
        size=marker_size
    ), selector=dict(mode="markers"))

    return fig

# MAP ########################################################################
@callback(
    Output('accident-map', 'figure'),
    Input('3d-dropdown-selection', 'value')
)
def update_map(value: str) -> Figure:
    # Callbacks in Dash have to have an output and an input.
    # We don't use the input for this, but we need it to trigger the callback
    return px.density_mapbox(df, lat='Latitude', lon='Longitude', radius=10,
                             center=dict(lat=36.6062, lon=-98.3321), zoom=4,
                             mapbox_style="open-street-map")

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
    Input('3d-dropdown-selection', 'value')
)
def update_bar_event_graph(value: str) -> Figure:

    # Y akse baby
    y_akse = pd.DataFrame()
    temp_data = df['Event Type Group'].value_counts().sort_index()
    temp_data.drop('Non-RGX Collision', inplace=True) # Remove Non-RGX Collision from list
    y_akse['Event Type Group'] = temp_data.values

    # X akse baby
    x_akse_raw = df['Event Type Group'].unique()
    x_akse = np.delete(x_akse_raw, np.where(x_akse_raw == "Non-RGX Collision")) # Remove Non-RGX Collision from list
    x_akse.sort()

    return px.bar(x=x_akse, y=y_akse['Event Type Group'])

def main():
    app.run(debug=True, host="127.0.0.1", port=8070)

if __name__ == '__main__':
    main()
