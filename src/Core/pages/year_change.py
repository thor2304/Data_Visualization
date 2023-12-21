import trace

import dash
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Output, Input
from plotly.graph_objs import Figure

from src.Core.CustomComponents import GraphDiv, CheckList
from src.Core.data_provider import get_df, get_category_orders
from src.Core.styles import graphStyle, pageStyle, textStyle, textTitleStyle, labelStyle, legendColors

dash.register_page(__name__, name="1. Do more happen every year?", order=1)

df = get_df()

# The different types of events. Used to create the checklist
eventsList = sorted(df["Event Type Group"].unique())
# statesList without Unknown
statesListRaw = df["State"].unique()
statesList = np.delete(statesListRaw, np.where(statesListRaw == "Unknown"))

layout = html.Div([
    html.H1(children="Is there an increase or decrease in certain types of accidents in the last 9 years?",
            style={'textAlign': 'center', 'padding-bottom': 20, 'padding-top': 50}),
    html.P(children="To answer this question, the page contains three different graphs. "
                    "The first graph is a doughnut chart, which shows the amount of events in the period 2014-2022. "
                    "The second graph is a line graph, which shows the amount of events per year for each event type. "
                    "This graph highlights the evolution of the different event types over the years. "
                    "The third graph is as well a line chart. However, this line chart builds upon the second graph, "
                    "by showing the amount of events per state over the years. ",
           style=textStyle),

    # PIE CHART #####################################################################
    html.H3(children="Amount of events in the period 2014-2022", style=textTitleStyle),
    html.P(children="The amount of events in the period 2014-2022, is shown through a doughnut chart. "
                    "The doughnut chart aims at visualizing the amount of events for each event type."
                    "This should result in a clear overview of the amount of events for each event type. ",
           style=textStyle),
    html.P(children="From the doughnut chart it is clear that collisions and assaults are the most common event types. "
                    "The other event types are rare compared to collisions and assaults. "
                    "The event types Security and Other may not be as clear as the other event types in the context of what they include. "
                    "The event type Security includes events such as bomb threats, hijackings and random gun fire. "
                    "The event type Other includes events such as people falling, people getting sick and people getting lost. ",
           style=textStyle),
    GraphDiv(graph=dcc.Graph(id='bar-event-graph', style=graphStyle)),

    # EVENT GRAPH ###################################################################
    html.H3(children="Events per year", style=textTitleStyle),
    html.P(
        children="To visualize the evolution of the amount of different accidents per year, line graphs were created. "
                 "The line graphs show the amount of events per year for each event type. "
                 "On the left side of the graph the different Event Types can be selected. ",
        style=textStyle),
    html.P(children="Since the amount of events per year varies a lot between the different event types, "
                    "the data can be normalised. "
                    "Normalising the data means that the different Event Types are indexed to the first year. ",
           style=textStyle),
    GraphDiv(
        left_of_graph=[
            CheckList(title="Choose event types", options=eventsList, checklist_id="event-checklist"),
            dbc.Form([
                html.H3(children="Choose whether to normalise data",
                        style={'textAlign': 'center', 'padding-top': 20}),
                html.P(children="Relative to the accidents in 2014"),
                html.Div(
                    dbc.RadioItems(
                        options=["Don't normalise data", "Normalise data", ],
                        value="Don't normalise data",
                        id="event-normaliser",
                    ),
                    className="py-2",
                )])],
        graph=dcc.Graph(id='event-graph', style=graphStyle),
        # right_of_graph=[html.H1('', style={'textAlign': 'center '})]
    ),

    # LINE CHART WITH STATES #########################################################
    html.H3(children="Events per state", style=textTitleStyle),
    html.P(
        children="The following horizontal bar graph shows the amount of events per state for a specific year or "
                 "a range of years. ",
        style=textStyle),
    GraphDiv(
        left_of_graph=[
            html.H3(children="Choose event type", style={'textAlign': 'center'}),
            dcc.Dropdown(eventsList, eventsList[0], id='state-line-chart-event-selection',
                         style={'width': '100%', 'justify-content': 'end', 'margin-bottom': '2em'}, clearable=False),
            html.H3(children="Choose whether to normalise data", style={'textAlign': 'center'}),
            html.Div(
                    dbc.RadioItems(
                        options=["Don't normalise data", "Normalise data", ],
                        value="Don't normalise data",
                        id='state-line-chart-normaliser',
                    ),
                    className="py-2",
                ),
            CheckList("Choose states", statesList[:18], 'state-line-chart-state-selection', True),
        ],
        graph=dcc.Graph(id='state-line-chart', style=graphStyle),
        right_of_graph=[dbc.Form([
            CheckList("Choose States", statesList[18:], 'state-line-chart-state-selection2', True),
        ])]
    )
], style=pageStyle)


# EVENT GRAPH #################################################################
@callback(
    Output('event-graph', 'figure'),
    Input('event-checklist', 'value'),
    Input('event-normaliser', 'value')
)
def update_event_graph(value: list[str], value2: str) -> Figure:
    labels = {
        "Year": "Years",
        "Amount of Events": "Amount of events",
    }

    # Mask to get active rows dependendt on input value
    mask = df['Event Type Group'].isin(value)
    active_rows = df[mask]

    # Get amount of events per year per event type
    active_rows = active_rows.groupby(['Year', 'Event Type Group']).size().reset_index(name='Amount of Events')

    # If normalise is true the data should visualize how much each event type increases/decreases each year
    # Each event type should be indexed to the first year. This means that the first year should be 100%
    # Then next year should be divided by the first year and multiplied by 100 to get the percentage increase/decrease
    if value2 == "Normalise data":
        labels["Amount of Events"] = "Percentage increase/decrease"

        # Get the first year for each event type
        first_year = active_rows.groupby(['Event Type Group'])['Amount of Events'].transform('first')

        # Divide the amount of events for each year by the first year and multiply by 100
        active_rows['Amount of Events'] = active_rows['Amount of Events'] / first_year * 100

    fig = px.line(
        active_rows,
        x="Year",
        y="Amount of Events",
        color="Event Type Group",
        labels=labels,
        category_orders=get_category_orders(),
        color_discrete_sequence=legendColors,
    )

    fig.add_annotation(x=2020, y=0.5,
                       yref="paper",
                       text="Covid 19 lockdown in 2020",
                       bgcolor="rgba(255, 255, 255, 0.8)",
                       showarrow=False,
                       arrowhead=1)

    if value2 == "Normalise data":
        fig.update_yaxes(ticksuffix="%")
    else:
        fig.update_yaxes(autorangeoptions_include=[0])

    # Hover settings for the graph
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate='<b>%{data.name}:</b> %{y}<br>' +
                      '<extra></extra>',
    )

    fig.update_xaxes(dtick=1)

    fig.update_layout(
        hoverlabel=labelStyle,
        hoverdistance=20,
        hovermode='x unified',
    )

    return fig


# PIE CHART #################################################################
@callback(
    Output('bar-event-graph', 'figure'),
    Input('bar-event-graph', 'style')
)
def update_bar_event_graph(_: Figure) -> Figure:
    fig = px.pie(df, names="Event Type Group", color="Event Type Group", category_orders=get_category_orders(),
                 color_discrete_sequence=legendColors, hole=0.65)

    # Hover settings for the graph
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>' +
                      '<b>Amount of events:</b> %{value}<br>' +
                      '<b>Percentage of all events:</b> %{percent}<br>' +
                      '<extra></extra>',
        textfont_size=14,
    )

    fig.update_layout(
        hoverlabel=labelStyle,
    )

    return fig


# LINE CHART WITH STATES #########################################################
@callback(
    Output('state-line-chart', 'figure'),
    Input('state-line-chart-event-selection', 'value'),
    Input('state-line-chart-state-selection', 'value'),
    Input('state-line-chart-state-selection2', 'value'),
    Input('state-line-chart-normaliser', 'value')
)
def update_state_line_chart(event_type: str, states_selected1, states_selected2, normalise: str) -> Figure:
    labels = {
        "Year": "Years",
        "Amount of Events": "Amount of events",
    }

    states_selected = states_selected1 + states_selected2

    # Mask to get active rows dependendt on input value
    mask = df['Event Type Group'] == event_type
    active_rows = df[mask]

    # Get amount of events per year in the different states, which are selected
    active_rows = active_rows[active_rows['State'].isin(states_selected)]

    # Get amount of events per year per event type
    active_rows = active_rows.groupby(['Year', 'State']).size().reset_index(name='Amount of Events')

    if normalise == "Normalise data":
        labels["Amount of Events"] = "Percentage increase/decrease"

        # Get the first year for each event type
        first_year = active_rows.groupby(['State'])['Amount of Events'].transform('first')

        # Divide the amount of events for each year by the first year and multiply by 100
        active_rows['Amount of Events'] = active_rows['Amount of Events'] / first_year * 100

    fig = px.line(
        active_rows,
        x="Year",
        y="Amount of Events",
        labels=labels,
        color_discrete_sequence=['grey'],
        hover_data={'Amount of Events': False},
        color="State",
        markers=True,
    )

    if normalise == "Normalise data":
        fig.update_yaxes(ticksuffix="%")
    else:
        fig.update_yaxes(autorangeoptions_include=[0])

    # Hover settings for the graph
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=3),
        marker=dict(size=7),
        hovertemplate='<b>%{data.name}:</b> %{y}<br>' +
                      '<extra></extra>',
    )

    fig.update_xaxes(dtick=1)

    fig.update_layout(
        hoverlabel=labelStyle,
        hoverdistance=20,
        hovermode='x unified',
    )

    return fig
