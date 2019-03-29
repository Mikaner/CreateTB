import discord
from discord.ext import commands
from Setting import Settings
import json

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    @commands.command()
    async def join(self, ctx):
        pass

    @commands.command()
    async def play(self, ctx):
        pass

    @commands.command()
    async def stop(self, ctx):
        pass

    @commands.command()
    async def start(self, ctx):
        pass

    @commands.command()
    async def skip(self, ctx):
        pass

    @commands.command()
    async def remove(self, ctx):
        pass

    @commands.command()
    async def disconnect(self, ctx):
        pass

    @commands.command()
    async def help(self, ctx):
        pass


if __name__ == '__main__':
    prefix = "$"
    bot = commands.Bot(command_prefix=prefix, description='music bot')
    with open('../config/config.json', 'r', encoding='utf-8') as tokenCode:
        token = json.load(tokenCode)

    bot.add_cog(MusicCog(bot))
    bot.run(token["token"])