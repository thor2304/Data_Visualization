from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

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
    country_data = df[df.country == value]
    # return go.
    return px.line(country_data, x='year', y='pop', labels={
        "year": "years",
        "pop": "population",
    })


def main():
    app.run(debug=True, host="127.0.0.1", port=8070)


if __name__ == '__main__':
    main()
