import dash
import dash_bootstrap_components as dbc
from dash import html
from utils import get_introduction_block

dash.register_page(__name__, path='/')

layout = html.Div(
    className="page-container",
    children=get_introduction_block()
)