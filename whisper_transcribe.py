import whisper
import sqlite3
import os

model = whisper.load_model("base")

def transcribe_and_store(video_path):
    result = model.transcribe(video_path)
    conn = sqlite3.connect("transcripts.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS segments (
            id INTEGER PRIMARY KEY,
            file TEXT,
            start REAL,
            end REAL,
            text TEXT
        )
    ''')
    for segment in result["segments"]:
        cur.execute("INSERT INTO segments (file, start, end, text) VALUES (?, ?, ?, ?)",
                    (os.path.basename(video_path), segment['start'], segment['end'], segment['text']))
    conn.commit()
    conn.close()
