import discord
from discord.ext import commands
from music.Setting import Settings
from music.Download import Download
from music.Queue import Queue
import json
from discord.ext.commands import CommandNotFound
import urllib.parse as urlparse


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.Q = Queue()
        self.setting = Settings()
        self.download = Download()

    def is_url_valid(self, url):
        if url.startswith('https://www.youtube.com/watch?v='):
            return (True, 'youtube')
        elif url.startswith('https://www.nicovideo.jp/watch/sm'):
            return (True, 'niconico')
        else:
            return (False, '')
        

    def status_queue(self, ctx):
        embed = discord.Embed(title='TB', description="The state of Queue:", color=0x00bfff)
        for index, job in enumerate(self.Q.get_queue()):
            embed.add_field(name=index+1, value=job, inline=False)

        return ctx.send(embed=embed)

    def next(self):# need to adjust
        if self.Q.get_queue() == []:
            print("done")
            return
        #self.voice_client.play(self.Q.next_job(), after=self.next)

    @commands.command()
    async def join(self, ctx):

        if self.voice_client is not None and self.voice_client.is_connected():
            await self.voice_client.disconnect()

        if ctx.author.voice is not None:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send('Please join a voice channel before using $join')
            return

        self.voice_client = await voice_channel.connect()

    @commands.command()
    async def play(self, ctx, *args):
        if self.voice_client is None:
            if ctx.author.voice is not None:
                voice_channel = ctx.author.voice.channel
            else:
                await ctx.send('Please join a voice channel before using $play')

            self.voice_client = await voice_channel.connect()

        if len(args) == 0:
            self.Q.add_queue(discord.FFmpegPCMAudio('music/local_music_files/MikeTest.mp3'))
        elif len(args) == 1:
            # assert args is url
            is_valid, service = self.is_url_valid(args[0])
            if is_valid:
                if service == 'youtube':
                    file_path = self.download.youtube_stream(args, self.setting.settings['download_file_ext'])
                    self.Q.add_queue(discord.FFmpegPCMAudio(file_path))
                elif service == 'niconico':
                    file_path = self.download.niconico_dl(args, self.setting.settings['download_file_ext'])
                    self.Q.add_queue(discord.FFmpegPCMAudio(file_path))
            else:
                # assert args is search words
                pass
        else:
            # assert args is search words
            pass

        if not self.voice_client.is_playing():
            self.voice_client.play(self.Q.next_job(), after=self.next)
        
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
    async def remove(self, ctx, position):
        if self.voice_client is None:
            return
        if int(position)==0:
            self.voice_client.stop()
        else:
            try:
                self.Q.remove_queue(int(position))
            except IndexError:
                await ctx.send("Out of queue.")

            finally:
                await self.status_queue(ctx)

    @commands.command()
    async def move(self,ctx,from_position,to_position):
        self.Q.move_queue(int(from_position),int(to_position))
        await self.status_queue(ctx)

    @commands.command()
    async def queue(self,ctx):
        await self.status_queue(ctx)


    @commands.command()
    async def disconnect(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_connected():
            await self.voice_client.disconnect()

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(title='TB', description="A music bot. List of commands are:", color=0x00bfff)

        for name, description in self.setting.settings['commands']:
            embed.add_field(name=name, value=description, inline=False)

        await ctx.send(embed=embed)






if __name__ == '__main__':
    prefix = "$"
    bot = commands.Bot(command_prefix=prefix, description='music bot')

    with open('config/config.json', 'r', encoding='utf-8') as tokenCode:
        token = json.load(tokenCode)

    bot.remove_command('help')
    bot.add_cog(MusicCog(bot))
    bot.run(token["token"])