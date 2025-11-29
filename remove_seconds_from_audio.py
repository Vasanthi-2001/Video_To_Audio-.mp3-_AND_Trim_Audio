#Removing seconds from an audio 
#which is customizable like from first,last and middle


import librosa
import soundfile as sf
import numpy as np
import yt_dlp
import os

OUTPUT_FOLDER = "Removed_sec_from_audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

INPUT_AUDIO = input("Enter audio file path or YouTube link: ").strip().strip('"')
REMOVE_SEC = float(input("Enter seconds to remove: "))

print("\nChoose trim option:")
print("1 → Remove from start")
print("2 → Remove from end")
print("3 → Remove from middle")
choice = int(input("Enter choice (1/2/3): "))


def download_youtube_audio(url):
    filename = os.path.join(OUTPUT_FOLDER, "%(title)s.%(ext)s")
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


# If YouTube link → Download
if "youtube.com" in INPUT_AUDIO or "youtu.be" in INPUT_AUDIO:
    print("\nDownloading from YouTube...")
    INPUT_AUDIO = download_youtube_audio(INPUT_AUDIO)
    print(f"Downloaded audio saved at: {INPUT_AUDIO}\n")


# Load audio
audio, sr = librosa.load(INPUT_AUDIO, sr=None)
total_sec = len(audio) / sr
remove_samples = int(REMOVE_SEC * sr)

if REMOVE_SEC >= total_sec:
    print("❌ Error: Remove seconds is greater than audio length!")
    exit()

# Trimming Logic
if choice == 1:
    print("Removing from start...")
    trimmed_audio = audio[remove_samples:]

elif choice == 2:
    print("Removing from end...")
    trimmed_audio = audio[:-remove_samples]

elif choice == 3:
    print("Removing from middle...")
    mid = len(audio) // 2
    trimmed_audio = np.concatenate((audio[:mid - remove_samples//2], audio[mid + remove_samples//2:]))

else:
    print("Invalid choice!")
    exit()


# Save output
base_name = os.path.splitext(os.path.basename(INPUT_AUDIO))[0]
OUTPUT_AUDIO = os.path.join(OUTPUT_FOLDER, f"{base_name}_trimmed_{REMOVE_SEC}s.mp3")

sf.write(OUTPUT_AUDIO, trimmed_audio, sr)

print(f"\n✔ Trimmed audio saved at: {OUTPUT_AUDIO}")
print(f"✔ Removed {REMOVE_SEC} seconds successfully!")
