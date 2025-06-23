from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import sqlite3
import time
from utils import download_video, enforce_video_limit, clip_video

app = Flask(__name__)

DB_PATH = "transcripts.db"
DOWNLOAD_DIR = "downloads"
CLIPS_DIR = "clips"
MAX_VIDEOS = 10

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form["video_url"]
        enforce_video_limit(DOWNLOAD_DIR)
        video_path = download_video(video_url, DOWNLOAD_DIR)
        from whisper_transcribe import transcribe_and_store
        transcribe_and_store(video_path)
        return redirect(url_for("search"))
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    term = request.form.get("term", "") if request.method == "POST" else ""
    if term:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, file, start, end, text FROM segments WHERE text LIKE ?", (f"%{term}%",))
        results = cur.fetchall()
        conn.close()
    return render_template("results.html", results=results, term=term)

import tempfile
from flask import after_this_request

@app.route('/clip/<int:segment_id>')
def clip(segment_id):
    conn = sqlite3.connect("transcripts.db")
    cur = conn.cursor()
    cur.execute("SELECT file, start, end FROM segments WHERE rowid=?", (segment_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return "Segment not found", 404

    video_path, start_time, end_time = row

    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    clip_path = temp_file.name
    temp_file.close()

    # Clip the video into that temp file
    clip_video(video_path, float(start_time), float(end_time), clip_path)

    @after_this_request
    def cleanup(response):
        try:
            os.remove(clip_path)
        except Exception as e:
            print("Error removing temp file:", e)
        return response

    # Send the file as download
    return send_file(
        clip_path,
        as_attachment=True,
        download_name=f"clip_{segment_id}.mp4",
        mimetype="video/mp4"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7999)
