import discord
from discord.ext import commands
from music.Setting import Settings
from music.Download import Download
from music.Queue import Queue
from discord.ext.commands import CommandNotFound
import os
from apiclient.errors import HttpError
from pathlib import Path
import re


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
        # Pathを使ってみたいということで編集中
        # ディレクトリトラバーサルはlist指定型で防ごうと思います
        self.local = Path("./music/local_music_file/")
        self.files = os.listdir("music/local_music_files")
        # thumbnailを使うとは言っていない
        self.local_thumbnail = "./music/local_music_file/thumbnail.png"


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
        embed = discord.Embed(title='Now Playing', description=self.now_playing["title"], color=0x00bfff)
        if self.now_playing["thumbnail"] is not None:
            embed.set_thumbnail(url=self.now_playing["thumbnail"])

        return ctx.send(embed=embed)

    def status_queue(self, ctx):
        embed = discord.Embed(title='Status of Queue', description="In queue :", color=0x00bfff)
        for index, job in enumerate(self.Q.get_queue()):
            embed.add_field(name=str(index+1)+" : "+job["title"], value=job["author"], inline=True)

        return ctx.send(embed=embed)

    def next(self):# need to adjust
        if self.is_queue_looped:
            self.Q.add_queue(self.now_playing)

        if self.Q.get_queue() == []:
            print("done Now Queue is empty")
            return
        
        print('load next audio')
        
        self.now_playing = self.Q.next_job()

        if self.is_local(self.now_playing["url"]):
            self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing["url"]), after=lambda e: self.next())
        else:
            self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing["url"], stderr=self.devnull, before_options=self.beforeArgs), after=lambda e: self.next())

    @commands.command()
    async def join(self, ctx):

        if self.voice_client is not None and self.voice_client.is_connected():
            await self.voice_client.disconnect()

        if ctx.author.voice is None:
            await ctx.send(embed=discord.Embed(title='Please join a voice channel before $join', colour=0x00bfff))
            return

        voice_channel = ctx.author.voice.channel
        self.voice_client = await voice_channel.connect()
        await ctx.send(embed=discord.Embed(title=f"Successfuly connected to {self.voice_client.channel} ! :thumbsup:", colour=0x00bfff))

    @commands.command()
    async def show_local_file(self, ctx, *args):
        try:
            page = int(args[0])-1 if len(args) != 0 else 0
        except TypeError:
            await ctx.send("TypeError")
        embed = discord.Embed(title="My local files")
        # Page processing
        if -1 < page <= (len(self.files)//20):
            for i in range(page*20, (page+1)*20 if len(self.files) > (page+1)*20 else len(self.files)):
                embed.add_field(name=self.files[i],value=self.local)
        else:
            await ctx.send(embed=discord.Embed(title="OutOfPage", colour=0xff0000))
            return

        await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx, *args):
        if self.voice_client is None:
            if ctx.author.voice is None:
                await ctx.send(embed=discord.Embed(title='Please join a voice channel before $join', colour=0x00bfff))
                return
            
            voice_channel = ctx.author.voice.channel
            self.voice_client = await voice_channel.connect()
            await ctx.send(embed=discord.Embed(title=f"Successfuly connected to {self.voice_client.channel} ! :thumbsup:", colour=0x00bfff))

        if len(args) == 0:
            print("test")
            self.Q.add_queue({"url":'./music/local_music_files/MikeTest.mp3',"title":"MikeTest.mp3","thumbnail":None,"author":"Mikaner"})

        elif len(args) == 1:
            print("1",args)
            # assert args is url
            is_valid, service = self.is_url_valid(args[0])
            if is_valid:
                if service == 'youtube':
                    self.Q.add_queue(self.download.youtube_stream(args, self.setting.settings['download_file_ext']))
                elif service == 'niconico':
                    self.Q.add_queue(self.download.niconico_dl(args, self.setting.settings['download_file_ext']))

            else:
                # assert args is search words
                print("search1 ", args)
                try:
                    url = self.download.youtube_search(" ".join(args))
                    await ctx.send(url)
                except HttpError:
                    await ctx.send("Http Error occured")
                    return
                    
                self.Q.add_queue(self.download.youtube_stream([url], self.setting.settings['download_file_ext']))

        elif args[0] == '-l':
            # play local file
            print("play local",args)
            file_name = " ".join(args[1::])
            files = [n for n in self.files if file_name in n]
            if len(files)==1:
                self.Q.add_queue({"url":'./music/local_music_files'+self.files[self.files.index(files[0])],"title":self.files[self.files.index(files[0])][:len(file_name)-4:], "thumbnail":None, "author":"Cannot read, please wait."})
            else:
                await ctx.send(f"Which file would you like to listen {', '.join(files)} ?")
                return

        else:
            print("search2 ",args)
            # assert args is search words
            try:
                url = self.download.youtube_search(" ".join(args))
                await ctx.send(url)
            except HttpError:
                await ctx.send("Http Error occured")
                return

            self.Q.add_queue(self.download.youtube_stream([self.download.youtube_search(" ".join(args))], self.setting.settings['download_file_ext']))

        add = self.Q.get_queue()[-1]
        embed = discord.Embed(title="Added to queue !",description=add["title"], colour=0x00bfff)
        if add["thumbnail"] is not None:
            embed.set_thumbnail(url=add["thumbnail"])
        embed.set_author(name=add["author"])
        await ctx.send(embed=embed)


        if not self.voice_client.is_playing():
            self.now_playing = self.Q.next_job()
            if self.is_local(self.now_playing["url"]):
                self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing["url"]), after=lambda e: self.next())
            else:
                self.voice_client.play(discord.FFmpegPCMAudio(self.now_playing["url"], stderr=self.devnull, before_options=self.beforeArgs), after=lambda e: self.next())

    @commands.command()
    async def loopqueue(self, ctx):
        self.is_queue_looped = not self.is_queue_looped

        if self.is_queue_looped:
            embed = discord.Embed(title='Enabled loopqueue', colour=0x47ea7e)
        else:
            embed = discord.Embed(title='Disabled loopqueue', colour=0xff0000)

        await ctx.send(embed=embed)

    @commands.command()
    async def nowplaying(self, ctx):
        await self.show_now_playing(ctx)

    @commands.command()
    async def stop(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_playing():
            self.voice_client.pause()
            await ctx.send(embed=discord.Embed(title="Paused", colour=0x47ea7a))


    @commands.command()
    async def start(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_paused():
            self.voice_client.resume()
            await ctx.send(embed=discord.Embed(title="Resumed", colour=0x47ea7a))

    @commands.command()
    async def skip(self, ctx):
        if self.voice_client is None:
            return
        await ctx.send(embed=discord.Embed(title=self.now_playing["title"]+' was skipped', colour=0x47ea7a))
        self.voice_client.stop()

    @commands.command()
    async def remove(self, ctx, position):
        if self.voice_client is None:
            return
        try:
            if int(position)==0:
                await ctx.send(embed=discord.Embed(title=self.now_playing["title"]+' was skipeed', colour=0x47ea7a))
                self.voice_client.stop()
                return
            position = self.Q.convert_value(int(position))
        except TypeError:
            await ctx.send(embed=discord.Embed(title="Type Error",description="Please type integer", colour=0xff0000))
            return

        try:
            await ctx.send(embed=discord.Embed(title='Removed the '+self.Q.remove_queue(int(position))["title"], colour=0x47ea7a))

        except IndexError:
            await ctx.send(embed=discord.Embed(title="Out of queue.", colour=0xff0000))

        finally:
            await self.show_now_playing(ctx)
            await self.status_queue(ctx)

    @commands.command()
    async def move(self,ctx,from_position,to_position):
        try:
            if int(from_position)==0 or int(to_position)==0:
                await self.ctx.send(embed=discord.Embed(title="Out of queue.", colour=0xff0000))
                return
            from_position, to_position = self.Q.convert_value(int(from_position)), self.Q.convert_value(int(to_position))
        except TypeError:
            await ctx.send(embed=discord.Embed(title="Type Error",description="Please type integer", colour=0xff0000))
            return

        try:
            await ctx.send(embed=discord.Embed(title='Moved ' + self.Q.get_queue()[int(from_position)]["title"] + ' to ' + str(to_position if to_position < 0 else to_position+1), colour=0x47ea7a))
            self.Q.move_queue(int(from_position), int(to_position))
        except IndexError:
            await ctx.send(embed=discord.Embed(title="Out of queue", colour=0xff0000))
        finally:
            await self.status_queue(ctx)

    @commands.command()
    async def queue(self,ctx):
        await self.show_now_playing(ctx)
        await self.status_queue(ctx)

    @commands.command()
    async def clear(self,ctx):
        self.Q.queue_clear()
        await self.status_queue(ctx)
        await ctx.send(embed=discord.Embed(title="Queue cleared!", colour=0x47ea7a))

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
    config = Config()
    bot = commands.Bot(command_prefix=config.get_prefix(), description='music bot')

    bot.remove_command('help')
    bot.add_cog(MusicCog(bot))
    bot.run(config.get_token())
