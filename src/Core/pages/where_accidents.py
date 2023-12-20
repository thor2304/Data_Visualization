import dash
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc

from src.Core.CustomComponents import GraphDiv, CheckList
from src.Core.data_provider import get_df, get_category_orders
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
                html.Div(children=[
                    html.Div(style={'width': '2em', "height": "4em", "background-color": color}),
                    html.Div(children=[
                        html.P(["- ", "top"]),
                        html.P(["- ", "bottom"])
                    ], style={"height": "4em", "padding-left": ".2em", "width": "fit-content", "text-align": "left",
                              "display": "flex",
                              "justify-content": "space-between", "align-items": "left", "flex-direction": "column"})
                ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'padding': '.5em'})
                for color in reversed(colorBarColors)
            ], id="color-bar", style={"width": "fit-content"})
        ]

    ),
    GraphDiv(
        left_of_graph=[
            html.Div(
                dbc.RadioItems(
                    options=eventsList,
                    value=eventsList[0],
                    id="bar_event_type",
                ),
                className="py-2",
            )
        ],
        graph=dcc.Graph(id='top10-bar', style=graphStyle)),
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
        p_tags = child["props"]["children"][1]["props"]["children"]
        p_tags[1]["props"]["children"][1] = f"{stops[i]}"
        p_tags[0]["props"]["children"][1] = f"{stops[i + 1]}"
    return children


@callback(
    Output('accident-map', 'figure'),
    Input('hexagon-size', 'value'),
    Input('map-event-checklist', 'value')
)
def update_map(value: int, event_type: str) -> Figure:
    mask = df['Event Type Group'].isin(event_type) & df['Latitude'].notna() & df['Longitude'].notna()
    active_rows = df[mask]
    print(f"Number of rows: {len(active_rows)}")
    # Drop rows where latitude is above 90
    active_rows = active_rows[active_rows['Latitude'] < 90]

    # Drop rows where longitude is higher than -45
    active_rows = active_rows[active_rows['Longitude'] < -45]
    print(f"Number of rows after dropping: {len(active_rows)}")

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


@callback(
    Output('top10-bar', 'figure'),
    Input('bar_event_type', 'value')
)
def update_bar(bar_event_type: str) -> Figure:
    # Remove Unknown from the dataframe

    # Create a mask to remove all rows where the event type is unknown
    mask = (df['Event Type Group'] != "Unknown")
    newDf = df[mask]
    print(newDf)

    # sum the percentage of accidents in Alabame for each event type
    alabama_df = newDf[newDf["State"] == "Louisiana"]
    alabama_df = alabama_df.groupby(["Event Type Group"], as_index=False).agg({"Percentage of accidents in state": sum})
    print(alabama_df)

    # get top 10 states with the highest percentage of accidents for the selected event type out of all event types
    grouped_df = newDf.groupby(["State", "Event Type Group"], as_index=False).agg({"Percentage of accidents in state": sum})
    grouped_df = grouped_df.sort_values("Percentage of accidents in state", ascending=False)
    grouped_df = grouped_df[grouped_df["Event Type Group"] == bar_event_type]
    grouped_df = grouped_df.head(10)

    fig = px.bar(grouped_df, x="State", y="Percentage of accidents in state", color='Event Type Group',
                 category_orders=get_category_orders(),
                 color_discrete_sequence=legendColors,
                 orientation='v',
                 )

    fig.update_yaxes(ticksuffix="%")



    return fig
