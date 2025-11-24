#AUDIO FILE TRIMMER – ONLY LAST 10 SECONDS
#SUPPORTS BOTH YOUTUBE URLS & .MP3 FILES

import yt_dlp
import moviepy.editor as mp
import os
import re

from source import source

OUTPUT_FOLDER = "trimmed_audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_audio(video_link):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_link, download=False)
            title = sanitize_filename(info.get("title", "audio"))
        
        output_template = os.path.join(OUTPUT_FOLDER, f"{title}.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
        
        return os.path.join(OUTPUT_FOLDER, f"{title}.mp3")
    except Exception as e:
        print("❌ Download error:", e)
        return None

def trim_last_seconds(input_file, duration=10):
    """Trim only the LAST N seconds of audio"""
    try:
        clip = mp.AudioFileClip(input_file)
        audio_duration = clip.duration

        start_time = max(0, audio_duration - duration)
        trimmed = clip.subclip(start_time, audio_duration)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_last_{duration}s.mp3")

        trimmed.write_audiofile(output_file)
        clip.close()

        os.remove(input_file)   # Optional: delete original downloaded file

        print(f"✅ Trimmed (last {duration} seconds) saved at:", output_file)
    except Exception as e:
        print("❌ Trimming error:", e)

def process_audio(source, duration=10):
    print("🔄 Processing:", source)
    if source.startswith("http://") or source.startswith("https://"):
        audio_path = download_audio(source)
    elif os.path.isfile(source) and source.lower().endswith(".mp3"):
        audio_path = source
    else:
        print("❌ Invalid input: must be a YouTube link or .mp3 file path")
        return

    if audio_path:
        trim_last_seconds(audio_path, duration)

# Example usage:
source = r"C:\Users\Admin\Desktop\YT_Video_to_Audio_AND_audio_Trim\downloaded_audio\Infinity Reference Audio3.mp3"
process_audio(source, duration=10)
