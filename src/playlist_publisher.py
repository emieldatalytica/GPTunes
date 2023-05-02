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
        tracks=playlist.playlist,
    )

    user_message = f"""A new playlist {new_playlist["title"]} has been created!
            Check it out here: {new_playlist['external_urls']['spotify']}"""

    logger.info(user_message)
    return user_message

    # # create the playlist
    # new_playlist = spotify_client.spotify.user_playlist_create(
    #     user=spotify_client.spotify.current_user()["id"],
    #     name=playlist.title,
    #     public=True,
    #     collaborative=False,
    #     description=playlist.description,
    # )

    # # retrieve the playlist details to get the playlist ID
    # playlists = spotify_client.spotify.user_playlists(user=spotify_client.spotify.current_user()["id"])
    # created_playlist = next((p for p in playlists["items"] if p["name"] == playlist.title), None)

    # if not created_playlist:
    #     raise ValueError(f"Could not find playlist '{playlist.title}'")

    # # add the tracks to the playlist
    # spotify_client.spotify.user_playlist_add_tracks(
    #     user=spotify_client.spotify.current_user()["id"],
    #     playlist_id=created_playlist["id"],
    #     tracks=playlist.playlist,
    # )

    # user_message = f"""A new playlist {created_playlist["name"]} has been created!
    #     Check it out here: {created_playlist['external_urls']['spotify']}"""

    # logger.info(user_message)
    # return created_playlist["id"]
