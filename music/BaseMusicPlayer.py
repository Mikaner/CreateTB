import discord
from music.Download import Download
from music.Queue import Queue
import os
from pathlib import Path
from celery_tasks.celery import app
from music.utils.tools import (
    get_heart_beating_data_for_niconico,
    create_niconico_session
)
from celery_tasks.tasks import send_heart_beating

class BaseMusicPlayer:
    def __init__(self):
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
        elif url.startswith("https://open.spotify.com/track/"):
            return (True, "spotify")
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

    def play_audio(self, ctx, music_info, nico_task=None):
        url = music_info["url"]
        if self.is_local(music_info["url"]):
            self.voice_client[f'{ctx.author.voice.channel}'].play(
                discord.FFmpegPCMAudio(
                    music_info["url"],
                ),
                after=lambda e: self.next(ctx))
        else:
            if music_info["service"] == "niconico":
                if nico_task is not None:
                    print(nico_task)
                    nico_task.abort()
                    print("finished removing task")
                session_initialization_data = get_heart_beating_data_for_niconico(music_info["url"])
                request_data = create_niconico_session(session_initialization_data)
                nico_task = send_heart_beating.delay(
                    request_data["data"]["session"]["id"],
                    request_data
                )
                music_info["url"] = request_data["data"]["session"]["content_uri"]

            self.voice_client[f'{ctx.author.voice.channel}'].play(
                discord.FFmpegPCMAudio(
                    music_info["url"],
                    stderr=open(os.devnull, 'w'),
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                ),
                after=lambda e: self.next(ctx, nico_task))
        music["url"] = url


    def next(self, ctx, nico_task=None):
        if self.is_queue_looped:
            self.Q.add_queue(self.now_playing)

        if self.Q.get_queue() == []:
            print("done Now Queue is empty")
            return

        print('load next audio')
        print(nico_task)

        self.now_playing = self.Q.next_job()
        self.play_audio(ctx, self.now_playing, nico_task)


    def add_channel(self, ctx):
        if not f'{ctx.author.voice.channel}' in self.voice_client:
            self.voice_client[f'{ctx.author.voice.channel}'] = None
