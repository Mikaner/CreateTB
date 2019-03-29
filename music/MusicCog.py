import discord
from discord.ext import commands
from music.Setting import Settings
from music.Download import Download
from music.Queue import Queue
import json
from discord.ext.commands import CommandNotFound

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.Q = Queue()
        self.bot = bot
        self.voice_client = None

    @commands.command()
    async def join(self, ctx):

        if self.voice_client is not None and self.voice_client.is_connected():
            await self.voice_client.disconnect()

        if ctx.author.voice.channel is not None:
            voice_channel = ctx.author.voice.channel
        else:
            voice_channel = ctx.guild.voice_channels[0]
        self.voice_client = await voice_channel.connect()

    @commands.command()
    async def play(self, ctx, *args):
        if self.voice_client is None:
            # if not joined
            if ctx.author.voice.channel is not None:
                voice_channel = ctx.author.voice.channel
            else:
                voice_channel = ctx.guild.voice_channels[0]
                
            self.voice_client = await voice_channel.connect()

        await ctx.send(args)
        audio_source = discord.FFmpegPCMAudio('music/local_music_files/MikeTest.mp3')
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
    async def remove(self, ctx, position):
        if self.voice_client is None:
            return
        if position==0:
            self.voice_client.stop()
        else:
            try:
                self.Q.remove_queue(position)
            except IndexError:
                await ctx.send("Out of queue.")

            finally:
                await status_queue(ctx)

    @commands.command()
    async def move(self,ctx,from_position,to_position):
        self.Q.move_queue(from_position,to_position)


    @commands.command()
    async def disconnect(self, ctx):
        if self.voice_client is None:
            return
        if self.voice_client.is_connected():
            await self.voice_client.disconnect()

    @commands.command()
    async def help(self, ctx):
        setting = Settings()

        embed = discord.Embed(title='TB', description="A music bot. List of commands are:", color=0xeee657)

        for name, description in setting.settings['commands']:
            embed.add_field(name=name, value=description, inline=False)

        await ctx.send(embed=embed)

    def status_queue(self, ctx):
        embed = discord.Embed(title='TB', description="The state of Queue:", color=0x00bfff)
        for index, job in enumerate(self.Q.get_queue()):
            embed.add_field(name=index, value=job, inline=False)

        return ctx.send(embed=embed)


if __name__ == '__main__':
    prefix = "$"
    bot = commands.Bot(command_prefix=prefix, description='music bot')

    with open('config/config.json', 'r', encoding='utf-8') as tokenCode:
        token = json.load(tokenCode)

    bot.remove_command('help')
    bot.add_cog(MusicCog(bot))
    bot.run(token["token"])