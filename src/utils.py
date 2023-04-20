"""Utility functions and classes used in other scripts."""

import json

import spotipy
from google.cloud import secretmanager
from spotipy.oauth2 import CacheHandler, SpotifyOAuth


def extract_json_from_response(response: str) -> str:
    """Extract the json from the response.

    Args:
        response (str): The response from the assistant.

    Returns:
        str: The extracted json.
    """
    json_str = response.strip("`").strip().replace("\n", "")
    return json.loads(json_str)


class SpotifyClient:
    """Class that instantiates a Spotify client to interact with the API."""

    def __init__(self) -> None:
        cid = self.access_secret_version("projects/420207002838/secrets/SPOTIFY_CLIENT_ID/versions/1")
        secret = self.access_secret_version("projects/420207002838/secrets/SPOTIFY_CLIENT_SECRET/versions/1")
        redirect_uri = self.access_secret_version("projects/420207002838/secrets/SPOTIFY_REDIRECT_URI/versions/latest")

        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=cid,
                client_secret=secret,
                redirect_uri=redirect_uri,
                cache_handler=GoogleCacheHandler(),
                scope="playlist-modify-public",
            )
        )

    @staticmethod
    def access_secret_version(secret_version_id: str) -> str:
        """Return the value of a secret's version.

        Args:
            secret_version_id: the id of the secret version in the secret manager

        Returns:
            object: the secret decoded in utf-8
        """
        client = secretmanager.SecretManagerServiceClient()

        response = client.access_secret_version(name=secret_version_id)

        return response.payload.data.decode("UTF-8")


class GoogleCacheHandler(CacheHandler):
    """Class with custom implementation of Spotipy's CacheHandler.

    This implementation loads and saves the cached access tokens to GCP.
    """

    def get_cached_token(self) -> dict:
        """Get and return a token_info dictionary object."""
        return json.loads(
            SpotifyClient.access_secret_version("projects/420207002838/secrets/DOT-CACHE/versions/latest")
        )

    def save_token_to_cache(self, token_info: dict) -> None:
        """Save a token_info dictionary object to the cache and return None."""
        # TO-DO: update dot-cache with refreshed token
        return None