import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc

from src.Core.CustomComponents import GraphDiv, CheckList
from src.Core.data_provider import get_df, get_category_orders
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

    grouped_df = sorted_df.groupby(["Event Type Group", "Hour", "Month"], as_index=False).agg({y_selection: sum})
    grouped_df = grouped_df.sort_values("Month", ascending=True)
    #
    # fig = px.histogram(sorted_df, x="Hour", y=y_selection, color='Event Type Group', orientation='v',
    #                    category_orders=get_category_orders(),
    #                    color_discrete_sequence=legendColors,
    #                    )

    fig = px.bar(grouped_df, x="Hour", y=y_selection, color='Event Type Group',
                 category_orders=get_category_orders(),
                 color_discrete_sequence=legendColors,
                 animation_frame="Month",
                 animation_group="Hour",
                 )

    # fig.update_layout(updatemenus=[
    #     {
    #         "buttons": [
    #             {
    #                 "args": [None, {"frame": {"duration": 500, "redraw": False},
    #                                 "fromcurrent": True, "transition": {"duration": 300,
    #                                                                     "easing": "quadratic-in-out"}}],
    #                 "label": "Play",
    #                 "method": "animate"
    #             },
    #             {
    #                 "args": [[None], {"frame": {"duration": 0, "redraw": False},
    #                                   "mode": "immediate",
    #                                   "transition": {"duration": 0}}],
    #                 "label": "Pause",
    #                 "method": "animate"
    #             }
    #         ],
    #         "direction": "left",
    #         "pad": {"r": 10, "t": 87},
    #         "showactive": False,
    #         "type": "buttons",
    #         "x": 0.1,
    #         "xanchor": "right",
    #         "y": 0,
    #         "yanchor": "top"
    #     }
    # ]
    # )


    return treat_histogram_fig(fig, y_selection)


# @callback(
#     Output('time-graph', 'figure'),
#     Input('type-dropdown-selection', 'value'),
#     Input('event-checklist', 'value'),
# )
# def time_of_day(y_selection: str, selected_event_types: list[str]) -> Figure:
#     # Hover could be solved by adding another column, that is Hour.dt.time, and then show that.
#
#     mask = df['Event Type Group'].isin(selected_event_types)
#     active_rows = df[mask]
#     sorted_df = active_rows.sort_values("Event Date", ascending=True)
#
#     fig = px.histogram(sorted_df, x="Hour", y=y_selection, color='Event Type Group', orientation='v',
#                        category_orders=get_category_orders(),
#                        color_discrete_sequence=legendColors,
#                        )
#
#     return treat_histogram_fig(fig, y_selection)


@callback(
    Output('time-graph-animated', 'figure'),
    Input('type-dropdown-selection-animated', 'value'),
    Input('event-checklist-animated', 'value'),
)
def animated_time_of_day(y_selection: str, selected_event_types: list[str]) -> Figure:
    # Hover could be solved by adding another column, that is Hour.dt.time, and then show that.
    max_Ranges = {
        "Total Injuries": 700,
        "Number of accidents": 600,
        "Total Fatalities": 25,
    }

    mask = df['Event Type Group'].isin(selected_event_types)
    active_rows = df[mask]
    sorted_df = active_rows.sort_values("Event Date", ascending=True)

    fig = px.histogram(sorted_df, x="Hour", y=y_selection, color='Event Type Group', orientation='v',
                       category_orders=get_category_orders(),
                       color_discrete_sequence=legendColors,
                       animation_frame="Month",
                       # animation_group="Event Type Group",
                       range_y=[0, max_Ranges[y_selection]],
                       # title="Number of accidents per hour of the day"
                       )

    return treat_histogram_fig(fig, y_selection)


def treat_histogram_fig(fig: Figure, y_selection: str, transition_duration = 1500) -> Figure:
    hovertemplate = '<b>%{data.name}</b><br>' + \
                    '<b>' + y_selection + ':</b> %{y}<br>' + \
                    '<b>Time:</b> %{x}<br>' + \
                    '<extra></extra>'
    texttemplate = '%{y}'
    fig.update_traces(
        # texttemplate=texttemplate,
        hovertemplate=hovertemplate,
    )

    for f in fig.frames:
        for trace in f.data:
            trace.update(
                hovertemplate=hovertemplate,
                # texttemplate=texttemplate
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
