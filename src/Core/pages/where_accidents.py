import dash
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.figure_factory as ff

from src.Core.data_provider import get_df
from src.Core.styles import graphStyle, dropdownStyle, legendColors

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

    fig = ff.create_hexbin_mapbox(
        data_frame=df,
        lat="Latitude",
        lon="Longitude",
        nx_hexagon=50,
        opacity=0.5,
        labels={"color": "Number of accidents"},
        color="Number of accidents",
        color_continuous_scale=[legendColors[4], legendColors[0], legendColors[2], legendColors[3]],
        mapbox_style="open-street-map",
        min_count=0,
        agg_func=np.sum,
        zoom=4,
        show_original_data=True,
        original_data_marker=dict(size=1, opacity=1, color="Navy"),
        center=dict(lat=38.92, lon=-99.07),
        range_color=[0, 200],

    )

    return fig
