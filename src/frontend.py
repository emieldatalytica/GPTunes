import os
from typing import Tuple, Union

import dash
import requests  # type: ignore
from dash import dcc, html
from dash.dependencies import Input, Output, State

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title="GPTunes")
server = app.server


app.layout = html.Div(
    className="container-fluid",
    children=[
        html.Div(
            className="content",
            children=[
                html.Div(
                    className="icons",
                    children=[
                        html.A(className="github", href="https://github.com/emieldatalytica/GPTunes", target="_blank"),
                        html.A(className="linkedin", href="https://www.linkedin.com/in/emieldeheij/", target="_blank"),
                    ],
                ),
                html.H1("🎶  GPTunes  🎶", className="title"),
                html.H3("Craft your themed Spotify playlist with AI!", className="subtitle"),
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
        post_url = os.environ.get("POST_URL", "http://0.0.0.0:8080/create_themed_playlist")
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
    debug_mode = os.getenv("DEBUG_MODE", "True").lower() == "true"
    app.run_server(debug=debug_mode, host="0.0.0.0", port=8050)
