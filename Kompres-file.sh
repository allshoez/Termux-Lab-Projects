#!/bin/bash

# ===== Warna =====
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

while true; do
    clear
    echo -e "${CYAN}==============================${NC}"
    echo -e "${GREEN}      KOMPRES FOLDER ZIP      ${NC}"
    echo -e "${CYAN}==============================${NC}"
    echo -e "${YELLOW}1.${NC} Kompres folder pilihan"
    echo -e "${YELLOW}X.${NC} Exit"
    echo -ne "${PURPLE}Pilih opsi: ${NC}"
    read option

    case $option in
        1)
            echo -ne "${BLUE}Masukkan path folder yang ingin dikompres: ${NC}"
            read srcfolder
            if [ ! -d "$srcfolder" ]; then
                echo -e "${RED}Folder tidak ditemukan!${NC}"
                read -n1 -r -p "Tekan sembarang tombol untuk kembali ke menu..."
                continue
            fi

            foldername=$(basename "$srcfolder")
            echo -ne "${BLUE}Masukkan password ZIP (akan terlihat): ${NC}"
            read password

            # Hasil otomatis di /sdcard/foldername.zip
            zip -r -P "$password" "/sdcard/$foldername.zip" "$srcfolder" &> /dev/null

            echo -e "${GREEN}Berhasil dikompres: /sdcard/$foldername.zip${NC}"
            read -n1 -r -p "Tekan sembarang tombol untuk kembali ke menu..."
            ;;
        [Xx])
            echo -e "${RED}Keluar...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Opsi tidak valid!${NC}"
            read -n1 -r -p "Tekan sembarang tombol untuk kembali ke menu..."
            ;;
    esac
done