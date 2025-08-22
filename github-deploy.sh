#!/bin/bash

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;36m"
CYAN="\033[0;36m"
RESET="\033[0m"

# Pilih bahasa
echo -e "${CYAN}=== Pilih Bahasa / Choose Language ===${RESET}"
echo -e "1) Bahasa Indonesia\n2) English"
read -p "Pilih [1/2]: " LANG_OPT

if [ "$LANG_OPT" = "2" ]; then
    L_PROJECT="Enter project folder path:"
    L_TOKEN_ASK="Do you already have GitHub Token?"
    L_TOKEN_OPTION="A) Yes  B) Guide  C) Exit"
    L_TOKEN_PROMPT="Enter token:"
    L_USERNAME="GitHub Username:"
    L_REPO="Repository name:"
    L_FOLDER_NOT_FOUND="Folder not found!"
    L_TOKEN_FOUND="Token found, using existing token."
    L_REPO_EXISTS="Repo exists."
    L_REPO_CREATE="Repo does not exist, creating new repo..."
    L_REPO_CREATED="Repo created or already exists."
    L_REPO_FAIL="Failed to create repo, check token or connection."
    L_PULL="Remote exists, pulling updates..."
    L_PULL_EMPTY="Repo empty or new"
    L_NO_CHANGE="No new changes"
    L_PUSH_FAIL="Push failed, retry"
    L_DONE="=== Done! All files pushed to GitHub ==="
    L_TIPS="Tip: Next time just run this script again."
else
    L_PROJECT="Masukkan path folder project:"
    L_TOKEN_ASK="Apakah sudah punya GitHub Token?"
    L_TOKEN_OPTION="A) Sudah  B) Panduan  C) Keluar"
    L_TOKEN_PROMPT="Masukkan token:"
    L_USERNAME="Username GitHub:"
    L_REPO="Nama repo:"
    L_FOLDER_NOT_FOUND="Folder tidak ditemukan!"
    L_TOKEN_FOUND="Token ditemukan, menggunakan token lama."
    L_REPO_EXISTS="Repo sudah ada."
    L_REPO_CREATE="Repo belum ada, membuat repo baru..."
    L_REPO_CREATED="Repo berhasil dibuat atau sudah ada."
    L_REPO_FAIL="Gagal buat repo, cek token atau koneksi."
    L_PULL="Remote ada, menarik update..."
    L_PULL_EMPTY="Repo kosong atau baru"
    L_NO_CHANGE="Tidak ada perubahan baru"
    L_PUSH_FAIL="Push gagal, retry"
    L_DONE="=== Selesai! Semua file sudah di-push ke GitHub ==="
    L_TIPS="Tips AI: Update berikutnya cukup jalankan script ini lagi."
fi

# Cek git
command -v git >/dev/null 2>&1 || { echo -e "${RED}Git belum terinstall! pkg install git${RESET}"; exit 1; }

# Pilih opsi awal
echo -e "${CYAN}=== Opsi Awal ===${RESET}"
echo -e "A) Buat repo GitHub dulu"
echo -e "B) Masukkan file ke dalam repo GitHub"
echo -e "C) Masukkan folder project"
echo -e "D) Salin folder SDCard ke Home Termux"
echo -e "E) Hapus folder dan isinya di Home Termux"
echo -e "F) Back"
read -p "Pilih [A-F]: " INIT_OPTION

# Setup GitHub token jika opsi A/B/C
TOKEN_FILE="$HOME/.gh_token"
if [[ "$INIT_OPTION" =~ ^[AaBbCc]$ ]]; then
    if [ -f "$TOKEN_FILE" ]; then
        GH_TOKEN=$(cat "$TOKEN_FILE")
        echo -e "${GREEN}$L_TOKEN_FOUND${RESET}"
    else
        while true; do
            echo -e "${BLUE}$L_TOKEN_ASK${RESET}"
            echo -e "$L_TOKEN_OPTION"
            read -p "Pilih [A/B/C]: " OPTION
            case "$OPTION" in
                A|a) read -p "$(echo -e ${YELLOW}$L_TOKEN_PROMPT ${RESET})" GH_TOKEN; break;;
                B|b) echo -e "${GREEN}https://github.com/settings/tokens${RESET}"; read -p "$(echo -e ${YELLOW}$L_TOKEN_PROMPT ${RESET})" GH_TOKEN; break;;
                C|c) echo -e "${RED}Keluar${RESET}"; exit 0;;
                *) echo -e "${RED}Opsi salah${RESET}";;
            esac
        done
        echo "$GH_TOKEN" > "$TOKEN_FILE"
        echo -e "${GREEN}Token tersimpan di $TOKEN_FILE${RESET}"
    fi
    export GH_TOKEN

    # Input username + repo
    while true; do
        read -p "$(echo -e ${YELLOW}$L_USERNAME ${RESET})" USERNAME
        read -p "$(echo -e ${YELLOW}$L_REPO ${RESET})" REPO
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GH_TOKEN" https://api.github.com/repos/$USERNAME/$REPO)
        if [ "$STATUS" -eq 200 ] || [ "$STATUS" -eq 404 ]; then break; else echo -e "${RED}Username atau repo salah! Cek kembali.${RESET}"; fi
    done
    REPO_URL="https://$USERNAME:$GH_TOKEN@github.com/$USERNAME/$REPO.git"
fi

# ===================== MENU OPSI =====================
if [[ "$INIT_OPTION" =~ ^[Aa]$ ]]; then
    # Opsi A: Buat repo GitHub baru
    echo -e "${GREEN}Opsi buat repo dipilih.${RESET}"
    if [ "$STATUS" -eq 404 ]; then
        echo -e "${YELLOW}$L_REPO_CREATE${RESET}"
        CREATE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GH_TOKEN" -d "{\"name\":\"$REPO\",\"private\":false}" https://api.github.com/user/repos)
        if [ "$CREATE" -eq 201 ] || [ "$CREATE" -eq 422 ]; then echo -e "${GREEN}$L_REPO_CREATED${RESET}"; else echo -e "${RED}$L_REPO_FAIL${RESET}"; exit 1; fi
    else
        echo -e "${GREEN}$L_REPO_EXISTS${RESET}"
    fi

elif [[ "$INIT_OPTION" =~ ^[Bb]$ ]]; then
    # Opsi B: Masukkan file ke repo
    echo -e "${GREEN}Opsi masukkan file ke repo dipilih.${RESET}"
    echo -e "${CYAN}Dimana file berada?${RESET}"
    echo -e "A) Sdcard\nB) Home Termux"
    read -p "Pilih [A/B]: " FILE_LOC

    FILES_TO_ADD=()
    if [[ "$FILE_LOC" =~ ^[Aa]$ ]]; then
        read -p "Masukkan path file lengkap dari /sdcard (pisah koma jika lebih dari satu): " FILE_INPUT
        IFS=',' read -ra FILES <<< "$FILE_INPUT"
        for f in "${FILES[@]}"; do
            if [ -f "/sdcard/$f" ]; then FILES_TO_ADD+=("/sdcard/$f"); else echo -e "${RED}File /sdcard/$f tidak ditemukan!${RESET}"; fi
        done
    elif [[ "$FILE_LOC" =~ ^[Bb]$ ]]; then
        read -p "Masukkan path file lengkap dari Home Termux (pisah koma jika lebih dari satu): " FILE_INPUT
        IFS=',' read -ra FILES <<< "$FILE_INPUT"
        for f in "${FILES[@]}"; do
            if [ -f "$HOME/$f" ]; then FILES_TO_ADD+=("$HOME/$f"); else echo -e "${RED}File $HOME/$f tidak ditemukan!${RESET}"; fi
        done
    else
        echo -e "${RED}Opsi tidak valid, keluar${RESET}"; exit 1
    fi

    read -p "Masukkan nama folder proyek lokal untuk commit file: " PROJECT_NAME
    PROJECT_DIR="$HOME/$PROJECT_NAME"
    mkdir -p "$PROJECT_DIR"

    for f in "${FILES_TO_ADD[@]}"; do
        cp "$f" "$PROJECT_DIR/"
        echo -e "${GREEN}File $(basename $f) ditambahkan ke $PROJECT_DIR${RESET}"
    done

    cd "$PROJECT_DIR" || exit 1
    [ ! -d ".git" ] && git init && git branch -M main
    git remote set-url origin $REPO_URL 2>/dev/null || git remote add origin $REPO_URL
    echo ".gh_token" >> .gitignore 2>/dev/null
    git add .
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    git commit -m "Add file(s) $TIMESTAMP" || echo -e "${YELLOW}$L_NO_CHANGE${RESET}"
    for i in 1 2 3; do git push -u origin main && break; echo -e "${RED}$L_PUSH_FAIL ($i/3)...${RESET}"; sleep 2; done
    echo -e "${GREEN}$L_DONE${RESET}"

elif [[ "$INIT_OPTION" =~ ^[Cc]$ ]]; then
    # Opsi C: Masukkan folder project
    echo -e "${GREEN}Opsi masukkan folder project dipilih.${RESET}"
    echo -e "${CYAN}Dimana folder project?${RESET}"
    echo -e "A) Sdcard\nB) Home Termux"
    read -p "Pilih [A/B]: " LOC_OPTION

    if [[ "$LOC_OPTION" =~ ^[Aa]$ ]]; then
        read -p "Masukkan nama folder project: " PROJECT_NAME
        PROJECT_DIR="$HOME/$PROJECT_NAME"
        mkdir -p "$PROJECT_DIR"
        cp -r "/sdcard/$PROJECT_NAME/" "$PROJECT_DIR/"
    elif [[ "$LOC_OPTION" =~ ^[Bb]$ ]]; then
        read -p "Masukkan nama folder project di Home Termux: " PROJECT_NAME
        PROJECT_DIR="$HOME/$PROJECT_NAME"
        [ -d "$PROJECT_DIR" ] || { echo -e "${RED}Folder tidak ditemukan!${RESET}"; exit 1; }
    else
        echo -e "${RED}Opsi tidak valid, keluar${RESET}"; exit 1
    fi

    cd "$PROJECT_DIR" || exit 1
    [ ! -d ".git" ] && git init && git branch -M main
    git remote set-url origin $REPO_URL 2>/dev/null || git remote add origin $REPO_URL
    echo ".gh_token" >> .gitignore 2>/dev/null
    git add .
    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
    git commit -m "Add project folder $TIMESTAMP" || echo -e "${YELLOW}$L_NO_CHANGE${RESET}"
    for i in 1 2 3; do git push -u origin main && break; echo -e "${RED}$L_PUSH_FAIL ($i/3)...${RESET}"; sleep 2; done
    echo -e "${GREEN}$L_DONE${RESET}"

elif [[ "$INIT_OPTION" =~ ^[Dd]$ ]]; then
    # Opsi D: Salin folder SDCard ke Home Termux
    read -p "Masukkan nama folder di SDCard: " SD_FOLDER
    read -p "Masukkan nama folder tujuan di Home Termux: " HOME_FOLDER
    mkdir -p "$HOME/$HOME_FOLDER"
    cp -r "/sdcard/$SD_FOLDER/" "$HOME/$HOME_FOLDER/"
    echo -e "${GREEN}Folder /sdcard/$SD_FOLDER disalin ke $HOME/$HOME_FOLDER${RESET}"

elif [[ "$INIT_OPTION" =~ ^[Ee]$ ]]; then
    # Opsi E: Hapus folder di Home Termux
    read -p "Masukkan nama folder di Home Termux yang ingin dihapus: " DEL_FOLDER
    FOLDER_PATH="$HOME/$DEL_FOLDER"
    if [ -d "$FOLDER_PATH" ]; then
        read -p "Yakin ingin menghapus $FOLDER_PATH beserta isinya? [y/N]: " CONFIRM
        if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
            rm -rf "$FOLDER_PATH"
            echo -e "${GREEN}Folder $FOLDER_PATH berhasil dihapus${RESET}"
        else
            echo -e "${YELLOW}Hapus dibatalkan${RESET}"
        fi
    else
        echo -e "${RED}Folder $FOLDER_PATH tidak ditemukan!${RESET}"
    fi

elif [[ "$INIT_OPTION" =~ ^[Ff]$ ]]; then
    # Opsi F: Back / keluar
    echo -e "${CYAN}Kembali / keluar dari script${RESET}"
    exit 0

else
    echo -e "${RED}Opsi tidak valid!${RESET}"
    exit 1
fi

echo -e "${GREEN}=== Selesai ===${RESET}"
