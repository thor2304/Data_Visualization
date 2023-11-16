import os

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure

print("fetch data")
if os.environ["fetch"] == "True":
    df = pd.read_csv('http://datadump.cryptobot.dk/Major_Safety_Events.csv', low_memory=False)
else:
    df = pd.read_csv('src/Core/cleaned_output.csv')
print("data fetched")
print(df.columns[35])

TITLE = 'Data Visualizations incoming'

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1(children=TITLE, style={'textAlign': 'center'}),
    dcc.Dropdown(df.Agency.unique(), 'Metro Transit', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value: str) -> Figure:
    country_data = df[df.Agency == value]
    return px.scatter(country_data, x='Vehicle Speed', y='Total Serious Injuries', labels={
        "Agency": "agency",
        "Year": "years",
    })


def main():
    print(df)
    print(df.columns)
    app.run(debug=True, host="127.0.0.1", port=8070)


if __name__ == '__main__':
    main()
