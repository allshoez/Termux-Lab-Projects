#!/data/data/com.termux/files/usr/bin/bash

# Warna
CYAN="\033[1;36m"
GREEN="\033[1;32m"
RESET="\033[0m"

# Fungsi konversi ke GB (base 1000, ala pabrikan)
toGB() {
    awk -v val=$1 'BEGIN { printf "%.2f GB", val/1000/1000/1000 }'
}

# Cek RAM
cek_memory() {
    echo -e "${CYAN}=== MEMORY (RAM) ===${RESET}"
    free -k | awk 'NR==2{print $2, $3, $4}' | while read total used free; do
        echo -e "${GREEN}Total RAM   :${RESET} $(toGB $((total*1024)))"
        echo -e "${GREEN}Dipakai     :${RESET} $(toGB $((used*1024)))"
        echo -e "${GREEN}Sisa        :${RESET} $(toGB $((free*1024)))"
    done
    echo ""
}

# Cek Storage
cek_storage() {
    echo -e "${CYAN}=== STORAGE (Internal) ===${RESET}"
    df -k /data | awk 'NR==2{print $2*1024, $3*1024, $4*1024}' | while read total used free; do
        echo -e "${GREEN}Total Storage:${RESET} $(toGB $total)"
        echo -e "${GREEN}Dipakai      :${RESET} $(toGB $used)"
        echo -e "${GREEN}Sisa         :${RESET} $(toGB $free)"
    done
    echo ""
}

# Jalankan cek
cek_memory
cek_storage