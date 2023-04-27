from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import flask

server = flask.Flask(__name__)

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

#app = Dash(url_base_pathname = '/', use_pages=True, external_stylesheets=external_stylesheets)
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets, server=server)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='assets/logo.png', height="50px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/global",
                style={"textDecoration": "none"},
            ),
        dbc.NavItem(dbc.NavLink("Global Comparison", href="/global")),
        dbc.NavItem(dbc.NavLink("Query Tracing", href="/threshold")),
        dbc.NavItem(dbc.NavLink("Per-Query Stats", href="/qdata")),
            ]
        ),
    color="light",
    dark=False,
)

app.layout = html.Div([
    navbar,
    html.P(""),
	dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
