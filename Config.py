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
