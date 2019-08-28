import discord
from music.Download import Download
from music.Queue import Queue
import os
from pathlib import Path

class BaseMusicPlayer:
    def __init__():
        self.voice_client = {}
        self.Q = Queue()
        self.now_playing = None
        self.is_queue_looped = False
        self.download = Download()
        # Pathを使ってみたいということで編集中
        # ディレクトリトラバーサルはlist指定型で防ごうと思います
        self.local = Path("./music/local_music_file/")
        self.files = os.listdir("music/local_music_files")

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
        embed = discord.Embed(
            title='Now Playing',
            description=self.now_playing["title"],
            color=0x00bfff)
        if self.now_playing["thumbnail"] is not None:
            embed.set_thumbnail(url=self.now_playing["thumbnail"])

        return ctx.send(embed=embed)

    def status_queue(self, ctx):
        embed = discord.Embed(
            title='Status of Queue',
            description="In queue :",
            color=0x00bfff)
        for index, job in enumerate(self.Q.get_queue()):
            embed.add_field(
                name=str( index + 1) +
                " : " +
                job["title"],
                value=job["author"],
                inline=True)

        return ctx.send(embed=embed)

    def play_audio(url):
        if self.is_local(self.now_playing["url"]):
            self.voice_client[f'{ctx.author.voice.channel}'].play(
                discord.FFmpegPCMAudio(
                    self.now_playing["url"]),
                after=lambda e: self.next(ctx))
        else:
            self.voice_client[f'{ctx.author.voice.channel}'].play(
                discord.FFmpegPCMAudio(
                    self.now_playing["url"],
                    stderr=open(os.devnull, 'w'),
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"),
                after=lambda e: self.next(ctx))

    # def next(self):# need to adjust
    def next(self, ctx):
        if self.is_queue_looped:
            self.Q.add_queue(self.now_playing)

        if self.Q.get_queue() == []:
            print("done Now Queue is empty")
            return

        print('load next audio')

        self.now_playing = self.Q.next_job()
        self.play_audio(self.now_playing["url"])


    def add_channel(self, ctx):
        if not f'{ctx.author.voice.channel}' in self.voice_client:
            self.voice_client[f'{ctx.author.voice.channel}'] = None
