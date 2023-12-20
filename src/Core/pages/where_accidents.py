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

colorBarColors = [
    legendColors[4],
    legendColors[0],
    legendColors[2],
    legendColors[3],
]

colorSteps = [0.01, 0.1, 0.3]

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
        graph=dcc.Graph(id='accident-map', style=graphStyle),
        right_of_graph=[
            html.Div([
                html.P(children="", style={'padding': '2em', "width": "100%", "background-color": color})
                for color in reversed(colorBarColors)
            ], id="color-bar", style={"width": "fit-content"})
        ]

    ),
], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}, )


def discrete_colorscale(breakpoints=None, discrete=True):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex color codes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns a nonuniform   discrete colorscale
    """
    if breakpoints is None:
        breakpoints = [0, 1]

    if len(breakpoints) != len(colorBarColors) - 1:
        raise ValueError("Breakpoints must be same length as colors")

    out = [
        [0, colorBarColors[0]],
    ]

    if discrete:
        out.append([breakpoints[0], colorBarColors[0]])

    for k in range(1, len(breakpoints)):
        col = colorBarColors[k]

        colorstop = breakpoints[k - 1]
        out.append([colorstop, col])

        if discrete:
            colorstop = breakpoints[k]
            out.append([colorstop, col])

    if discrete:
        out.append([breakpoints[-1], colorBarColors[-1]])

    out.append([1, colorBarColors[-1]])

    return out


@callback(
    Output('color-bar', 'children'),
    Input('color-bar', 'children'),
    Input('accident-map', 'figure'),
)
def update_colorscale(children, figure):
    min = figure["layout"]["coloraxis"]["cmin"]
    max = figure["layout"]["coloraxis"]["cmax"]

    stops = [min]

    for step in colorSteps:
        stops.append(min + step * (max - min))

    stops.append(max)

    for i, child in enumerate(reversed(children)):
        child["props"]["children"] = f"{stops[i]} - {stops[i + 1]}"
    return children


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
        color_continuous_scale=discrete_colorscale(colorSteps, True),
        mapbox_style="open-street-map",
        min_count=min_count,
        agg_func=np.sum,
        zoom=3.7,
        center=dict(lat=38.92, lon=-96),
        # range_color=[0, 200],
    )

    return fig
