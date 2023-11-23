import os

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure

import united_states

us = united_states.UnitedStates()

print("fetch data")
if os.environ["fetch"] == "True":
    df = pd.read_csv('http://datadump.cryptobot.dk/Major_Safety_Events.csv', low_memory=False)
else:
    df = pd.read_csv('src/Core/data/cleaned_output.csv')
print("data fetched")
print(df.columns[35])


TITLE = 'Data Visualizations incoming'

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1(children=TITLE, style={'textAlign': 'center'}),
    dcc.Dropdown(df.Agency.unique(), 'Metro Transit', id='dropdown-selection'),
    dcc.Graph(id='graph-content', style={'width': '100%', 'height': '60em'}),
    html.H1(children="Map of all accidents", style={'textAlign': 'center'}),
    dcc.Graph(id='accident-map', style={'width': '100%', 'height': '60em'}),
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value: str) -> Figure:
    country_data = df[df.Agency == value]
    return px.scatter(country_data, x='Year', y='Total Serious Injuries', labels={
        "Agency": "agency",
        "Year": "years",
    })


@callback(
    Output('accident-map', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_map(value: str) -> Figure:
    # Callbacks in Dash have to have an output and an input.
    # We don't use the input for this, but we need it to trigger the callback
    return px.density_mapbox(df, lat='Latitude', lon='Longitude', radius=10,
                             center=dict(lat=36.6062, lon=-98.3321), zoom=4,
                             mapbox_style="open-street-map")


def main():
    print(df)
    print(df.columns)
    # print(us.from_coords(36.6062, -98.3321)[0])
    app.run(debug=True, host="127.0.0.1", port=8070)


if __name__ == '__main__':
    main()
