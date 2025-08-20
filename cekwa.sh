
#!/bin/bash

# Warna-warna
hijau="\033[1;32m"
merah="\033[1;31m"
kuning="\033[1;33m"
biru="\033[1;34m"
cyan="\033[1;36m"
reset="\033[0m"

while true; do
    clear
    echo -e "${kuning}=========================================${reset}"
    echo -e "${biru}        🚀 WhatsApp Tools via Termux     ${reset}"
    echo -e "${kuning}=========================================${reset}"
    echo -e "${hijau}(A) Kirim Pesan${reset}"
    echo -e "${cyan}(B) Cek Nomor WA${reset}"
    echo -e "${merah}(C) Exit${reset}"
    echo -ne "${kuning}Pilih opsi (A/B/C): ${reset}"
    read opsi

    if [[ "$opsi" == "A" || "$opsi" == "a" ]]; then
        echo -ne "${hijau}Masukkan nomor tujuan (format 628xxx): ${reset}"
        read nomor
        echo -ne "${cyan}Masukkan pesan: ${reset}"
        read pesan
        pesan=$(echo $pesan | sed 's/ /%20/g')
        echo -e "${biru}Membuka WhatsApp...${reset}"
        am start -a android.intent.action.VIEW -d "https://wa.me/$nomor?text=$pesan"
        echo -e "${hijau}✅ Selesai! Pesan siap dikirim ke $nomor${reset}"
        read -p "Tekan [Enter] untuk kembali ke menu..."

    elif [[ "$opsi" == "B" || "$opsi" == "b" ]]; then
        echo -ne "${hijau}Masukkan nomor yang mau dicek (628xxx): ${reset}"
        read nomor
        echo -e "${kuning}Mengecek nomor...${reset}"
        am start -a android.intent.action.VIEW -d "https://wa.me/$nomor"
        echo -e "${cyan}⚡ Kalau nomor ${hijau}$nomor${reset}${cyan} aktif di WA → WhatsApp akan terbuka.${reset}"
        echo -e "${merah}❌ Kalau tidak terdaftar → akan muncul notifikasi error.${reset}"
        read -p "Tekan [Enter] untuk kembali ke menu..."

    elif [[ "$opsi" == "C" || "$opsi" == "c" ]]; then
        echo -e "${merah}🚪 Keluar dari WhatsApp Tools...${reset}"
        exit 0

    else
        echo -e "${merah}⚠️ Opsi tidak valid, pilih A, B, atau C!${reset}"
        sleep 2
    fi
done


