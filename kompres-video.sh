cat <<'EOF' > kompres-video.sh
#!/bin/bash

# Warna
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

TARGET_BITRATE="250k"
AUDIO_BITRATE="64k"

echo -e "${CYAN}==============================="
echo -e "${MAGENTA} HLS Multi-Folder Merge & Compress (~300MB)"
echo -e "${CYAN}===============================${RESET}"

# Scan semua folder .m3u8
echo -e "${YELLOW}🔹 Mencari folder .m3u8 di /sdcard...${RESET}"
mapfile -t FOLDERS < <(find /sdcard -maxdepth 1 -type d -name "*.m3u8" | sort)

if [ ${#FOLDERS[@]} -eq 0 ]; then
    echo -e "${RED}❌ Tidak ditemukan folder .m3u8 di /sdcard${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ Ditemukan ${#FOLDERS[@]} folder. Mulai proses...${RESET}"

# Loop tiap folder
for FOLDER in "${FOLDERS[@]}"; do
    echo -e "${CYAN}-------------------------------${RESET}"
    echo -e "${MAGENTA}📂 Proses folder: $FOLDER${RESET}"
    
    cd "$FOLDER" || { echo -e "${RED}❌ Gagal masuk folder${RESET}"; continue; }

    SEGMENT_FILES=($(ls | sort -n))
    if [ ${#SEGMENT_FILES[@]} -eq 0 ]; then
        echo -e "${RED}❌ Tidak ada file segmen di folder${RESET}"
        continue
    fi

    # Buat daftar file
    rm -f files.txt
    for f in "${SEGMENT_FILES[@]}"; do
        echo "file '$f'" >> files.txt
    done

    # Estimasi progress gabung
    TOTAL=${#SEGMENT_FILES[@]}
    echo -e "${YELLOW}🔹 Menggabungkan segmen menjadi output.mp4...${RESET}"
    ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4 -progress pipe:1 | while read line; do
        if [[ "$line" =~ out_time_ms=([0-9]+) ]]; then
            echo -ne "${BLUE}Gabung segmen...${RESET}\r"
        fi
    done

    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Gabung segmen gagal!${RESET}"
        continue
    fi

    # Kompres dengan progress
    echo -e "${YELLOW}🔹 Mengompres output.mp4 ke target ~300MB...${RESET}"
    ffmpeg -i output.mp4 -b:v $TARGET_BITRATE -c:a aac -b:a $AUDIO_BITRATE output_small_300mb.mp4 -progress pipe:1 | while read line; do
        if [[ "$line" =~ out_time_ms=([0-9]+) ]]; then
            echo -ne "${MAGENTA}Mengompres...${RESET}\r"
        fi
    done

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Selesai! File MP4 siap diputar: ${FOLDER}/output_small_300mb.mp4${RESET}"
    else
        echo -e "${RED}❌ Kompres gagal!${RESET}"
    fi
done

echo -e "${CYAN}===============================${RESET}"
echo -e "${GREEN}Semua folder selesai diproses.${RESET}"
EOF