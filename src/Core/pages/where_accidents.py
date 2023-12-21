import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.figure_factory as ff

from src.Core.data_provider import get_df
from src.Core.styles import graphStyle, dropdownStyle

dash.register_page(__name__, name="Where do accidents happen?")

df = get_df()

layout = html.Div([
    html.Div([
        html.H1('Is there a relation between time periods in the day and certain types of accidents?',
                style={'textAlign': 'center'}),
        dcc.Graph(id='accident-map', style=graphStyle),
    ], style={'width': '60%'}),
], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}, )


@callback(
    Output('accident-map', 'figure'),
    Input('accident-map', 'figure')
)
def update_map(value: str) -> Figure:
    # Callbacks in Dash have to have an output and an input.
    # We don't use the input for this, but we need it to trigger the callback
    df = get_df()

    fig = ff.create_hexbin_mapbox(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        nx_hexagon=10,
        opacity=0.9,
        labels={"color": "Accident Count"},
    )

    px.set_mapbox_access_token(open(".mapbox_token").read())
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
