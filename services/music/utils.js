const detect_service = (url) => {
    if (url.startsWith("https://www.youtube.com/watch?v=")) {
      return "youtube";
    } else if (url.startsWith("https://www.nicovideo.jp/watch/sm")) {
      return "niconico";
    } else {
      return null;
    }
}