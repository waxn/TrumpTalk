import sqlite3
import json

DB_NAME = "transcripts.db"
TRANSCRIPTION_FILE = "Donald Trump's full speech at 2024 Republican National Convention.txt"  # Change if needed
VIDEO_FILE = "Donald Trump's full speech at 2024 Republican National Convention.mp4"                 # The file you transcribed

# Connect to DB
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file TEXT,
    start REAL,
    end REAL,
    text TEXT
);
''')

# Load Whisper JSON output if available
with open("Donald Trump's full speech at 2024 Republican National Convention.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    try:
        time_part, text = line.split("]", 1)
        time_part = time_part.strip("[").strip()
        start_str, end_str = time_part.split(" - ")
        start = float(start_str)
        end = float(end_str)
        cur.execute("INSERT INTO segments (file, start, end, text) VALUES (?, ?, ?, ?)",
                    (VIDEO_FILE, start, end, text.strip()))
    except Exception as e:
        print(f"Skipping line due to error: {e}")

conn.commit()
conn.close()

print("✅ Transcription saved to transcripts.db")
