import discord
from discord.ext import commands

import json
import traceback

INITIAL_COGS = [
    'music.MusicCog'
]


class MainTB(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('---message---')

    def token(self):
        with open('./config/config.json','r',encoding='utf-8') as tokenCode:
            self.tokens = json.load(tokenCode)
        return self.tokens["token"]



if __name__ == "__main__":
    prefix = "$"

    TB = MainTB(command_prefix=prefix)
    TB.run(TB.token())
