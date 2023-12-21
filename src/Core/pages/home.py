import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure
import numpy as np
import united_states
import dash_bootstrap_components as dbc

from src.Core.styles import graphStyle, dropdownStyle
from src.Core.data_provider import get_df

dash.register_page(__name__, path='/', name="Introduction", order=0)

us = united_states.UnitedStates()

TITLE = 'Group 11 visualizations - Major Safety Events'
Questions = {
    "2": "",
}

df = get_df()

layout = html.Div([
    html.Div([
        # TITLE
        html.H1(children=TITLE, style={'textAlign': 'center'}),
        html.Br(),

        # INTRODUCTION
        html.H3(children="Introduction", style={'textAlign': 'center'}),
        html.P(children="We are four students, "
                        "who created this dashboard during a course in data visualization in an attempt to "
                        "illustrate/find different relations between Major Security and Safety Events in transportation"
                        " in the United States of America between 2014 and 2022, which is our dataset."),
        html.P(children=["The dataset can be found at: ",
                         html.A("data.gov", href="https://catalog.data.gov/dataset/major-safety-events", )]),
        html.P(children="The dashboard includes fully interactive plots using Plotly. "
                        "This means that all plots can be adjusted to highlight certain areas or specific information. "
                        "The plots allow zoom in and out. "
                        "These features are incredibly useful on the heat maps "
                        "if specific areas are interesting for the user. "),
        html.P(children="At the top of the page a navigation bar can be found. "
                        "The navigation bar can be used to switch between the different pages. "
                        "Each page contains an overall question, which we tried to answer through the visualizations. "
                        "The questions are the following:"),
        dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    "Is there an increase or decrease in certain types of accidents in the last 9 years?"),
                dbc.ListGroupItem(
                    "Is there a relation between time periods in the day and certain types of accidents?"),
                dbc.ListGroupItem("Do certain types of accidents occur more often in certain environments?"),
            ],
            numbered=True,
            style={"width": "fit-content", "margin": "auto"},
        ),
        html.P(children=["The report can be downloaded ",
                         html.A("here", href="/static/group-11-report-DV.pdf", download="group-11-report-DV.pdf")]),

    ], style={'width': '60%', "text-align": "center"}),
],
    style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
)
