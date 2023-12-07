import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

navbarChildren = [
    dbc.NavItem(dbc.NavLink(page['name'], id=page["name"], href=page["relative_path"])) for page
    in dash.page_registry.values()
]
navbarChildren.append(dbc.NavItem(
    dbc.Button(
        "Download Report",
        href="/static/group-11-report-DV.pdf",
        download="group-11-report-DV.pdf",
        external_link=True,
        color="dark",
    )))

navbar = dbc.NavbarSimple(
    children=navbarChildren,
    brand="Group 11 Data visualization project",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    navbar,
    html.Br(),
    dash.page_container,
])


def main():
    app.run(debug=True, host="127.0.0.1", port=8070)


if __name__ == '__main__':
    main()
