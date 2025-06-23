from utils import enforce_video_limit, download_video
from whisper_transcribe import transcribe_and_store

def main():
    url = input("Paste a video URL: ").strip()
    enforce_video_limit("downloads")
    video = download_video(url, "downloads")
    print("Downloaded. Transcribing...")
    transcribe_and_store(video)
    print("Done.")

if __name__ == "__main__":
    main()
