import os
from typing import Tuple, Union

import dash
import requests  # type: ignore
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(
    className="container",
    children=[
        html.Div(
            className="content",
            children=[
                html.H1("Generate your themed playlist with AI", className="title"),
                dcc.Input(id="input-field", type="text", placeholder="Enter a theme here", className="input"),
                html.Button("Submit", id="submit-button", className="button"),
                dcc.Loading(
                    id="loading-icon",
                    children=[html.Div(id="output-field", className="output"), html.Div(id="playlist-embed")],
                    type="default",
                ),
            ],
        )
    ],
)


@app.callback(
    Output("output-field", "children"),
    Output("playlist-embed", "children"),
    Input("submit-button", "n_clicks"),
    State("input-field", "value"),
)
def create_and_embed_playlist(
    n_clicks: Union[int, None], value: Union[str, None]
) -> Tuple[Union[dcc.Markdown, None], Union[html.Iframe, None]]:
    if n_clicks == 1 and value is not None:
        post_url = "http://0.0.0.0:8080/create_themed_playlist"  # local debugging
        # post_url = "https://gptunes-api-lduyxfnclq-ez.a.run.app/create_themed_playlist"
        response = requests.post(post_url, params={"theme": value})
        if response.status_code == 200:
            playlist_data = response.json()
            playlist_url = playlist_data["url"]
            playlist_description = playlist_data["description"]

            stripped_url = playlist_url.split("/")[-1].split("?")[0]
            src_url = f"https://open.spotify.com/embed/playlist/{stripped_url}?utm_source=generator?theme=0"

            text = "Follow your playlist here!"
            hyperlinked_string = f"{playlist_description}\n\n[{text}]({playlist_url})"

            return dcc.Markdown(hyperlinked_string), html.Iframe(
                src=src_url,
                height="352",
                width="80%",
                style={"border-radius": "12px"},
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture",
            )
        else:
            error_message = (
                f"There was an error in creating the playlist. Status code: {response.status_code}. "
                f"Message: {response.text}"
            )
            return error_message, None

    return None, None


if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
    app.run_server(debug=debug_mode, host="0.0.0.0", port=8050)
