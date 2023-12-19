import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px
import numpy as np

from src.Core.data_provider import get_df
from src.Core.styles import graphDivStyle, pageStyle

dash.register_page(__name__)

df = get_df()

eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))

layout = html.Div([
    html.H1('Is there a relation between time periods in the day and certain types of accidents?',
            style={'textAlign': 'center', 'width': '60%'}),
    html.Div([
        html.Div([
            html.H3(children="Choose event type", style={'textAlign': 'center'}),
            dcc.Checklist(
                id="event-checklist",
                options=[{'label': html.Span(i, style={'padding-left': 10}), 'value': i} for i in eventsList],
                value=[eventsList[0]],
                inline=False,
                labelStyle={'display': 'flex', 'align-items': 'center'},
            ),
            html.H3(children="Choose whether to normalise data", style={'textAlign': 'center', 'padding-top': 20}),
            dcc.RadioItems(
                id='event-normaliser',
                options=["Normalise data", "Don't normalise data"],
                value="Don't normalise data",
                labelStyle={'display': 'flex'}),
        ], style={'width': '60%', 'margin': 'auto', 'height': '100%'}),
        dcc.Graph(id='time-graph', style={'width': '100%', 'height': '60em'}),
        html.H1('', style={'textAlign': 'center '}),
    ], style=graphDivStyle),
], style=pageStyle)


@callback(
    Output('time-graph', 'figure'),
    Input('event-checklist', 'value')
)
def update_3d_plot(value: str) -> Figure:
    # Filter the df so only the rows within dateStart and dateEnd are left

    # mask = (df['Event Date'] >= date_start) & (df['Event Date'] <= date_end)
    # active_rows = df[mask]

    mask = df['Event Type Group'].isin(value)
    active_rows = df[mask]

    active_rows['Hour'] = active_rows['Event Time'].apply(
        lambda x: x.replace(second=0, microsecond=0, minute=0, hour=x.hour)
    )

    fig = px.histogram(active_rows, x="Hour", y="Total Injuries", color='Event Type Group', orientation='v',
                       height=800,
                       title="Test")

    fig.update_xaxes(
        title_text="Time of day"
    )

    return fig

# Plot 1: What ype of accidents at what time of day?
# Stacked bar chart for accident types. X-axis: time of day. Y-axis: number of accidents. Color: accident type.

# Plot 2:  At what time of day are people injured?
# Bar chart for number of injuries. X-axis: time of day. Y-axis: number of injuries. Color: accident type.

# Consider:
# Overlaying the number of injuries as a line on the first plot.
