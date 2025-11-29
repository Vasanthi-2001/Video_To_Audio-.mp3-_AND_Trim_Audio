import yt_dlp
import moviepy.editor as mp
import os
import re

OUTPUT_FOLDER = "Trim_specific_range_from_audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------------------
# CLEAN FILENAME
# -----------------------------------------
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

# -----------------------------------------
# TIME CONVERSION MM:SS → total_seconds
# -----------------------------------------
def convert_to_seconds(time_str):
    """
    Converts 'MM:SS' or 'HH:MM:SS' into total seconds.
    """
    parts = list(map(int, time_str.split(":")))
    
    if len(parts) == 2:  # MM:SS
        minutes, seconds = parts
        return minutes * 60 + seconds

    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds

    else:
        raise ValueError("Invalid time format! Use MM:SS or HH:MM:SS")

# -----------------------------------------
# DOWNLOAD AUDIO FROM YOUTUBE
# -----------------------------------------
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

# -----------------------------------------
# TRIM ANY SPECIFIC TIME RANGE
# -----------------------------------------
def trim_audio(input_file, start_time, end_time):
    try:
        clip = mp.AudioFileClip(input_file)

        trimmed = clip.subclip(start_time, end_time)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(
            OUTPUT_FOLDER,
            f"{base_name}_clip_{start_time}s_to_{end_time}s.mp3"
        )

        trimmed.write_audiofile(output_file)
        clip.close()

        print("✅ Trimmed audio saved at:", output_file)

    except Exception as e:
        print("❌ Trimming error:", e)

# -----------------------------------------
# MAIN PROCESSOR — YOUTUBE OR LOCAL MP3
# -----------------------------------------
def process_audio(source, start_str, end_str):
    print("🔄 Processing:", source)

    # Convert MM:SS → seconds
    start_time = convert_to_seconds(start_str)
    end_time = convert_to_seconds(end_str)

    # Source
    if source.startswith("http://") or source.startswith("https://"):
        audio_path = download_audio(source)
    elif os.path.isfile(source) and source.lower().endswith(".mp3"):
        audio_path = source
    else:
        print("❌ Invalid input: must be a YouTube URL or .mp3 file path")
        return

    if audio_path:
        trim_audio(audio_path, start_time, end_time)

# -----------------------------------------
# EXAMPLE USAGE
# -----------------------------------------

source = "https://youtu.be/nlMpxUYKTcU?si=skBTTce9_96RVWMC"

start_time_str = "3:30"      # MM:SS → auto converts to 0 seconds
end_time_str   = "3:43"      # MM:SS → auto converts to 10 seconds

process_audio(source, start_time_str, end_time_str)
