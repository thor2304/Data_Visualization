import dash
from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure
import plotly.express as px


from src.Core.data_provider import get_df
from src.Core.styles import graphDivStyle, pageStyle

dash.register_page(__name__)

df = get_df()

layout = html.Div([
    html.H1('Is there a relation between time periods in the day and certain types of accidents?', style={'textAlign': 'center', 'width': '60%'}),
    html.Div([
        html.Div([
            dcc.Dropdown(df["Rail/Bus/Ferry"].unique(), 'Bus', id='3d-dropdown-selection', style={'width': '50%', 'justify-content': 'end'}),
        ], style={'width': '100%', 'display': 'flex', 'justify-content': 'end', 'align-items': 'center'}),
        dcc.Graph(id='3d-graph', style={'width': '100%', 'height': '60em'}),
        html.H1('', style={'textAlign': 'center '}),
    ], style=graphDivStyle),
], style=pageStyle)



# 3D GRAPH ###################################################################
@callback(
    Output('3d-graph', 'figure'),
    Input('3d-dropdown-selection', 'value')
)
def update_3d_plot(value: str) -> Figure:
    category_data = df[df["Rail/Bus/Ferry"] == value]
    marker_size = 3

    fig = px.scatter_3d(category_data, x='Event Date', y='Event Time', z='Total Injuries', labels={
        "Agency": "agency",
        "Year": "years",
    }, color="Total Injuries")

    fig.update_traces(marker=dict(
        size=marker_size
    ), selector=dict(mode="markers"))

    return fig