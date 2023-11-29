import os
import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure
import numpy as np
import united_states

us = united_states.UnitedStates()

print("fetch data")
if os.environ["fetch"] == "True":
    df = pd.read_csv('http://datadump.cryptobot.dk/Major_Safety_Events.csv', low_memory=False)
else:
    filename = f"{__file__[:-7]}data/cleaned_output.csv"
    df = pd.read_csv(filename)
    # df.apply(lambda x: x['Event Date'].format(name=x['name']), axis=1)
    df['Event Date'] = pd.to_datetime(df['Event Date'])
    df['Event Time'] = pd.to_datetime(df['Event Time'])
print("data fetched")
print(df.columns[12])
print(df["Event Time"])


TITLE = 'Data Visualizations incoming'

app = Dash(__name__, use_pages=True)

server = app.server

## List to Event Graph
eventsListRaw = df["Event Type Group"].unique()
eventsList = np.delete(eventsListRaw, np.where(eventsListRaw == "Non-RGX Collision"))

app.layout = html.Div([
html.H1('Multi-page app with Dash Pages'),
html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
        dash.page_container

    # html.H1(children=TITLE, style={'textAlign': 'center'}),
    # dcc.Dropdown(df["Rail/Bus/Ferry"].unique(), 'Bus', id='3d-dropdown-selection'),
    # dcc.Graph(id='3d-graph', style={'width': '100%', 'height': '80em'}),

    # dcc.Dropdown(df.Agency.unique(), 'Dallas Area Transit', id='dropdown-selection'),
    # dcc.Graph(id='graph-content'),
    # html.H2(children="Map of all accidents", style={'textAlign': 'center'}),
    # dcc.Graph(id='accident-map', style={'width': '100%', 'height': '60em'}),

    # html.H2(children="Graph showing amount of events", style={'textAlign': 'center'}),
    # dcc.Dropdown(eventsList, 'Collision', id='event-dropdown-selection'),
    # dcc.Graph(id='event-graph'),
])


# @callback(
#     Output('3d-graph', 'figure'),
#     Input('3d-dropdown-selection', 'value')
# )
# def update_3d_plot(value: str) -> Figure:
#     category_data = df[df["Rail/Bus/Ferry"] == value]
#     marker_size = 3
#
#     fig = px.scatter_3d(category_data, x='Event Date', y='Event Time', z='Total Injuries', labels={
#         "Agency": "agency",
#         "Year": "years",
#     }, color="Total Injuries")
#
#     fig.update_traces(marker=dict(
#         size=marker_size
#     ), selector=dict(mode="markers"))
#
#     return fig


# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value: str) -> Figure:
#     country_data = df[df.Agency == value]
#     return px.scatter(country_data, x='Event Date', y='Total Serious Injuries', labels={
#         "Agency": "agency",
#         "Year": "years",
#     })

@callback(
    Output('event-graph', 'figure'),
    Input('event-dropdown-selection', 'value')
)
def update_event_graph(value: str) -> Figure:
    ## Get all event types except for Non-RGX Collision
    oldList = df['Event Type Group'].unique()
    eventTypes = oldList.tolist()
    eventTypes.remove("Non-RGX Collision")

    ## Create list from year column
    testDf = df['Year'].unique()
    p = testDf.tolist()

    ## Sort list in ascending order
    p.sort()

    ## Create new dataframe to store data
    out = pd.DataFrame()

    ## Add year column from original data starting from lowest year to highest
    out['Year'] = p
    print(out)

    ## Calculate number of events per year one event type
    counts = df[df['Event Type Group'] == value]['Year'].value_counts()
    counts.sort_index(inplace=True, ascending=True)
    print(counts)

    ## Add event type column to new dataframe
    out[value] = counts.values
    print(out)

    return px.line(out, x='Year', y=value, markers=True, labels={
        value: "Amount of events",
        "Year": "Years",
    })


# @callback(
#     Output('accident-map', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_map(value: str) -> Figure:
#     # Callbacks in Dash have to have an output and an input.
#     # We don't use the input for this, but we need it to trigger the callback
#     return px.density_mapbox(df, lat='Latitude', lon='Longitude', radius=10,
#                              center=dict(lat=36.6062, lon=-98.3321), zoom=4,
#                              mapbox_style="open-street-map")


def main():
    app.run(debug=True, host="127.0.0.1", port=8070)




if __name__ == '__main__':
    main()
