"""This script is intended to be used to authenticate with Spotify and generate a cache file for the Spotify API.

You can run it from the command line like this:
python authenticate_spotify.py --env dev # or main
"""

import argparse
import json
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import CacheHandler, SpotifyOAuth


class RefreshCacheHandler(CacheHandler):
    """Class with custom implementation of Spotipy's CacheHandler.

    This implementation forces the caller to authenticate manually with Spotify and generate a fresh cache file.
    """

    def __init__(self) -> None:
        super().__init__()

    def get_cached_token(self) -> None:
        return None

    def save_token_to_cache(self, token_info: dict) -> None:
        """Save a token_info dictionary object to the cache and return None."""
        # logger.info("Saving cached token locally.")
        # write cache to local file
        with open(".cache", "w") as file:
            file.write(json.dumps(token_info))
        return None


def spotify_auth(env: str) -> None:
    """Authenticate with Spotify and generate a cache file.

    Args:
        env (str): The environment to use for loading the correct environment variables.
    """
    # load the correct .env file based on the env argument
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"infra/envs/{env}/.env")
    load_dotenv(dotenv_path=dotenv_path)

    # load environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID_VERSION")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET_VERSION")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scope = "playlist-modify-public ugc-image-upload"

    # authenticate with Spotify
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            cache_handler=RefreshCacheHandler(),
            scope=scope,
        )
    )

    # this should open a browser window for you to authenticate with Spotify and generate a cache file
    sp.current_user()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get environment for Spotify authentication.")
    parser.add_argument("--env", type=str, help="Environment for Spotify authentication (dev/main)", required=True)
    args = parser.parse_args()

    spotify_auth(args.env)  # Pass env argument from command line
