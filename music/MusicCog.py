import discord
from discord.ext import commands
from music.Setting import Settings
from music.Download import Download
import json
from discord.ext.commands import CommandNotFound
import urllib.parse as urlparse


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.setting = Settings()

    @commands.command()
    async def join(self, ctx):

        if self.voice_client is not None and self.voice_client.is_connected():
            await self.voice_client.disconnect()

        if ctx.author.voice is not None:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send('Join a voice channel before using $join')
            return

        self.voice_client = await voice_channel.connect()

    @commands.command()
    async def play(self, ctx, *args):
        if self.voice_client is None:
            # if not joined
            if ctx.author.voice is not None:
                voice_channel = ctx.author.voice.channel
            else:
                await ctx.send('Join a voice channel before using $play')

            self.voice_client = await voice_channel.connect()

        if len(args) == 0:
            audio_source = discord.FFmpegPCMAudio('music/local_music_files/MikeTest.mp3')
        elif len(args) == 1:
            # assert args is url
            is_valid, service = self.is_url_valid(args[0])
            if is_valid:
                if service == 'youtube':
                    download = Download()
                    file_path = download.youtube_dl(args, self.setting.settings['download_file_ext'])
                    audio_source = discord.FFmpegPCMAudio(file_path)
                elif service == 'niconico':
                    pass
            else:
                # assert args is search words
                pass
            
        else:
            # assert args is search words
            pass
        if not self.voice_client.is_playing():
            self.voice_client.play(audio_source, after=lambda e: print('done', e))
        
    @commands.command()
    async def stop(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_playing():
            self.voice_client.pause()

    @commands.command()
    async def start(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_paused():
            self.voice_client.resume()

    @commands.command()
    async def skip(self, ctx):
        if self.voice_client is None:
            return
        self.voice_client.stop()

    @commands.command()
    async def remove(self, ctx):
        if self.voice_client is None:
            return
        self.voice_client.stop()

    @commands.command()
    async def disconnect(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_connected():
            await self.voice_client.disconnect()

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(title='TB', description="A music bot. List of commands are:", color=0xeee657)

        for name, description in self.setting.settings['commands']:
            embed.add_field(name=name, value=description, inline=False)

        await ctx.send(embed=embed)

    def is_url_valid(self, url):
        if url.startswith('https://www.youtube.com/watch?v='):
            return (True, 'youtube')
        elif url.startswith('https://www.nicovideo.jp/watch/sm'):
            return (True, 'niconico')
        else:
            return (False, '')
        

if __name__ == '__main__':
    prefix = "$"
    bot = commands.Bot(command_prefix=prefix, description='music bot')

    with open('config/config.json', 'r', encoding='utf-8') as tokenCode:
        token = json.load(tokenCode)

    bot.remove_command('help')
    bot.add_cog(MusicCog(bot))
    bot.run(token["token"])