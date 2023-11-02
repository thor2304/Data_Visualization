import os

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure

print("fetch data")
if os.environ["fetch"] == "True":
    df = pd.read_csv('http://datadump.cryptobot.dk/Major_Safety_Events.csv', low_memory=False)
else:
    df = pd.read_csv('Major_Safety_Events.csv')
print("data fetched")
print(df.columns[35])

TITLE = 'Data Visualizations incoming'

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1(children=TITLE, style={'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value: str) -> Figure:
    return
    # country_data = df[df.country == value]
    # return go.
    # return px.line(country_data, x='year', y='pop', labels={
    #     "year": "years",
    #     "pop": "population",
    # })


def main():
    print(df)
    app.run(debug=True, host="127.0.0.1", port=8070)


if __name__ == '__main__':
    main()
