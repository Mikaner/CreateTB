import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from Config import Config
from music.MusicCog import MusicCog
import traceback
import re
import random

INITIAL_COGS = [
    MusicCog
]


class MainTB(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

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
        print('message'.center(15, '-'))

    async def on_message(self, message):
        if message.content.startswith(config.get_prefix()):
            await self.process_commands(message)
        if self.user == message.author:
            return
        if message.content.startswith("にゃーん"):
            await message.channel.send("にゃーん")


        dice = re.compile(u'/d (.+)d(.+)').match(message.content)
        if dice:# dice計算用
            try:
                reply = dice.group()+':\n' # dice.group():受け取ったmessageのうち、判定に使った情報
                diceSum = 0 # 合計計算用の受け取り変数を用意
                if int(dice.group(1)) <= 992:
                    for i in range(int(dice.group(1))):# 2d6だった場合、2回for文を回す
                        r = random.randrange(0,int(dice.group(2)))+1 # 2d6だった場合、0~5をランダムで選択し、+1する
                        diceSum += r
                        reply += ' '+str(r)
                    reply += '\n⇒ '+str(diceSum)
                else:
                    reply = 'ちょ、多すぎ！もっとちっちゃくして！'
            except ValueError: # 大体変なことするとfor文の中のint()の部分で型のエラーが出るからそれをcatch
                reply = '数値じゃないと...わかんないのです....'
            finally: # どっちにしろこの文は起動するからfinally使ってます。正直いらないと思う。見やすいからいるかな？
                await message.channel.send(reply)

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("No such command")
            return
        raise error



if __name__ == "__main__":
    config = Config()
    TB = MainTB(command_prefix=config.get_prefix())
    TB.run(config.get_token())
