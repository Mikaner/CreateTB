import discord
from discord.ext import commands
import json
import settings

prefix = "$"
voice_client = None

bot = commands.Bot(command_prefix=prefix, description='A bot that greets the user back.')
with open('./config/config.json','r',encoding='utf-8') as tokenCode:
    token = json.load(tokenCode)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---message---')


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)


@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)


@bot.command()
async def ping(ctx):
    """
    This test will be shown in the help command
    """
    latency = bot.latency

    await ctx.send(latency)


bot.remove_command('help')
@bot.command()
async def help(ctx):
    """
    This command will show the all commands this bot has
    """

    help_text = ""

    for command, description in settings.commands:
        help_text += "- " + command + " - " + description + "\n"

    await ctx.send(help_text)


@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: こんにちは！ :wave:")

@bot.command()
async def join(ctx):
    global voice_client
    voice_channel = ctx.guild.voice_channels[0]
    voice_client = await voice_channel.connect()

@bot.command()
async def play(ctx):
    global voice_client
    if voice_client==None:
        #join(ctx) <- 'Command' object is not callable
        voice_channel = ctx.guild.voice_channels[0]
        voice_client = await voice_channel.connect()
    audio_source = discord.FFmpegPCMAudio("./music/secret/14 TODAY THE FUTURE Magical Mirai ver.wma")
    if not voice_client.is_playing():
        voice_client.play(audio_source)


@bot.command()
async def stop(ctx):
    global voice_client
    if voice_client==None:
        return
    if voice_client.is_playing():
        voice_client.pause()
    elif voice_client.is_paused():
        voice_client.resume()

@bot.command()
async def remove(ctx):
    global voice_client
    if voice_client==None:
        return
    voice_client.stop()

@bot.command()
async def disconnect(ctx):
    global voice_client
    if voice_client==None:
        return
    if voice_client.is_connected():
        await voice_client.disconnect()

bot.run(token["token"])


### helper functions ###
def is_valid_url(url):
    pass