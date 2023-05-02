"""This is the main module to generate a themed playlist on a weekly basis, piecing other modules together."""

import fastapi

from playlist_generator import compose_playlist
from playlist_publisher import publish_playlist_to_spotify
from utils import get_logger

main = fastapi.FastAPI()

logger = get_logger(__name__)


@main.post("/weekly_themed_playlist")
def create_themed_playlist(theme: str) -> str:
    """Create a themed playlist on a weekly basis.

    Returns:
        str: A message informing the user that the playlist has been successfully updated.
    """
    playlist = compose_playlist(theme=theme)
    logger.info(f"Sending playlist titled '{playlist.title}' to publisher-service.")
    message = publish_playlist_to_spotify(playlist)
    return message
