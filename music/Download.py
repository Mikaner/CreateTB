import youtube_dl

class Download:
    def youtube_dl(self, youtube_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'music/downloaded_music_files/%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(youtube_url)

    def niconico_dl(self):
        pass

if __name__ == '__main__':
    download = Download()
    download.youtube_dl(['https://www.youtube.com/watch?v=tSTqQyU9DsM&t=2s'])