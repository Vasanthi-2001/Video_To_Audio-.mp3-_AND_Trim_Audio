# import yt_dlp
# import moviepy.editor as mp
# import os
# import re

# OUTPUT_FOLDER = "trimmed_audio"
# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# def sanitize_filename(name):
#     # Remove illegal characters for filenames
#     return re.sub(r'[\\/*?:"<>|]', "", name)

# def download_audio(video_link):
#     try:
#         # Extract video title first
#         with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
#             info = ydl.extract_info(video_link, download=False)
#             title = sanitize_filename(info.get("title", "audio"))
        
#         output_template = os.path.join(OUTPUT_FOLDER, f"{title}.%(ext)s")
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "outtmpl": output_template,
#             "postprocessors": [{
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "mp3",
#                 "preferredquality": "192",
#             }],
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_link])
        
#         return os.path.join(OUTPUT_FOLDER, f"{title}.mp3")
#     except Exception as e:
#         print("Download error:", e)
#         return None

# def trim_audio(input_file, duration=10):
#     try:
#         clip = mp.AudioFileClip(input_file)
#         trimmed = clip.subclip(0, duration)

#         base_name = os.path.splitext(os.path.basename(input_file))[0]
#         output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_trimmed_{duration}s.mp3")

#         trimmed.write_audiofile(output_file)
#         clip.close()
#         os.remove(input_file)

#         print("Trimmed audio saved at:", output_file)
#     except Exception as e:
#         print("Trimming error:", e)

# def youtube_to_trimmed_audio(video_link, duration=10):
#     print("Downloading and trimming audio...")
#     audio_path = download_audio(video_link)
#     if audio_path:
#         trim_audio(audio_path, duration)

# # Example usage
# video_link = "https://youtube.com/shorts/ZhynHvFGnUA?si=QJ43hhq9Ldlt53NO"
# youtube_to_trimmed_audio(video_link, duration=10)












import yt_dlp
import moviepy.editor as mp
import os
import re

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
        print("Download error:", e)
        return None

def trim_audio(input_file, duration=10):
    try:
        clip = mp.AudioFileClip(input_file)
        trimmed = clip.subclip(0, duration)

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}_trimmed_{duration}s.mp3")

        trimmed.write_audiofile(output_file)
        clip.close()
        os.remove(input_file)

        print("✅ Trimmed audio saved at:", output_file)
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
        trim_audio(audio_path, duration)

# Example usage
source = r"https://youtube.com/shorts/AKHx_Gp6ui4?si=JEqYiT7fvIbzv-6A"
# source = r"C:/Users/Admin/Desktop/Audio_Noise Reduction_Video_Trim/downloaded_audio/trending.mp3"
process_audio(source, duration=10)
