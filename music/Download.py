import youtube_dl
import requests
import time
from bs4 import BeautifulSoup
import json
from youtube_dl.utils import DownloadError
import urllib.parse as urlparse
import os
import pafy
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import concurrent.futures
from Config import Config
from apiclient.discovery import build


class Download:
    def __init__(self):
        self.executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
        self.config = Config()

    def youtube_dl(self, youtube_url, ext):
        url = youtube_url[0]
        parsed = urlparse.urlparse(url)
        file_path = 'music/downloaded_music_files/youtube/' + \
            urlparse.parse_qs(parsed.query)['v'][0] + '.' + ext

        if not os.path.isfile(file_path):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': ext,
                    'preferredquality': '192',
                }],
                'outtmpl': file_path,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(youtube_url)

        return file_path


    def youtube_stream(self, youtube_url, ext):
        url = youtube_url[0]
        video = pafy.new(url)
        title = video.title
        thumbnail = video.thumb
        author = video.author
        best = video.getbestaudio()
        playurl = best.url

        print(title)
        return {
            "service": "youtube",
            "url": playurl,
            "title": title,
            "thumbnail": thumbnail,
            "author": author}
    
    def niconico_stream(self, niconico_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '192',
            }],
            'restrictfilenames': True,
            'noplaylist': True,
            'cookiefile': 'nico-cookie.txt',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'usenetrc': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(niconico_url, download=False)
            print(info_dict)

        return {
            "service": "niconico",
            "url": niconico_url,
            "title": info_dict.get('title', None),
            "thumbnail": info_dict.get('thumbnails', None)[0]["url"],
            "author": info_dict.get('uploader', None)}


    def spotify_stream(self, url):
        """
        client_credentials_manager = SpotifyClientCredentials(client_id=self.config.get_spotify_client_id(), client_secret=self.config.get_spotify_client_secret())
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        track_id = url.split("/")[4]
        results = spotify.track(track_id)

        title = results["name"]
        thumbnail = results["album"]["images"][0]["url"]
        author = results["album"]["artists"][0]["name"]
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '192',
            }],
            'restrictfilenames': True,
            'noplaylist': True,
            'cookiefile': 'nico-cookie.txt',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'usenetrc': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            print(info_dict)

        """
        return {
            "service": "spotify",
            "url": url,
            "title": title,
            "thumbnail": thumbnail,
            "author": author
        }
        """


    def spotify_search(self, words):
        client_credentials_manager = SpotifyClientCredentials(client_id=self.config.get_spotify_client_id(), client_secret=self.config.get_spotify_client_id())
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        results = spotify.search(q="track:" + name, type="track")
        track_id = results["tracks"]["items"][0]["url"].split(":")[2]

        return "https://open.spotify.com/track/" + track_id


    def youtube_search(self, words):
        youtube_api_service_name = 'youtube'
        youtube_api_version = 'v3'

        developer_key = self.config.get_api_key()
        youtube = build(
            youtube_api_service_name,
            youtube_api_version,
            developerKey=developer_key)

        search_response = youtube.search().list(
            q=words,
            part="id,snippet"
        ).execute()

        videos = []

        for search_result in search_response.get("items", []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append(search_result['id']['videoId'])

        url = 'https://www.youtube.com/watch?v=' + videos[0]

        return url


if __name__ == '__main__':
    download = Download()
    try:
        #download.youtube_dl(['https://www.youtube.com/watch?v=tSTqQyU9DsM&t=2s'], 'mp3')
        download.niconico_dl(
            ['https://www.nicovideo.jp/watch/sm15967835'], 'mp3')
    except DownloadError:
        download.niconico_dl(
            ['https://www.nicovideo.jp/watch/sm15967835'], 'mp3')
