"""Utility functions and classes used in other scripts."""

import spotipy
from google.cloud import secretmanager
from spotipy.oauth2 import SpotifyClientCredentials


def extract_json_from_response(response: str) -> str:
    """Extract the json from the response.

    Args:
        response (str): The response from the assistant.

    Returns:
        str: The extracted json.
    """
    start = response.find("```") + 3
    end = response.find("```", start)
    return response[start:end]


class SpotifyClient:
    """Class that instantiates a Spotify client to interact with the API."""

    def __init__(self) -> None:
        cid = self.access_secret_version("projects/420207002838/secrets/SPOTIFY_CLIENT_ID/versions/1")
        secret = self.access_secret_version("projects/420207002838/secrets/SPOTIFY_CLIENT_SECRET/versions/1")
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

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
