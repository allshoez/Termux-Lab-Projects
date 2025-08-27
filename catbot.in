
#!/data/data/com.termux/files/usr/bin/env bash
# CatBot Termux Pro - Warna-warni + Learn + Spinner + Confirm

DATA_FILE="data.json"

# Warna
YELLOW='\033[1;33m'
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
RESET='\033[0m'

# Spinner sederhana
spin() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ -d /proc/$pid ]; do
        for i in $(seq 0 3); do
            printf "\r⏳ ${spinstr:$i:1} Loading..."
            sleep $delay
        done
    done
    printf "\r"
}

# Ambil jawaban
get_response() {
    local question="$1"
    if [ -f "$DATA_FILE" ]; then
        local answer=$(jq -r --arg q "$question" '.[] | select(.Tanya==$q) | .Jawab' "$DATA_FILE")
        echo "$answer"
    else
        echo ""
    fi
}

# Simpan jawaban baru
save_answer() {
    local question="$1"
    local answer="$2"
    if [ ! -f "$DATA_FILE" ]; then
        echo "[]" > "$DATA_FILE"
    fi
    tmp=$(mktemp)
    jq --arg t "$question" --arg j "$answer" '. += [{"Tanya": $t, "Jawab": $j}]' "$DATA_FILE" > "$tmp" && mv "$tmp" "$DATA_FILE"
}

echo -e "${CYAN}=== 😎 CatBot Manager Pro 🤖 ===${RESET}"
echo -e "[X] = Keluar program"
echo ""

while true; do
    read -p "$(echo -e "${YELLOW}😎 you: ${RESET}")" user_input

    # Exit
    [[ "$user_input" =~ ^[Xx]$ ]] && { echo -e "${CYAN}🤖 CatBot: Sampai jumpa! 👋${RESET}"; break; }

    # Spinner saat mencari jawaban
    sleep 0.05 & pid=$!
    spin $pid
    wait $pid

    response=$(get_response "$user_input")

    if [ -n "$response" ]; then
        echo -e "${YELLOW}🤖 CatBot: ${RESET}$response"
    else
        echo -e "${YELLOW}🤖 CatBot: Maaf, saya belum tahu jawabannya.${RESET}"
        echo -e "${RED} A) Ajari jawaban baru${RESET}"
        echo -e "${YELLOW} B) Lewati${RESET}"
        echo -e "${GREEN} C) Keluar${RESET}"
        read -p "$(echo -e "${YELLOW}> ${RESET}")" pilihan
        case "$pilihan" in
            [Aa])
                read -p "$(echo -e "${YELLOW}Masukkan jawaban: ${RESET}")" new_answer
                echo -e "Jawaban yang akan disimpan: $new_answer"
                read -p "$(echo -e "${YELLOW}Konfirmasi simpan? (y/n): ${RESET}")" confirm
                if [[ "$confirm" =~ ^[Yy]$ ]]; then
                    save_answer "$user_input" "$new_answer"
                    echo -e "${CYAN}🤖 CatBot: Terima kasih, saya sudah belajar!${RESET}"
                else
                    echo -e "${CYAN}🤖 CatBot: Jawaban dibatalkan.${RESET}"
                fi
                ;;
            [Bb])
                echo -e "${CYAN}🤖 CatBot: Oke, lanjut...${RESET}"
                ;;
            [Cc])
                echo -e "${CYAN}🤖 CatBot: Sampai jumpa! 👋${RESET}"
                break
                ;;
            *)
                echo -e "${CYAN}🤖 CatBot: Pilihan tidak dikenal.${RESET}"
                ;;
        esac
    fi
done
