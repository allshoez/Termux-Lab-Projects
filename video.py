
import os
import json
import webbrowser
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=".")

PORT = 3000

# lokasi folder & file output di sdcard
VIDEOS_FOLDER = os.path.join("/sdcard", "Movies", "videos")
OUTPUT_FILE = os.path.join("/sdcard", "Movies", "videos.js")

def scan_videos():
    all_videos = {}

    if not os.path.exists(VIDEOS_FOLDER):
        print("⚠️ Folder tidak ditemukan:", VIDEOS_FOLDER)
        return

    categories = [f for f in os.listdir(VIDEOS_FOLDER) if os.path.isdir(os.path.join(VIDEOS_FOLDER, f))]
    for cat in categories:
        cat_path = os.path.join(VIDEOS_FOLDER, cat)
        files = [f for f in os.listdir(cat_path) if f.lower().endswith(".mp4")]
        all_videos[cat] = [
            {
                "src": f"videos/{cat}/{f}",
                "title": ".".join(f.split(".")[:-1])
            }
            for f in files
        ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("const allVideos = ")
        json.dump(all_videos, f, indent=2, ensure_ascii=False)
        f.write(";")

    print(f"{OUTPUT_FILE} updated!")

# scan folder sdcard/TakTik/videos
scan_videos()

# serve file statis, termasuk index.html dari sdcard/TakTik
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory("/sdcard/TakTik", filename)

@app.route("/")
def index():
    return send_from_directory("/sdcard/TakTik", "index.html")

if __name__ == "__main__":
    url = f"http://127.0.0.1:{PORT}"
    print(f"Server running at {url}")
    try:
        webbrowser.get("chrome").open(url)
    except:
        webbrowser.open(url)
    app.run(host="0.0.0.0", port=PORT, debug=True)

