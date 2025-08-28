
#!/data/data/com.termux/files/usr/bin/bash

# Warna ANSI
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
PURPLE="\033[0;35m"
CYAN="\033[0;36m"
RESET="\033[0m"

while true; do
    clear
    # Judul warna-warni
    echo -e "${RED}=== ${GREEN}MULTI ${YELLOW}PLATFORM ${BLUE}DOWNLOADER ${PURPLE}TERMUX ===${RESET}"

    # Menu opsi warna kuning
    echo -e "${YELLOW}1. Download YouTube Video (best)${RESET}"
    echo -e "${YELLOW}2. Download YouTube Audio (MP3)${RESET}"
    echo -e "${YELLOW}3. Download YouTube Video Resolusi tertentu${RESET}"
    echo -e "${YELLOW}4. Download YouTube Playlist${RESET}"
    echo -e "${YELLOW}5. Download TikTok Video${RESET}"
    echo -e "${YELLOW}6. Update yt-dlp${RESET}"
    echo -e "${YELLOW}X. Keluar${RESET}"

    read -p "➡️ Pilih menu: " menu

    case $menu in
        1)
            read -p "Masukkan URL YouTube: " url
            yt-dlp -o "/sdcard/Download/%(title)s.%(ext)s" -f best "$url"
            read -p "[✔] Selesai... tekan Enter"
            ;;
        2)
            read -p "Masukkan URL YouTube: " url
            yt-dlp -o "/sdcard/Download/%(title)s.%(ext)s" -f bestaudio --extract-audio --audio-format mp3 "$url"
            read -p "[✔] Selesai... tekan Enter"
            ;;
        3)
            read -p "Masukkan URL YouTube: " url
            echo -e "${YELLOW}Pilih resolusi video:${RESET}"
            echo -e "${YELLOW}1. 1080p${RESET}"
            echo -e "${YELLOW}2. 720p${RESET}"
            echo -e "${YELLOW}3. 480p${RESET}"
            echo -e "${YELLOW}4. 360p${RESET}"
            echo -e "${YELLOW}5. 240p${RESET}"
            read -p "➡️ Pilih: " res
            case $res in
                1) fmt="bestvideo[height<=1080]+bestaudio/best[height<=1080]" ;;
                2) fmt="bestvideo[height<=720]+bestaudio/best[height<=720]" ;;
                3) fmt="bestvideo[height<=480]+bestaudio/best[height<=480]" ;;
                4) fmt="bestvideo[height<=360]+bestaudio/best[height<=360]" ;;
                5) fmt="bestvideo[height<=240]+bestaudio/best[height<=240]" ;;
                *) echo -e "${RED}[!] Pilihan tidak valid!${RESET}"; sleep 1; continue ;;
            esac
            yt-dlp -o "/sdcard/Download/%(title)s.%(ext)s" -f "$fmt" "$url"
            read -p "[✔] Selesai... tekan Enter"
            ;;
        4)
            read -p "Masukkan URL Playlist: " url
            yt-dlp -o "/sdcard/Download/%(playlist_title)s/%(title)s.%(ext)s" "$url"
            read -p "[✔] Playlist selesai di-download... tekan Enter"
            ;;
        5)
            read -p "Masukkan URL TikTok: " url
            yt-dlp -o "/sdcard/Download/%(title)s.%(ext)s" "$url"
            read -p "[✔] TikTok selesai di-download... tekan Enter"
            ;;
        6)
            echo -e "${CYAN}[🔄] Updating yt-dlp...${RESET}"
            pip install -U yt-dlp
            echo -e "${GREEN}[✔] Update selesai!${RESET}"
            read -p "Tekan Enter untuk kembali ke menu"
            ;;
        x|X)
            echo -e "${GREEN}[✔] Keluar...${RESET}"
            exit 0
            ;;
        *)
            echo -e "${RED}[!] Pilihan tidak valid!${RESET}"
            sleep 1
            ;;
    esac
done


