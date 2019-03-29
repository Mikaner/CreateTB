import youtube_dl
import urllib.parse as urlparse
import os

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
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(niconico_url)
            
        return file_path
      

if __name__ == '__main__':
    download = Download()
    #download.youtube_dl(['https://www.youtube.com/watch?v=tSTqQyU9DsM&t=2s'], 'mp3')
    #download.niconico_dl(['https://www.nicovideo.jp/watch/sm33141569'], 'mp3')