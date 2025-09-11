
#!/data/data/com.termux/files/usr/bin/bash

# ===== IDM-Style Termux Downloader =====
OUTPUT_DIR="/sdcard/Download"

# Warna
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${CYAN}=== IDM-Style Termux Downloader ===${RESET}"
read -p "Masukkan URL video/embed: " URL

# Buat folder download
mkdir -p "$OUTPUT_DIR"

# Cek direct MP4
if echo "$URL" | grep -qiE "\.mp4|\.mkv|\.webm"; then
    echo -e "${GREEN}🔗 Direct link detected...${RESET}"
    FILENAME=$(basename "$URL" | sed 's/[?].*//')
    OUTPUT_FILE="$OUTPUT_DIR/$FILENAME"
    echo -e "${YELLOW}Downloading $FILENAME ...${RESET}"
    curl -C - -L "$URL" -o "$OUTPUT_FILE" || wget -c "$URL" -O "$OUTPUT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Download selesai: $OUTPUT_FILE${RESET}"
    else
        echo -e "${RED}❌ Download gagal!${RESET}"
    fi
    exit 0
fi

# Cek HLS / m3u8
if echo "$URL" | grep -qiE "\.m3u8"; then
    echo -e "${GREEN}🔗 HLS/m3u8 link detected...${RESET}"
    OUTPUT_FILE="$OUTPUT_DIR/video_$(date +%s).mp4"
    ffmpeg -i "$URL" -c copy "$OUTPUT_FILE"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Download selesai: $OUTPUT_FILE${RESET}"
    else
        echo -e "${RED}❌ Download gagal!${RESET}"
    fi
    exit 0
fi

# Fallback yt-dlp
if command -v yt-dlp >/dev/null 2>&1; then
    echo -e "${GREEN}🔗 Using yt-dlp fallback...${RESET}"
    OUTPUT_FILE="$OUTPUT_DIR/%(title)s.%(ext)s"
    yt-dlp -f best -o "$OUTPUT_FILE" "$URL"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Download selesai di folder $OUTPUT_DIR${RESET}"
    else
        echo -e "${RED}❌ yt-dlp gagal download!${RESET}"
    fi
else
    echo -e "${RED}❌ yt-dlp tidak terpasang, install dulu: pkg install yt-dlp${RESET}"
fi
