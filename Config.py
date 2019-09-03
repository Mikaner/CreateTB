import json


class Config:
    def __init__(self):
        with open("./config/config.json", 'r', encoding="utf-8") as code:
            self.config = json.load(code)

    def get_token(self):
        return self.config["token"]

    def get_API_key(self):
        return self.config["APIKey"]

    def get_prefix(self):
        return self.config["prefix"]

    def get_spotify_client_id(self):
        return self.config["spotify_client_id"]

    def get_spotify_client_secret(self):
        return self.config["spotify_client_secret"]