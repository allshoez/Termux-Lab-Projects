#!/bin/bash

# Warna
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

TARGET_BITRATE="250k"
AUDIO_BITRATE="64k"

echo -e "${CYAN}==============================="
echo -e "${GREEN} HLS / MP4 Compress + Auto Subtitle (Manual Folder)${RESET}"
echo -e "${CYAN}===============================${RESET}"

# Input folder
read -p "📂 Masukkan nama folder di /sdcard/: " FOLDER_NAME
FOLDER_PATH="/sdcard/$FOLDER_NAME"

if [ ! -d "$FOLDER_PATH" ]; then
    echo -e "${RED}❌ Folder tidak ditemukan: $FOLDER_PATH${RESET}"
    exit 1
fi

cd "$FOLDER_PATH" || { echo -e "${RED}❌ Gagal masuk folder${RESET}"; exit 1; }

# Cek file MP4
MP4_FILE=$(ls *.mp4 2>/dev/null | head -n1)
# Cek file segmen TS / tanpa ekstensi
SEGMENT_FILES=($(ls | grep -E "^[0-9]+$|.*\.ts$" | sort -V))
# Cek file SRT
SRT_FILE=$(ls *.srt 2>/dev/null | head -n1)

# Tentukan input video
if [ -n "$MP4_FILE" ]; then
    echo -e "${YELLOW}🔹 File MP4 ditemukan: $MP4_FILE${RESET}"
    INPUT_VIDEO="$MP4_FILE"
elif [ ${#SEGMENT_FILES[@]} -gt 0 ]; then
    echo -e "${YELLOW}🔹 Segmen ditemukan → gabung menjadi MP4...${RESET}"
    rm -f files.txt
    for f in "${SEGMENT_FILES[@]}"; do
        echo "file '$f'" >> files.txt
    done
    INPUT_VIDEO="output_temp.mp4"
    ffmpeg -f concat -safe 0 -i files.txt -c copy "$INPUT_VIDEO"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Gabung segmen gagal!${RESET}"
        exit 1
    fi
else
    echo -e "${RED}❌ Tidak ada file MP4 atau segmen di folder${RESET}"
    exit 1
fi

# Proses kompres + subtitle
if [ -n "$SRT_FILE" ]; then
    echo -e "${YELLOW}🔹 Subtitle ditemukan: $SRT_FILE → hardcode ke video${RESET}"
    ffmpeg -i "$INPUT_VIDEO" -vf "subtitles=$SRT_FILE:force_style='FontName=Arial,FontSize=24,PrimaryColour=&H00FFFF&'" -b:v $TARGET_BITRATE -c:a aac -b:a $AUDIO_BITRATE output_final.mp4
else
    echo -e "${YELLOW}🔹 Tidak ada subtitle → kompres biasa${RESET}"
    ffmpeg -i "$INPUT_VIDEO" -b:v $TARGET_BITRATE -c:a aac -b:a $AUDIO_BITRATE output_final.mp4
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Selesai! File MP4 siap diputar: ${FOLDER_PATH}/output_final.mp4${RESET}"
else
    echo -e "${RED}❌ Kompres gagal!${RESET}"
fi

# Hapus sementara kalau ada
[ "$INPUT_VIDEO" == "output_temp.mp4" ] && rm -f output_temp.mp4

echo -e "${CYAN}===============================${RESET}"
echo -e "${GREEN}Proses selesai.${RESET}"