from random import choice

from dash import Dash, html, State
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_extensions import EventListener
from dash_extensions.enrich import DashProxy
from dash_iconify import DashIconify

app = DashProxy()

event = {"event": "keydown", "props": ["key", "altKey", "ctrlKey", "shiftKey", "metaKey", "repeat"]}


class AsciiTableType1(html.Div):
    def __init__(self, df):
        columns = df.columns
        columns_length = [len(column) for column in columns]
        total_length = sum(columns_length)
        header = html.Div([html.Div(children="".join(["_" for i in range(length)]))
                           for column, length in zip(columns, columns_length)])
        super().__init__([  # Equivalent to `html.Div([...])`
            header
        ])


class AsciiTableType2(html.Div):
    def __init__(self, df):
        columns = df.columns
        columns_length = [len(column) for column in columns]
        total_length = sum(columns_length)
        header = html.Div([html.Div(children="".join(["-" for i in range(length)]))
                           for column, length in zip(columns, columns_length)])
        super().__init__([  # Equivalent to `html.Div([...])`
            header
        ])


current_input = html.Div([html.Div(">>> ", style={"color": "white"}),
                          dcc.Input([], style={"border": "none", "background": "transparent", "color": "white"},
                                    id="current_input")],
                         className="d-flex flex-row",
                         id="current_input_div",
                         style={"position": "absolute", "bottom": "0", "left": "0", "right": "0",
                                "background-color": "black"})

el = EventListener(id="el", events=[event], logging=True),


@app.callback(
    Output("current_input_div", "children"),
    Input("el", "n_events"),
    State("el", "event"),
    State("current_input", "value"),
    State("current_input_div", "children")
)
def key_event(n_events, e, current_input_value, current_input_div_children):
    print(e)
    if e is None:
        raise PreventUpdate()
    if e["key"] == "Return":
        current_input_div_children = html.Div([html.Div(f">>> {current_input_value}"),
                                               html.Div([html.Div([html.Div(">>> "),
                                                                   dcc.Input([], style={"border": "none"},
                                                                             id="current_input")],
                                                                  className="d-flex flex-row",
                                                                  id="current_input_div")])])
    print("pushed")
    return current_input_div_children


my_div = html.Div(
    [
        html.Div([
            DashIconify(icon="eos-icons:content-new",
                        color="green",
                        width=50, )
        ],
            style={"position": "absolute", "bottom": "30%", "left": "30%", "right": "30%", "top": "30%",
                   "border": "1px solid black", "background-color": "#ECEFF1"},
            className="d-flex flex-row justify-content-center align-items-center"),
    ], id="page")

app.layout = html.Div([my_div])

if __name__ == "__main__":
    app.run_server(port=9000)
