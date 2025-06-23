import whisper
import yt_dlp
import os

# Config
url = "https://youtu.be/WT0jqAQ9Omk"  # Change this to a real speech
output_file = "Donald Trump's full speech at 2024 Republican National Convention.mp4"

# Download video
ydl_opts = {
    'outtmpl': output_file,
    'format': 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[height<=720]',
    'merge_output_format': 'mp4'
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# Load Whisper
model = whisper.load_model("base")  # Try "medium" or "large" if you want more accuracy

# Transcribe
result = model.transcribe(output_file)

# Save output with timestamps
with open("Donald Trump's full speech at 2024 Republican National Convention.txt", "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        f.write(f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}\n")

print("Done! Transcription saved to Donald Trump's full speech at 2024 Republican National Convention.txt")
