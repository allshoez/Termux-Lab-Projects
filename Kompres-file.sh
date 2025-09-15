#!/bin/bash

# ===== WARNA =====
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ===== CEK DEPENDENSI =====
command -v zip >/dev/null 2>&1 || { echo -e "${RED}zip belum terinstall!${NC}"; pkg install zip -y; }
command -v rar >/dev/null 2>&1 || { echo -e "${RED}rar belum terinstall!${NC}"; pkg install rar -y; }

# ===== MENU =====
echo -e "${CYAN}=== KOMPRESES FOLDER TERMUX ===${NC}"
echo -e "${YELLOW}1) Kompres folder ke RAR"
echo -e "2) Kompres folder ke ZIP"
echo -e "3) Kompres folder ke RAR dengan password"
echo -e "4) Kompres folder ke ZIP dengan password${NC}"
read -p "Pilih opsi (1-4): " opsi

read -p "Masukkan nama folder: " folder

if [ ! -d "$folder" ]; then
    echo -e "${RED}Folder tidak ditemukan!${NC}"
    exit 1
fi

read -p "Masukkan nama file output (tanpa ekstensi): " outfile

case $opsi in
1)
    rar a "${outfile}.rar" "$folder"
    echo -e "${GREEN}Berhasil dikompres ke ${outfile}.rar${NC}"
    ;;
2)
    zip -r "${outfile}.zip" "$folder"
    echo -e "${GREEN}Berhasil dikompres ke ${outfile}.zip${NC}"
    ;;
3)
    read -sp "Masukkan password RAR: " pass
    echo
    rar a -p"$pass" "${outfile}.rar" "$folder"
    echo -e "${GREEN}Berhasil dikompres ke ${outfile}.rar dengan password${NC}"
    ;;
4)
    read -sp "Masukkan password ZIP: " pass
    echo
    zip -r -P "$pass" "${outfile}.zip" "$folder"
    echo -e "${GREEN}Berhasil dikompres ke ${outfile}.zip dengan password${NC}"
    ;;
*)
    echo -e "${RED}Opsi tidak valid!${NC}"
    ;;
esac