import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from music.MusicCog import MusicCog
import json
import traceback

INITIAL_COGS = [
    MusicCog
]


class MainTB(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        with open('./config/config.json','r',encoding='utf-8') as tokenCode:
            self.config = json.load(tokenCode)

        self.remove_command('help')

        for cog in INITIAL_COGS:
            try:
                self.add_cog(cog(self))
            except Exception:
                traceback.print_exc()


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('---message---')

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("No such command")
            return
        raise error

    def token(self):
        return self.config["token"]
        
        



if __name__ == "__main__":
    with open('./config/config.json','r',encoding='utf-8') as tokenCode:
        config = json.load(tokenCode)
    TB = MainTB(command_prefix=config["prefix"])
    TB.run(TB.token())
