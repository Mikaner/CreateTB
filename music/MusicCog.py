import discord
from discord.ext import commands
from .Setting import Settings
import json

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None

    @commands.command()
    async def join(self, ctx):
        voice_channel = ctx.guild.voice_channels[0]
        self.voice_client = await voice_channel.connect()

    @commands.command()
    async def play(self, ctx):
        if self.voice_client == None:
            voice_channel = ctx.guild.voice_channels[0]
            self.voice_client = await voice_channel.connect()

        audio_source = discord.FFmpegPCMAudio('local_music_files/MikeTest.mp3')
        if not self.voice_client.is_playing():
            self.voice_client.play(audio_source, after=lambda e: print('done', e))
        
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
        setting = Settings()

        embed = discord.Embed(title='TB', description="A music bot. List of commands are:", color=0xeee657)

        for name, description in setting.settings['commands']:
            embed.add_field(name=name, value=description, inline=False)

        await ctx.send(embed=embed)


if __name__ == '__main__':
    prefix = "$"
    bot = commands.Bot(command_prefix=prefix, description='music bot')

    with open('../config/config.json', 'r', encoding='utf-8') as tokenCode:
        token = json.load(tokenCode)

    bot.remove_command('help')
    bot.add_cog(MusicCog(bot))
    bot.run(token["token"])