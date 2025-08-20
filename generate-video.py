
import os
import json

BASE_FOLDER = "/sdcard/.isi folder..kamu"
VIDEOS_FOLDER = os.path.join(BASE_FOLDER, "videos")
OUTPUT_FILE = os.path.join(BASE_FOLDER, "videos.js")

def scan_videos():
    all_videos = {}

    categories = [f for f in os.listdir(VIDEOS_FOLDER)
                  if os.path.isdir(os.path.join(VIDEOS_FOLDER, f))]

    for cat in categories:
        cat_path = os.path.join(VIDEOS_FOLDER, cat)
        files = [f for f in os.listdir(cat_path) if f.lower().endswith(".mp4")]
        if files:
            all_videos[cat] = [f"videos/{cat}/{f}" for f in files]

    # tulis ke videos.js
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("const allVideos = {\n")
        for cat, vids in all_videos.items():
            f.write(f'  "{cat}": [\n')
            for v in vids:
                f.write(f'    "{v}",\n')
            f.write("  ],\n")
        f.write("};\n")

    print(f"[OK] {OUTPUT_FILE} updated!")

if __name__ == "__main__":
    scan_videos()
