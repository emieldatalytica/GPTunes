"""Utility functions and classes used in other scripts."""

import json
import logging
import os

import dirtyjson
import spotipy
from google.cloud import secretmanager
from pydantic import BaseModel, Field
from spotipy.oauth2 import CacheHandler, SpotifyOAuth


class Playlist(BaseModel):
    """Class to represent a playlist."""

    title: str
    description: str = Field(max_length=1000)
    cover_image: str
    tracks: list


def get_logger(name: str) -> logging.Logger:
    """Instantiate a logger object with the given name.

    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: The logger object.
    """
    func_logger = logging.getLogger(name)
    func_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    func_logger.addHandler(stream_handler)
    return func_logger


logger = get_logger(__name__)


def extract_json_from_response(response: str) -> dict:
    """Extract the json from the response.

    Args:
        response (str): The response from the assistant.

    Returns:
        dict: The extracted json.
    """
    json_str = response.strip("`").strip().replace("\n", "")
    return dirtyjson.loads(json_str)


class SpotifyClient:
    """Class that instantiates a Spotify client to interact with the Spotify API."""

    def __init__(self) -> None:
        """Initialize the Spotify client.

        Raises:
            ValueError: If the environment variables are not set.
        """
        self.env_id = str(os.getenv("ENV_ID"))
        if self.env_id == "None":
            raise ValueError("env_id must be set. Are environment variables set and loaded correctly?")
        cid = self.access_secret_version(self.env_id, "SPOTIFY_CLIENT_ID")
        secret = self.access_secret_version(self.env_id, "SPOTIFY_CLIENT_SECRET")
        redirect_uri = self.access_secret_version(self.env_id, "SPOTIFY_REDIRECT_URI")
        scope = "playlist-modify-public ugc-image-upload"

        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=cid,
                client_secret=secret,
                redirect_uri=redirect_uri,
                cache_handler=GoogleCacheHandler(env_id=self.env_id),
                scope=scope,
            )
        )

        logger.info("Spotify client instantiated.")

    @staticmethod
    def access_secret_version(env_id: str, secret_name: str) -> str:
        """Return the value of a secret's version.

        Args:
            env_id (str): The environment ID of the secret.
            secret_name (str): The name of the secret.

        Returns:
            object: the secret decoded in utf-8
        """
        client = secretmanager.SecretManagerServiceClient()
        secret_version_id = f"projects/{env_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(name=secret_version_id)
        return response.payload.data.decode("UTF-8")


class GoogleCacheHandler(CacheHandler):
    """Class with custom implementation of Spotipy's CacheHandler.

    This implementation loads and saves the cached access tokens to GCP.
    """

    def __init__(self, env_id: str) -> None:
        super().__init__()
        self.env_id = env_id

    def get_cached_token(self) -> dict:
        """Get and return a token_info dictionary object."""
        logger.info("Getting cached token from GCP.")
        return json.loads(SpotifyClient.access_secret_version(self.env_id, "DOT-CACHE"))

    def save_token_to_cache(self, token_info: dict) -> None:
        """Save a token_info dictionary object to the cache and return None."""
        logger.info("Saving cached token locally.")
        # write cache to local file
        with open(".cache", "w") as file:
            file.write(json.dumps(token_info))
        return None


spotify_client = SpotifyClient()
