

#!/data/data/com.termux/files/usr/bin/bash

# === YT-DLP TERMUX MANAGER ===
while true; do
    clear
    echo "=== YT-DLP MANAGER ==="
    echo "1. Download Video (kualitas terbaik)"
    echo "2. Download Audio (MP3)"
    echo "3. Download Video resolusi tertentu"
    echo "4. Download Playlist"
    echo "5. Update yt-dlp"
    echo "X. Keluar"
    echo "======================="
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
            echo "Pilih resolusi video:"
            echo "1. 1080p"
            echo "2. 720p"
            echo "3. 480p"
            echo "4. 360p"
            echo "5. 240p"
            read -p "➡️ Pilih: " res
            case $res in
                1) fmt="bestvideo[height<=1080]+bestaudio/best[height<=1080]" ;;
                2) fmt="bestvideo[height<=720]+bestaudio/best[height<=720]" ;;
                3) fmt="bestvideo[height<=480]+bestaudio/best[height<=480]" ;;
                4) fmt="bestvideo[height<=360]+bestaudio/best[height<=360]" ;;
                5) fmt="bestvideo[height<=240]+bestaudio/best[height<=240]" ;;
                *) echo "[!] Pilihan tidak valid!"; sleep 1; continue ;;
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
            echo "[🔄] Updating yt-dlp..."
            pip install -U yt-dlp
            echo "[✔] Update selesai!"
            read -p "Tekan Enter untuk kembali ke menu"
            ;;
        x|X)
            echo "[✔] Keluar..."
            exit 0
            ;;
        *)
            echo "[!] Pilihan tidak valid!"
            sleep 1
            ;;
    esac
done



