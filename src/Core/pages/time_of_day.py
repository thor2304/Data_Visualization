import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import numpy as np

from src.Core.data_provider import get_df, get_category_orders
from src.Core.styles import graphDivStyle, pageStyle, graphStyle, legendColors

dash.register_page(__name__, name="When does injuries happen?")

df = get_df()

eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))

layout = html.Div([
    html.H1('Is there a relation between time periods in the day and certain types of accidents?',
            style={'textAlign': 'center', 'width': '60%'}),
    html.Div([
        html.Div([
            html.H3(children="Choose Y-axis", style={'textAlign': 'center'}),
            dcc.Dropdown(["Total Injuries", "Number of accidents", "Total Fatalities"], 'Total Injuries',
                         id='type-dropdown-selection',
                         style={'width': '100%', 'justify-content': 'end'},
                         clearable=False),
        ], style={'width': '60%', 'margin': 'auto', 'height': '100%'}),
        dcc.Graph(id='time-graph', style=graphStyle),
        html.H4('Remove event types by clicking the legend', style={'textAlign': 'center '}),
    ], style=graphDivStyle),
], style=pageStyle)


@callback(
    Output('time-graph', 'figure'),
    Input('type-dropdown-selection', 'value')
)
def update_3d_plot(y_selection: str) -> Figure:
    # Hover could be solved by adding another column, that is Hour.dt.time, and then show that.
    fig = px.histogram(df, x="Hour", y=y_selection, color='Event Type Group', orientation='v',
                       category_orders=get_category_orders(),
                       color_discrete_sequence=legendColors,
                       # height=800,
                       # title="Number of accidents per hour of the day"
                       )

    fig.update_traces(
        texttemplate='%{y}',
        hovertemplate='<b>%{data.name}</b><br>' +
                      '<b>' + y_selection + ':</b> %{y}<br>' +
                      '<b>Time:</b> %{x}<br>' +
                      '<extra></extra>',
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

    return fig

# Plot 1: What ype of accidents at what time of day?
# Stacked bar chart for accident types. X-axis: time of day. Y-axis: number of accidents. Color: accident type.

# Plot 2:  At what time of day are people injured?
# Bar chart for number of injuries. X-axis: time of day. Y-axis: number of injuries. Color: accident type.

# Consider:
# Overlaying the number of injuries as a line on the first plot.
