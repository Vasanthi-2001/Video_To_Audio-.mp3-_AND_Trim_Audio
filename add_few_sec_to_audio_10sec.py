import librosa
import soundfile as sf
import numpy as np
import yt_dlp
import os

# Only one folder
OUTPUT_FOLDER = "extended_audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

INPUT_AUDIO = input("Enter audio file path or YouTube link: ").strip()
EXTEND_SECONDS = int(input("Enter how many seconds to extend: "))

def download_youtube_audio(url):
    filename = os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s")  # Save inside extended_audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
    return downloaded_path

# If input is YouTube link → Download first
if "youtube.com" in INPUT_AUDIO or "youtu.be" in INPUT_AUDIO:
    print("Downloading audio from YouTube...")
    INPUT_AUDIO = download_youtube_audio(INPUT_AUDIO)
    print(f"Downloaded audio saved at: {INPUT_AUDIO}")

# Load audio (supports .wav & .mp3)
audio, sr = librosa.load(INPUT_AUDIO, sr=None)

# Create silence based on user entered seconds
silence = np.zeros(int(EXTEND_SECONDS * sr))

# Append silence
extended_audio = np.concatenate((audio, silence))

# Auto-name output file
base_name = os.path.splitext(os.path.basename(INPUT_AUDIO))[0]
OUTPUT_AUDIO = os.path.join(OUTPUT_FOLDER, f"{base_name}_extended_{EXTEND_SECONDS}s.mp3")

# Save final audio
sf.write(OUTPUT_AUDIO, extended_audio, sr)
print(f"Extended audio saved at: {OUTPUT_AUDIO}")
print(f"Audio extended by {EXTEND_SECONDS} seconds successfully!")
