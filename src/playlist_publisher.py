"""Module for publishing auto-generated themed playlists to Spotify."""

import fastapi

from utils import get_logger, spotify_client

playlist_publisher = fastapi.FastAPI()

logger = get_logger(__name__)


@playlist_publisher.post("/publish")
def publish_playlist_to_spotify(playlist: dict) -> str:
    """Publish a playlist to Spotify.

    Args:
        playlist (dict): The playlist's track ids and description to publish.

    Returns:
        str: The playlist id.
    """
    # create the playlist
    new_playlist = spotify_client.spotify.user_playlist_create(
        user=spotify_client.spotify.current_user()["id"],
        name=playlist["title"],
        public=True,
        collaborative=False,
        description=playlist["description"],
    )

    # add the tracks to the playlist
    spotify_client.spotify.user_playlist_add_tracks(
        user=spotify_client.spotify.current_user()["id"],
        playlist_id=new_playlist["id"],
        tracks=playlist["playlist"],
    )

    user_message = f"""A new playlist {new_playlist["title"]} has been created!
            Check it out here: {new_playlist['external_urls']['spotify']}"""

    logger.info(user_message)
    return user_message
