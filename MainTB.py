import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from Config import Config
from music.MusicCog import MusicCog
import traceback

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

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("No such command")
            return
        raise error



if __name__ == "__main__":
    config = Config()
    TB = MainTB(command_prefix=config.get_prefix())
    TB.run(config.get_token())
