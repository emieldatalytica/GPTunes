"""Generate a playlist with OpenAI's GPT API based on a given theme."""

import os
from typing import Any

import fastapi
import openai

from prompt import INITIAL_PROMPT
from theme_picker import get_random_city
from utils import Playlist, extract_json_from_response, get_logger, spotify_client

openai.api_key = os.getenv("OPENAI_API_KEY")

playlist_generator = fastapi.FastAPI()
logger = get_logger(__name__)


@playlist_generator.get("/query_gpt_model")
def query_model_for_playlist(theme: str) -> str:
    """Generate a playlist with OpenAI's GPT API based on a given theme.

    Args:
        theme (str): The theme of the playlist.

    Returns:
        str: The model response in json-format.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": INITIAL_PROMPT.replace("{theme}", theme)},
        ],
        temperature=0.8,
    )
    return completion.choices[0].message["content"]  # type: ignore


def map_tracks_to_spotify_ids(tracks: dict) -> dict:
    """Map the tracks to their spotify ids using the spotify api.

    Args:
        tracks (dict): The tracks to map.

    Returns:
        dict: The tracks mapped to their spotify ids.
    """
    mapped_tracks = {}
    for artist, track in tracks.items():
        result = spotify_client.spotify.search(f"{artist} - {track}", type="track", limit=1)
        if result is None:
            # search again on only track name
            result = spotify_client.spotify.search(f"{track}", type="track", limit=1)
        if result is None:
            continue
        items = result.get("tracks", {}).get("items", [])
        if not items:
            continue
        mapped_tracks[track] = items[0]["id"]
    logger.info(f"Mapped {len(mapped_tracks.values())} tracks to spotify ids.")
    return mapped_tracks


@playlist_generator.get("/playlist", response_model=Playlist)
def compose_playlist(theme: str) -> Any:
    """Compose a playlist for a given theme.

    Args:
        theme (str): The theme of the playlist. If empty, a random theme is picked.
    Returns:
        Playlist: The composed playlist with tracks, title and description.
    """
    if not theme:
        theme = get_random_city()
    logger.info(f"Given theme: '{theme}'")
    gpt_response = query_model_for_playlist(theme)
    playlist_json = extract_json_from_response(gpt_response)

    assert isinstance(playlist_json, dict)
    assert all(key in playlist_json.keys() for key in ["tracks", "title", "description"])
    logger.info(f"Extracted playlist with {len(playlist_json['tracks'].keys())} tracks from GPT response.")

    track_ids = map_tracks_to_spotify_ids(playlist_json["tracks"])
    playlist_json["tracks"] = list(track_ids.values())
    logger.info(playlist_json)
    playlist = Playlist(**playlist_json)
    return playlist
