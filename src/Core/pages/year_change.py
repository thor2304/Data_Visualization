from typing import Tuple

import dash
import numpy as np
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import united_states

from src.Core.data_provider import get_df
from src.Core.styles import graphStyle, dropdownStyle

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

dash.register_page(__name__, name="Do more happen every year?")

df = get_df()

# List for Event Graph
eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))

layout = html.Div([
    html.Div([
        html.H1(children="Is there an increase or decrease in certain types of accidents in the last 9 years?",
                style={'textAlign': 'center'}),
        # BAR GRAPH
        html.H3(children="Graph showing amount of events", style={'textAlign': 'center'}),
        dcc.Graph(id='bar-event-graph', style=graphStyle),

        # EVENT GRAPH
        html.H3(children="Events per year", style={'textAlign': 'center'}),
        dcc.Dropdown(eventsList, 'Collision', id='event-dropdown-selection', style=dropdownStyle),
        dcc.Graph(id='event-graph', style=graphStyle),

        # HORIZONTAL BAR GRAPH
        html.H3(children="Horizontal bar graph", style={'textAlign': 'center'}),
        dcc.RangeSlider(
            min=0,
            max=9 * 12 - 1,  # - 1 because the index starts at 0
            step=1,
            marks={0: '2014-January', 12: '2015-January', 24: '2016-January', 36: '2017-January', 48: '2018-January',
                   60: '2019-January', 72: '2020-January', 84: '2021-January', 96: '2022-January', 107: '2022-December'
                   },
            value=[49, 60],
            id='horizontal-bar-graph-slider',
        ),
        dcc.Graph(id='horizontal-bar-graph', style=graphStyle),

    ], style={'width': '60%'}),
], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}, )


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
    Input('bar-event-graph', 'figure')
)
def update_bar_event_graph(value: str) -> Figure:
    # Y akse baby
    y_akse = pd.DataFrame()
    temp_data = df['Event Type Group'].value_counts().sort_index()
    temp_data.drop('Non-RGX Collision', inplace=True)  # Remove Non-RGX Collision from list
    y_akse['Event Type Group'] = temp_data.values

    # X akse baby
    x_akse_raw = df['Event Type Group'].unique()
    x_akse = np.delete(x_akse_raw, np.where(x_akse_raw == "Non-RGX Collision"))  # Remove Non-RGX Collision from list
    x_akse.sort()

    return px.bar(x=x_akse, y=y_akse['Event Type Group'])


## Horizontal bar graph
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
    print(f"month2: {month2}")
    if month2 == 12:
        date_end = pd.Timestamp(year=year2, month=month2, day=31, hour=23, minute=59, second=59)
    else:
        date_end = pd.Timestamp(year=year2, month=month2 + 1, day=1, hour=0, minute=0, second=0) - pd.Timedelta(
            nanoseconds=1)

    print(f"date_start: {date_start} date_end: {date_end}")

    # Filter the df so only the rows within dateStart and dateEnd are left
    mask = (df['Event Date'] >= date_start) & (df['Event Date'] <= date_end)
    active_rows = df[mask]

    fig = px.histogram(active_rows, x="Event Per Mil Citizens", y="State", color='Event Type Group', orientation='h',
                       height=1200,
                       title="Years chosen by slider " + inputMarks[value[0]] + " to " + inputMarks[value[1]])

    # Sort in descending order
    fig.update_yaxes(
        categoryorder="total ascending",
        title_text="States"
    )

    return fig
