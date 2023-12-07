import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px


from src.Core.data_provider import get_df
from src.Core.styles import graphStyle, dropdownStyle

dash.register_page(__name__, name="Accident environments")

df = get_df()

layout = html.Div([
    html.Div([
        html.H1('Do certain types of accidents occur more often in certain environments?', style={'textAlign': 'center'}),
        dcc.Graph(id='environment-map', style=graphStyle),
    ], style={'width': '60%'}),
], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}, )



@callback(
    Output('environment-map', 'figure'),
    Input('environment-map', 'figure')
)
def update_map(value: str) -> Figure:
    # Callbacks in Dash have to have an output and an input.
    # We don't use the input for this, but we need it to trigger the callback
    return px.density_mapbox(df, lat='Latitude', lon='Longitude', radius=10,
                             center=dict(lat=36.6062, lon=-98.3321), zoom=4,
                             mapbox_style="open-street-map")