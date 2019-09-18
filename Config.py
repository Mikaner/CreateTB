import json
import os

class Config:
    def __init__(self):
        self._prefix = os.environ.get("PREFIX")
        self._redis_url = os.environ.get("REDIS_URL")
        self._bot_token = os.environ.get("BOT_TOKEN")
        self._google_api_key = os.environ.get("GOOGLE_API_KEY")
        self._spotify_client_key = os.environ.get("SPOTIFY_CLIENT_KEY")
        self._spotify_client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    def get_token(self):
        return self._bot_token

    def get_api_key(self):
        return self._google_api_key

    def get_prefix(self):
        return self._prefix

    def get_redis_url(self):
        return self._redis_url

    def get_spotify_client_id(self):
        return self._spotify_client_key

    def get_spotify_client_secret(self):
        return self._spotify_client_secret