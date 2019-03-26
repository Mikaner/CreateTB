import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')
with open('./config/config.json','r',encoding='utf-8') as tokenCode:
    token = json.load(tokenCode)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot)
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
async def greet(ctx):
    await ctx.send(":smiley: こんにちは！ :wave:")

@bot.command()
async def join(ctx):
    global voice_client
    voice_channel = bot.get_channel(560100818490228741)#ctx.message.guild.voice_channels[0]
    voice_client = await voice_channel.connect()

@bot.command()
async def play(ctx):
    global voice_client
    if voice_client.is_connected():
        audio_source = discord.FFmpegPCMAudio("./Music/14 TODAY THE FUTURE Magical Mirai ver.wma")
        if not voice_client.is_playing():
            voice_client.play(audio_source)

@bot.command()
async def disconnect(ctx):
    global voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()

bot.run(token["token"])