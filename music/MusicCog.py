import discord
from discord.ext import commands
from music.Setting import Settings
from music.Download import Download
from music.Queue import Queue
import json
from discord.ext.commands import CommandNotFound
import urllib.parse as urlparse
import os


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.Q = Queue()
        self.setting = Settings()
        self.now_playing = None
        self.is_queue_looped = False
        self.download = Download()
        self.beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        self.devnull = open(os.devnull, 'w')

    def is_url_valid(self, url):
        if url.startswith('https://www.youtube.com/watch?v='):
            return (True, 'youtube')
        elif url.startswith('https://www.nicovideo.jp/watch/sm'):
            return (True, 'niconico')
        else:
            return (False, '')
    
    def is_local(self, url):    
        if url.startswith('http'):
            return False
        else:
            return True

    def show_now_playing(self, ctx):
        embed = discord.Embed(title='Now Playing', color=0x00bfff)
        embed.add_field(name='now playing', value=self.now_playing, inline=False)

        return ctx.send(embed=embed)

    def status_queue(self, ctx):
        embed = discord.Embed(title='Status of Queue', description="In queue :", color=0x00bfff)
        for index, job in enumerate(self.Q.get_queue()):
            embed.add_field(name=index+1, value=job, inline=False)

        return ctx.send(embed=embed)

    def next(self):# need to adjust
        print('load next audio')
        if self.Q.get_queue() == []:
            print("done")
            return
        
        if self.is_queue_looped:
            self.Q.add_queue(self.now_playing)
        
        self.now_playing = self.Q.next_job()

        if self.is_local(self.now_playing):
            self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing), after=lambda e: self.next())
        else:
            self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing, stderr=self.devnull, before_options=self.beforeArgs), after=lambda e: self.next())

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
                return

            self.voice_client = await voice_channel.connect()

        if len(args) == 0:
            self.Q.add_queue('music/local_music_files/MikeTest.mp3')
        elif len(args) == 1:
            # assert args is url
            is_valid, service = self.is_url_valid(args[0])
            if is_valid:
                if service == 'youtube':
                    #file_path = self.download.youtube_stream(args, self.setting.settings['download_file_ext'])
                    self.Q.add_queue(self.download.youtube_stream(args, self.setting.settings['download_file_ext']))
                elif service == 'niconico':
                    file_path = self.download.niconico_dl(args, self.setting.settings['download_file_ext'])
                    self.Q.add_queue(file_path)
            else:
                # assert args is search words
                pass
        else:
            # assert args is search words
            pass

        if not self.voice_client.is_playing():
            self.now_playing = self.Q.next_job()
            if self.is_local(self.now_playing):
                self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing), after=lambda e: self.next())
            else:
                self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing, stderr=self.devnull, before_options=self.beforeArgs), after=lambda e: self.next())

    @commands.command()
    async def loopqueue(self, ctx):
        self.is_queue_looped = not self.is_queue_looped

        if self.is_queue_looped:
            await ctx.send("Enabled loopqueue")
            return
        else:
            await ctx.send('Disabled loopqueue')
            return

    @commands.command()
    async def nowplaying(self, ctx):

        await self.show_now_playing(ctx)
    
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
        await self.show_now_playing(ctx)
        await self.status_queue(ctx)

    @commands.command()
    async def clear(self,ctx):
        self.Q.queue_clear()
        await self.status_queue(ctx)
        await ctx.send("Queue cleared!")

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

    @commands.command(name="logoutTB")
    async def logout(self,ctx):
        await ctx.bot.logout()
        exit()







if __name__ == '__main__':
    prefix = "$"
    bot = commands.Bot(command_prefix=prefix, description='music bot')

    with open('config/config.json', 'r', encoding='utf-8') as tokenCode:
        token = json.load(tokenCode)

    bot.remove_command('help')
    bot.add_cog(MusicCog(bot))
    bot.run(token["token"])