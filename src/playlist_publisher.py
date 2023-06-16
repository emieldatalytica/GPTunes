"""Module for publishing auto-generated themed playlists to Spotify."""

import fastapi

from utils import Playlist, get_logger, spotify_client

playlist_publisher = fastapi.FastAPI()

logger = get_logger(__name__)


@playlist_publisher.post("/publish")
def publish_playlist_to_spotify(playlist: Playlist) -> str:
    """Publish a playlist to Spotify.

    Args:
        playlist (Playlist): The playlist to publish.

    Returns:
        str: The playlist id.
    """
    # create the playlist
    new_playlist = spotify_client.spotify.user_playlist_create(
        user=spotify_client.spotify.current_user()["id"],
        name=playlist.title,
        public=True,
        collaborative=False,
        description=playlist.description,
    )

    # add the tracks to the playlist
    spotify_client.spotify.user_playlist_add_tracks(
        user=spotify_client.spotify.current_user()["id"],
        playlist_id=new_playlist["id"],
        tracks=playlist.tracks,
    )

    # upload the cover image
    try:
        spotify_client.spotify.playlist_upload_cover_image(
            playlist_id=new_playlist["id"], image_b64=playlist.cover_image
        )
    except Exception as e:
        logger.error(f"Could not upload cover image: {e}")

    return new_playlist["external_urls"]["spotify"]
