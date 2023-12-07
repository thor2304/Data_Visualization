import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure
import numpy as np
import united_states

from src.Core.styles import graphStyle, dropdownStyle
from src.Core.data_provider import get_df

dash.register_page(__name__, path='/', name="Introduction")

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
        html.P(children="This dashboard is made to visualize the data from the Major Safety Events dataset. "
                         "The dataset contains information about accidents in the United States from 2010 to 2019. "
                         "The dataset contains information about the type of accident, the location, the time of the "
                         "accident and the number of fatalities and injuries. "
                         "The dataset can be found on the following link: "
                         "https://www.kaggle.com/ahmedlahlou/accidents-in-usa-from-december-2015-to-september-2019"),

    ], style={'width': '60%'}),
],
    style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
)

