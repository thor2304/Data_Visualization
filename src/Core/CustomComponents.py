import dash_bootstrap_components as dbc
from dash import html, dcc

from src.Core.styles import graphDivStyle


def GraphDiv(left_of_graph: list = None, graph: dcc.Graph | html.Div = None, right_of_graph: list = None) -> html.Div:
    if left_of_graph is None:
        left_of_graph = html.P("")
    if right_of_graph is None:
        right_of_graph = html.P("")

    side_style = {'width': '60%', 'margin': 'auto', 'height': '100%', "padding-top": "3em"}
    return html.Div([
        html.Div(left_of_graph, style=side_style),
        graph,
        html.Div(right_of_graph, style=side_style),
    ], style=graphDivStyle)


def CheckList(title: str, options: list[str], checklist_id: str, only_select_first: bool = False) -> dbc.Form:
    return dbc.Form([
        html.Div(
            [html.H3(children=title, style={'textAlign': 'center'}),
             dbc.Checklist(
                 options=options,
                 value=[options[0]] if only_select_first else options,
                 switch=True,
                 id=checklist_id,
             )],
            className="py-2",
        ),
    ])
