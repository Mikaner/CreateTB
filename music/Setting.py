import json

class Settings:
    def __init__(self):
        with open('music/settings.json', 'r', encoding='utf-8') as setting_json:
            self.settings = json.load(setting_json)
        
    def volume(self):
        pass

    def get_help_text(self):
        return self.settings.commands