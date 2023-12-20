import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc

from src.Core.CustomComponents import GraphDiv, CheckList
from src.Core.data_provider import get_df, get_category_orders, get_reverse_category_orders
from src.Core.styles import graphDivStyle, pageStyle, graphStyle, legendColors

dash.register_page(__name__, name="When does injuries happen?")

df = get_df()

eventsList = sorted(df["Event Type Group"].unique())
layout = html.Div([
    html.H1('Is there a relation between time periods in the day and certain types of accidents?',
            style={'textAlign': 'center', 'width': '60%'}),
    GraphDiv(
        left_of_graph=[
            html.H3(children="Choose Y-axis", style={'textAlign': 'center'}),
            dcc.Dropdown(["Total Injuries", "Number of accidents", "Total Fatalities"], 'Total Injuries',
                         id='type-dropdown-selection',
                         style={'width': '100%', 'justify-content': 'end'},
                         clearable=False),
            CheckList(title="Choose event types", options=eventsList, checklist_id="event-checklist"),

        ],
        graph=dcc.Graph(id='time-graph', style=graphStyle),
    ),
    html.H1('How does this change over the course of a year?',
            style={'textAlign': 'center', 'width': '60%'}),
    html.P(
        "The following graph shows the number of accidents per month, for each event type group. "
        "The data is summed up from the years 2014-2022"),
    GraphDiv(
        left_of_graph=[
            html.H3(children="Choose Y-axis", style={'textAlign': 'center'}),
            dcc.Dropdown(["Total Injuries", "Number of accidents", "Total Fatalities"], 'Total Injuries',
                         id='type-dropdown-selection-animated',
                         style={'width': '100%', 'justify-content': 'end'},
                         clearable=False),
            CheckList(title="Choose event types", options=eventsList, checklist_id="event-checklist-animated"),
        ],
        graph=dcc.Graph(id='time-graph-animated', style=graphStyle),
    )
], style=pageStyle)




@callback(
    Output('time-graph', 'figure'),
    Input('type-dropdown-selection', 'value'),
    Input('event-checklist', 'value'),
)
def time_of_day(y_selection: str, selected_event_types: list[str]) -> Figure:
    # Hover could be solved by adding another column, that is Hour.dt.time, and then show that.

    mask = df['Event Type Group'].isin(selected_event_types)
    active_rows = df[mask]
    sorted_df = active_rows.sort_values("Event Date", ascending=True)

    fig = px.histogram(sorted_df, x="Hour", y=y_selection, color='Event Type Group', orientation='v',
                       category_orders=get_category_orders(),
                       color_discrete_sequence=legendColors,
                       )

    return treat_histogram_fig(fig, y_selection)


@callback(
    Output('time-graph-animated', 'figure'),
    Input('type-dropdown-selection-animated', 'value'),
    Input('event-checklist-animated', 'value'),
)
def animated_time_of_day(y_selection: str, selected_event_types: list[str]) -> Figure:
    # Hover could be solved by adding another column, that is Hour.dt.time, and then show that.
    mask = df['Event Type Group'].isin(selected_event_types)
    active_rows = df[mask]
    sorted_df = active_rows.sort_values("Event Date", ascending=True)

    max_Ranges = {
        "Total Injuries": 700,
        "Number of accidents": 600,
        "Total Fatalities": 25,
    }

    grouped_df = sorted_df.groupby(["Event Type Group", "Hour", "Month"], as_index=False).agg({y_selection: sum})
    grouped_df = grouped_df.sort_values("Month", ascending=True)

    fig = px.bar(grouped_df, x="Hour", y=y_selection, color='Event Type Group',
                 category_orders=get_reverse_category_orders(),
                 color_discrete_sequence=list(
                     reversed(legendColors[0:len(get_reverse_category_orders()["Event Type Group"])])),
                 animation_frame="Month",
                 animation_group="Hour",
                 range_y=[0, max_Ranges[y_selection]],
                 )

    months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    sorted_frames = list(fig.frames)
    sorted_frames.sort(key=lambda x: months[x.name])
    fig.frames = tuple(sorted_frames)

    sorted_steps = list(fig.layout.sliders[0].steps)
    sorted_steps.sort(key=lambda x: months[x.args[0][0]])
    fig.layout.sliders[0].steps = sorted_steps

    return treat_histogram_fig(fig, y_selection)


def treat_histogram_fig(fig: Figure, y_selection: str, show_text=True, transition_duration=1500) -> Figure:
    hovertemplate = '<b>%{data.name}</b><br>' + \
                    '<b>' + y_selection + ':</b> %{y}<br>' + \
                    '<b>Time:</b> %{x}<br>' + \
                    '<extra></extra>'
    texttemplate = '%{y}'
    text_position = 'inside'
    fig.update_traces(
        hovertemplate=hovertemplate,
    )

    if show_text:
        fig.update_traces(
            texttemplate=texttemplate,
            textposition=text_position,
        )

    for f in fig.frames:
        for trace in f.data:
            trace.update(
                hovertemplate=hovertemplate,
            )
            if show_text:
                trace.update(
                    texttemplate=texttemplate,
                    textposition=text_position,
                )

    fig.update_xaxes(
        title_text="Time of day",
    )

    fig.update_layout(
        xaxis=dict(tickformat='<b>%H:%M</b>',
                   type='date'),
        hovermode='x unified',
        bargap=0.2,
    )

    if len(fig.frames) > 1:
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = transition_duration

    return fig

# Plot 1: What ype of accidents at what time of day?
# Stacked bar chart for accident types. X-axis: time of day. Y-axis: number of accidents. Color: accident type.

# Plot 2:  At what time of day are people injured?
# Bar chart for number of injuries. X-axis: time of day. Y-axis: number of injuries. Color: accident type.

# Consider:
# Overlaying the number of injuries as a line on the first plot.
