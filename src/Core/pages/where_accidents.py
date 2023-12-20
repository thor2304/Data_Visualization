import dash
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

from src.Core.CustomComponents import GraphDiv, CheckList
from src.Core.data_provider import get_df
from src.Core.styles import graphStyle, dropdownStyle, legendColors

dash.register_page(__name__, name="Where do accidents happen?")

df = get_df()

eventsList = sorted(df["Event Type Group"].unique())

layout = html.Div([
    html.H1('Do certain types of accidents occur more often in certain environments?',
                style={'textAlign': 'center'}),
    GraphDiv(
        left_of_graph=[
            dbc.Form([
                CheckList(title="Choose event types", options=eventsList, checklist_id="map-event-checklist"),
                html.H3(children="Adjust amount of hexagons",
                        style={'textAlign': 'center', 'padding-top': 20}),
                html.P(children="Adjusting the amount of hexagons to an amount higher than 200 can take time to load."),
                html.P(children="Additionally, the hexagons can be hard too see, so zooming in is recommended."),
                html.Div(
                    dbc.RadioItems(
                        options=[10, 20, 30, 40, 50, 200, 1000, 3000, 5000, 10000],
                        value=20,
                        id="hexagon-size",
                    ),
                    className="py-2",
                )])],
        graph=dcc.Graph(id='accident-map', style=graphStyle)

    ),
], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}, )


@callback(
    Output('accident-map', 'figure'),
    Input('hexagon-size', 'value'),
    Input('map-event-checklist', 'value')
)
def update_map(value: int, event_type: str) -> Figure:

    mask = df['Event Type Group'].isin(event_type)
    active_rows = df[mask]

    min_count = 0
    opacity_value = 0.2

    if value > 200:
        min_count = 1
        opacity_value = 0.5

    fig = ff.create_hexbin_mapbox(
        data_frame=active_rows,
        lat="Latitude",
        lon="Longitude",
        nx_hexagon=value,
        opacity=opacity_value,
        labels={"color": "Number of accidents"},
        color="Number of accidents",
        color_continuous_scale=[legendColors[4], legendColors[0], legendColors[2], legendColors[3]],
        mapbox_style="open-street-map",
        min_count=min_count,
        agg_func=np.sum,
        zoom=3.7,
        center=dict(lat=38.92, lon=-96),
        range_color=[0, 200],

    )



    return fig
