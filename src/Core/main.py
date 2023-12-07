import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink(page['name'], href=page["relative_path"])) for page in dash.page_registry.values()
    ],
    brand="Group 11 Data visualization project",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    navbar,
    html.Br(),
    dash.page_container,

    # store
    dcc.Store(id='pandas_data', storage_type='memory'),
])


def main():
    app.run(debug=True, host="127.0.0.1", port=8070)


if __name__ == '__main__':
    main()
