import os
import yt_dlp

def enforce_video_limit(directory, max_videos=10):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return
    files = sorted(
        [os.path.join(directory, f) for f in os.listdir(directory)],
        key=os.path.getctime
    )
    while len(files) > max_videos:
        os.remove(files[0])
        files.pop(0)

def clip_video(file, start, end, output_path):
    buffer = 1
    clipped_start = max(0, start - buffer)
    clipped_end = end + buffer
    command = f'ffmpeg -i "{file}" -ss {clipped_start} -to {clipped_end} -c copy "{output_path}" -y'
    os.system(command)

def download_video(url, directory):
    ydl_opts = {
        'format': 'best[height<=480]',
        'outtmpl': os.path.join(directory, '%(id)s.%(ext)s'),
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(directory, f"{info['id']}.{info['ext']}")
