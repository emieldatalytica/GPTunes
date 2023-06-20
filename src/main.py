"""This is the main module to generate a themed playlist on a weekly basis, piecing other modules together."""

from typing import Dict

import fastapi
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from playlist_generator import compose_playlist
from playlist_publisher import publish_playlist_to_spotify
from utils import get_logger

main = fastapi.FastAPI()

logger = get_logger(__name__)


@main.get("/", include_in_schema=False)
def docs_redirect() -> RedirectResponse:
    return RedirectResponse("/docs")


@main.post("/create_themed_playlist")
def create_themed_playlist(theme: str) -> Dict[str, str]:
    """Create a themed playlist and publish it to Spotify.

    Raises:
        HTTPException: If the playlist could not be created or published.

    Returns:
        Dict[str, str]: The playlist url and description.
    """
    try:
        playlist = compose_playlist(theme=theme)
        logger.info(f"Sending playlist titled '{playlist.title}' to publisher-service.")
        url = publish_playlist_to_spotify(playlist)
    except Exception as e:
        logger.error(f"Failed to create and publish playlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"url": url, "description": playlist.description}
