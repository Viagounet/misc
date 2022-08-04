from dash_extensions.enrich import DashProxy, html, Input, Output, State
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate

# JavaScript event(s) that we want to listen to and what properties to collect.
# Create small example app
event = {"event": "keydown", "props": ["key", "altKey", "ctrlKey", "shiftKey","metaKey", "repeat"]}
app = DashProxy()
app.layout = html.Div([
    EventListener(id="el", events=[event], logging=True, children=[
    ]),
    html.Div(style={"background-color": "red", "width": "30px", "position": "absolute",
                    "top": "5%", "bottom":"85%"}, id="pong-bar"),
])


@app.callback(Output("pong-bar", "style"), Input("el", "n_events"), State("el", "event"), State("pong-bar", "style"))
def click_event(n_events, e, style):
    y_top = int(style["top"].replace("%", ""))
    y_bottom = int(style["bottom"].replace("%", ""))

    if e is None:
        raise PreventUpdate()

    if e["key"] == "ArrowDown":
        y_top += 2
        y_bottom -= 2

    if e["key"] == "ArrowUp":
        y_top -= 2
        y_bottom += 2

    style["top"] = f"{y_top}%"
    style["bottom"] = f"{y_bottom}%"

    print(style)

    return style


if __name__ == "__main__":
    app.run_server()
