"""Utility functions and classes used in other scripts."""

import argparse
import ast
import json
import logging
import os

import spotipy
from google.cloud import secretmanager
from pydantic import BaseModel, Field
from spotipy.oauth2 import CacheHandler, SpotifyOAuth


class Playlist(BaseModel):
    """Class to represent a playlist."""

    title: str
    description: str = Field(max_length=300)
    playlist: list


def get_logger(name: str) -> logging.Logger:
    """Instantiate a logger object with the given name.

    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: The logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


logger = get_logger(__name__)


def extract_json_from_response(response: str) -> dict:
    """Extract the json from the response.

    Args:
        response (str): The response from the assistant.

    Returns:
        dict: The extracted json.
    """
    json_str = response.strip("`").strip().replace("\n", "")
    return json.loads(json_str)


class SpotifyClient:
    """Class that instantiates a Spotify client to interact with the API."""

    def __init__(self, env: str = "dev", refresh_token: bool = False) -> None:
        """Initialize the Spotify client.

        Args:
            env (str, optional): The environment to use. Defaults to "dev".
            refresh_token (bool, optional): Whether to refresh the token. Defaults to False.

        Raises:
            ValueError: If env is not "dev" or "main".
        """
        # TO-DO: add support for main environment
        if env == "dev":
            self.env_id = str(os.getenv("GPTUNES_DEV_ENV_ID"))
        elif env == "main":
            self.env_id = str(os.getenv("GPTUNES_MAIN_ENV_ID"))
        else:
            raise ValueError("env must be either 'dev' or 'main'")
        cid = self.access_secret_version(self.env_id, "SPOTIFY_CLIENT_ID", 2)
        secret = self.access_secret_version(self.env_id, "SPOTIFY_CLIENT_SECRET", 1)
        redirect_uri = self.access_secret_version(self.env_id, "SPOTIFY_REDIRECT_URI", 1)
        scope = "playlist-modify-public"

        if refresh_token:
            logger.info("Prompting user for token, wait for browser to open.")
            token = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=cid,
                    client_secret=secret,
                    redirect_uri=redirect_uri,
                    scope=scope,
                )
            )
            logger.info(f"Token: type: {type(token)}, {token}, ")
            logger.info("Token has been refreshed.")
        else:
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
    def access_secret_version(env_id: str, secret_name: str, version: int) -> str:
        """Return the value of a secret's version.

        Args:
            env_id (str): The environment ID of the secret.
            secret_name (str): The name of the secret.
            version (int): The version of the secret.

        Returns:
            object: the secret decoded in utf-8
        """
        client = secretmanager.SecretManagerServiceClient()
        secret_version_id = f"projects/{env_id}/secrets/{secret_name}/versions/{version}"
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
        return json.loads(SpotifyClient.access_secret_version(self.env_id, "DOT-CACHE", 2))

    def save_token_to_cache(self, token_info: dict) -> None:
        """Save a token_info dictionary object to the cache and return None."""
        # TO-DO: update dot-cache with refreshed token
        return None


spotify_client = SpotifyClient()  # tmp

# code that uses argparse to parse argument 'refresh_token'
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-rt",
        "--refresh_token",
        type=str,
        dest="refresh_token",
        required=True,
        choices=["True", "False"],
        help="Boolean indicating whether to refresh the spotipy .cache token.",
    )
    args = parser.parse_args()
    logger.info(f"Script invoked with args: {args}")
    spotify_client = SpotifyClient(refresh_token=ast.literal_eval(args.refresh_token))
else:
    spotify_client = SpotifyClient()
