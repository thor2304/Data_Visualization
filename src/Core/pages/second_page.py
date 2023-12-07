import dash
from dash import Dash, html, dcc, callback, Output, Input

dash.register_page(__name__)

layout = html.Div([
    html.H1('This is our Archive page'),
    html.Div('This is our Archive page content.'),
])
