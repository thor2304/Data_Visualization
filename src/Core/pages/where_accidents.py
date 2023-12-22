import dash
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.figure_factory as ff
import dash_bootstrap_components as dbc
import pandas as pd

from src.Core.CustomComponents import GraphDiv, CheckList
from src.Core.data_provider import get_df, get_category_orders
from src.Core.styles import graphStyle, dropdownStyle, legendColors, textTitleStyle, textStyle, labelStyle
from src.Core.styles import graphStyle, dropdownStyle, legendColors, textStyle, textTitleStyle, headerStyle

dash.register_page(__name__, name="3. Where do accidents happen?", order=3)

df = get_df()

eventsList = sorted(df["Event Type Group"].unique())

# The following dicts are used to map the index of the slider to a date.
inputMarks = {
    0: '2014-January', 1: '2014-February', 2: '2014-March', 3: '2014-April', 4: '2014-May', 5: '2014-June',
    6: '2014-July', 7: '2014-August', 8: '2014-September', 9: '2014-October', 10: '2014-November', 11: '2014-December',
    12: '2015-January', 13: '2015-February', 14: '2015-March', 15: '2015-April', 16: '2015-May', 17: '2015-June',
    18: '2015-July', 19: '2015-August', 20: '2015-September', 21: '2015-October', 22: '2015-November',
    23: '2015-December', 24: '2016-January', 25: '2016-February', 26: '2016-March', 27: '2016-April', 28: '2016-May',
    29: '2016-June', 30: '2016-July', 31: '2016-August', 32: '2016-September', 33: '2016-October', 34: '2016-November',
    35: '2016-December', 36: '2017-January', 37: '2017-February', 38: '2017-March', 39: '2017-April', 40: '2017-May',
    41: '2017-June', 42: '2017-July', 43: '2017-August', 44: '2017-September', 45: '2017-October', 46: '2017-November',
    47: '2017-December', 48: '2018-January', 49: '2018-February', 50: '2018-March', 51: '2018-April', 52: '2018-May',
    53: '2018-June', 54: '2018-July', 55: '2018-August', 56: '2018-September', 57: '2018-October', 58: '2018-November',
    59: '2018-December', 60: '2019-January', 61: '2019-February', 62: '2019-March', 63: '2019-April', 64: '2019-May',
    65: '2019-June', 66: '2019-July', 67: '2019-August', 68: '2019-September', 69: '2019-October', 70: '2019-November',
    71: '2019-December', 72: '2020-January', 73: '2020-February', 74: '2020-March', 75: '2020-April', 76: '2020-May',
    77: '2020-June', 78: '2020-July', 79: '2020-August', 80: '2020-September', 81: '2020-October', 82: '2020-November',
    83: '2020-December', 84: '2021-January', 85: '2021-February', 86: '2021-March', 87: '2021-April', 88: '2021-May',
    89: '2021-June', 90: '2021-July', 91: '2021-August', 92: '2021-September', 93: '2021-October', 94: '2021-November',
    95: '2021-December', 96: '2022-January', 97: '2022-February', 98: '2022-March', 99: '2022-April', 100: '2022-May',
    101: '2022-June', 102: '2022-July', 103: '2022-August', 104: '2022-September', 105: '2022-October',
    106: '2022-November', 107: '2022-December'
}
months = {
    0: "January", 1: "February", 2: "March", 3: "April", 4: "May", 5: "June", 6: "July", 7: "August",
    8: "September", 9: "October", 10: "November", 11: "December"
}

colorBarColors = [
    legendColors[4],
    legendColors[0],
    legendColors[2],
    legendColors[3],
]

colorSteps = [0.01, 0.1, 0.3]

layout = html.Div([
    html.H1('Do certain types of accidents occur more often in certain environments?',
            style=headerStyle),
    # html.P(children="To find out if certain types of accidents happen more often in certain environments or states. "
    #                 "I was chosen to create a Hexbin Mapbox for creating a map, "
    #                 "that is divided into hexagons and colored by the number of accidents in the area of the hexagon. ",
    #        style=textStyle),

    html.H3(children="Where on the map does the most accidents happen?", style=textTitleStyle),
    html.P(children="From the Map below, it is clear that around the large cities there are many accidents. "
                    "For example, the hexagons around New York and Washington are purple, "
                    "which indicates the highest number of accidents. "
                    "The orange hexagons around Las Vegas and Phoenix,"
                    "indicate that there are fewer accidents in these areas. ",
           style=textStyle),
    html.P(children="The colorscale for this chart is a binned colorscale, as can be seen on the right. "
                    "The bins are not evenly distributed, "
                    "since the difference between the number of accidents in the "
                    "largest cities far exceeds that of the more sparsely populated ares.",
           style=textStyle),
    html.P(children=["Turning the number of hexbins up to ",
                     dbc.Button(
                         "1000", outline=True, color="secondary", size="sm", id="hexagon-size-button"
                     ),
                     ", ",
                     "reveals some interesting details about the underlying data. "
                     "For instance, we dont have a single recorded incident in the entire state of "
                     "South Dakota or Wyoming. "
                     "It is unlikely that these states have gone entirely without accidents for 9 years. "
                     "A possible explanation for this is that the data comes from only public transit, and these states "
                     "have a very low population density. So the transit options might be limited. "],
           style=textStyle),
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
    html.H3(["Which states have the highest relative share of ",
             html.B("Accident type", id="accident-type-indicator-text"),
             " events?"],
            style=textTitleStyle),
    html.P(children=["We wanted to see if different states had a different makeup of accidents compared to each other. "
                     "Below we have calculated how much each Event Type makes up,"
                     " out of the total events that happened in the state. "
                     "The 10 states that have the highest percentage for the chosen event type are shown in the chart. ",
                     "We can see that 4 states, have only reported ",
                     dbc.Button(
                         "Collisions", outline=True, color="secondary", size="sm", id="collisions-button"
                     ), " and no other event types for all 9 years. "
                        "This provides further insight to the data, "
                        "since it is unlikely that these states have only had collisions. "
                        "This is most likely caused by the reporting agencies from these states, "
                        "only reporting collisions."],
           style=textStyle),
    html.P(children="The bar chart represents the percentage of accidents per state, "
                    "and is colored based on the selected accident type. "
                    "You can chose the event type by clicking the radio buttons "
                    "in the left side of the screen. ",
           style=textStyle),
    GraphDiv(
        left_of_graph=[
            html.H3(children="Choose event type", style={'textAlign': 'center', 'padding-top': 20}),
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

    # HORIZONTAL BAR GRAPH #########################################################
    html.H3(children="What states have reported the most accidents, per capita?", style=textTitleStyle),
    html.P(
        children="Up to now, we have seen that the amount of events per year varies a lot between the different event types. "
                 "Generally, collisions and assaults are the most common event types, while the other event types are less common. "
                 "The goal with the following horizontal bar graph is to see if some event types are more common in certain states. "
                 "The graph is sorted in descending order based on the amount of events in the chosen period.",
        style=textStyle),
    html.P(children="Using the slider below, a specific year or a range of years can be selected, "
                    "which in return will be visualized in the graph.",
           style={'width': '40%', 'padding-bottom': 20}),
    GraphDiv(
        graph=html.Div([
            dcc.RangeSlider(
                min=0,
                max=9 * 12 - 1,  # - 1 because the index starts at 0
                step=1,
                marks={0: '2014-January', 12: '2015-January', 24: '2016-January', 36: '2017-January',
                       48: '2018-January',
                       60: '2019-January', 72: '2020-January', 84: '2021-January', 96: '2022-January',
                       107: '2022-December'
                       },
                value=[48, 60],
                id='horizontal-bar-graph-slider',
            ),
            dcc.Graph(id='horizontal-bar-graph', style=graphStyle),
        ]),
    )

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
    Output('hexagon-size', 'value'),
    Output('hexagon-size-button', 'n_clicks'),
    Input('hexagon-size-button', 'n_clicks'),
    Input('hexagon-size', 'value')
)
def update_hexbin_to_large(n_clicks: int, existing_value: int)-> tuple[int, int]:
    if n_clicks is None or n_clicks == 0:
        return existing_value, 0
    return 1000, 0


@callback(
    Output('bar_event_type', 'value'),
    Output('collisions-button', 'n_clicks'),
    Input('collisions-button', 'n_clicks'),
    Input('bar_event_type', 'value')
)
def update_to_collisions(n_clicks: int, existing_value: str)-> tuple[str, int]:
    if n_clicks is None or n_clicks == 0:
        return existing_value, 0
    return "Collision", 0


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
        p_tags[1]["props"]["children"][1] = f"{int(stops[i])}"
        p_tags[0]["props"]["children"][1] = f"{int(stops[i + 1])}"
    return children


@callback(
    Output('accident-map', 'figure'),
    Input('hexagon-size', 'value'),
    Input('map-event-checklist', 'value')
)
def update_map(value: int, event_type: str) -> Figure:
    mask = df['Event Type Group'].isin(event_type) & df['Latitude'].notna() & df['Longitude'].notna()
    active_rows = df[mask]

    # Drop rows where latitude is above 90
    active_rows = active_rows[active_rows['Latitude'] < 90]

    # Drop rows where longitude is higher than -45
    active_rows = active_rows[active_rows['Longitude'] < -45]

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

    fig.update_traces(
        hovertemplate='<b>%{z}</b> accidents in the area' +
                      '<extra></extra>',
    )

    fig.update_layout(
        hoverlabel=labelStyle,
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
    alabama_df = alabama_df.groupby(["Event Type Group"], as_index=False).agg(
        {"Percentage of accidents in state": "sum"})
    print(alabama_df)

    # get top 10 states with the highest percentage of accidents for the selected event type out of all event types
    grouped_df = newDf.groupby(["State", "Event Type Group"], as_index=False).agg(
        {"Percentage of accidents in state": "sum"})
    grouped_df = grouped_df.sort_values("Percentage of accidents in state", ascending=False)
    grouped_df = grouped_df[grouped_df["Event Type Group"] == bar_event_type]
    grouped_df = grouped_df.head(10)

    fig = px.bar(grouped_df, x="State", y="Percentage of accidents in state", color='Event Type Group',
                 category_orders=get_category_orders(),
                 color_discrete_sequence=legendColors,
                 orientation='v',
                 )

    fig.update_yaxes(ticksuffix="%")

    # Hover settings for the graph
    fig.update_traces(
        hovertemplate='<b>%{data.name}</b> represents <b>%{y:.2f}%</b> of all the accidents in the state <b>%{x}</b>' +
                      '<extra></extra>',
    )

    fig.update_layout(
        hoverlabel=labelStyle,
    )

    return fig


@callback(
    Output('accident-type-indicator-text', 'children'),
    Input('bar_event_type', 'value'),
)
def update_accident_type_text(y_selection: str) -> str:
    return y_selection


# Horizontal bar graph #########################################################
@callback(
    Output('horizontal-bar-graph', 'figure'),
    Input('horizontal-bar-graph-slider', 'value')
)
def update_horizontal_bar_graph(value) -> Figure:
    # Get Year and month from the two values in value
    # The first value is the start date
    # The second value is the end date
    year1 = int(inputMarks[value[0]].split("-")[0])
    month1 = inputMarks[value[0]].split("-")[1]
    year2 = int(inputMarks[value[1]].split("-")[0])
    month2 = inputMarks[value[1]].split("-")[1]

    # Map month 1 and month2 to the month number
    month1 = list(months.keys())[list(months.values()).index(month1)] + 1
    month2 = list(months.keys())[list(months.values()).index(month2)] + 1

    date_start = pd.Timestamp(year=year1, month=month1, day=1, hour=0, minute=0, second=0)

    # subtract 1 nano second from dateEnd to get the last day of the month. This does not work for the last month of the year
    if month2 == 12:
        date_end = pd.Timestamp(year=year2, month=month2, day=31, hour=23, minute=59, second=59)
    else:
        date_end = pd.Timestamp(year=year2, month=month2 + 1, day=1, hour=0, minute=0, second=0) - pd.Timedelta(
            nanoseconds=1)

    # Filter the df so only the rows within dateStart and dateEnd are left
    mask = (df['Event Date'] >= date_start) & (df['Event Date'] <= date_end)
    active_rows = df[mask]

    fig = px.histogram(active_rows, x="Event Per Mil Citizens", y="State", color='Event Type Group', orientation='h',
                       height=1200,
                       title="Years chosen by slider " + inputMarks[value[0]] + " to " + inputMarks[value[1]],
                       category_orders=get_category_orders(),
                       color_discrete_sequence=legendColors)

    # Sort in descending order
    fig.update_yaxes(
        categoryorder="total ascending",
        title_text="States"
    )

    # Hover settings for the graph
    fig.update_traces(
        hovertemplate='<b>%{data.name}</b><br>' +
                      '<b>Event Per Mil Citizens:</b> %{x:.2f}<br>' +
                      '<extra></extra>',
    )

    fig.update_layout(
        hovermode='y unified',
        bargap=0.3,
    )

    return fig
