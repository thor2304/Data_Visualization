from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from src.Core.styles import graphDivStyle, graphStyle


def GraphDiv(left_of_graph: list = None, graph: dcc.Graph | html.Div = None, right_of_graph: list = None) -> html.Div:
    if left_of_graph is None:
        left_of_graph = html.P("")
    if right_of_graph is None:
        right_of_graph = html.P("")

    side_style = {'width': '60%', 'margin': 'auto', 'height': '100%', "padding-top": "4em"}
    return html.Div([
        html.Div(left_of_graph, style=side_style),
        graph,
        html.Div(right_of_graph, style=side_style),
    ], style=graphDivStyle)
