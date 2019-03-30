import youtube_dl
from youtube_dl.utils import DownloadError
import urllib.parse as urlparse
import os
import pafy


class Download:
    def youtube_dl(self, youtube_url, ext):
        url = youtube_url[0]
        parsed = urlparse.urlparse(url)
        file_path = 'music/downloaded_music_files/youtube/' + urlparse.parse_qs(parsed.query)['v'][0] + '.' + ext

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

    def niconico_dl(self, niconico_url, ext):
        url = niconico_url[0]
        parsed = urlparse.urlparse(url)
        file_path = 'music/downloaded_music_files/niconico/' + os.path.basename(parsed.path) + '.' + ext

        if not os.path.isfile(file_path):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': ext,
                    'preferredquality': '192',
                }],
                'outtmpl': file_path,
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0',
                'usenetrc': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(niconico_url)
            
        return file_path

    def youtube_stream(self, youtube_url, ext):
        url = youtube_url[0]
        video = pafy.new(url)
        best = video.getbestaudio()
        playurl = best.url

        return playurl
      

if __name__ == '__main__':
    download = Download()
    try:
        #download.youtube_dl(['https://www.youtube.com/watch?v=tSTqQyU9DsM&t=2s'], 'mp3')
        download.niconico_dl(['https://www.nicovideo.jp/watch/sm15967835'], 'mp3')
    except DownloadError:
        download.niconico_dl(['https://www.nicovideo.jp/watch/sm15967835'], 'mp3')
