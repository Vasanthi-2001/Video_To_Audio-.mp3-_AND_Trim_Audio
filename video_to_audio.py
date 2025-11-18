import yt_dlp
import os

OUTPUT_FOLDER = "downloaded_audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def youtube_to_audio(video_link):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
        print("Audio saved in:", OUTPUT_FOLDER)
    except Exception as e:
        print("Error:", e)

# Example
video_link = "https://youtube.com/shorts/YhUVgmdXoUA?si=kuc1M7rPpOmY8Pnt"
youtube_to_audio(video_link)
