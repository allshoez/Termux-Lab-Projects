# ===== Termux Config & Environment =====

# PATH standar
export PATH=$HOME/bin:/data/data/com.termux/files/usr/bin:$PATH

# Terminal type standar
export TERM=xterm-256color

# Aliases standar
alias nano='nano'
alias ls='ls --color=auto'
alias ll='ls -lah'

# Fungsi buka file cepat
edit() {
    if [ -z "$1" ]; then
        echo "Gunakan: edit <nama_file>"
    else
        nano "$1"
    fi
}

# Fungsi buka file-manager script
fm() {
    if [ -f "$HOME/file-manager.in" ]; then
        bash "$HOME/file-manager.in"
    else
        echo "File manager tidak ditemukan di $HOME"
    fi
}

# Alias Backup & Restore Termux (opsional)
alias backup-termux='tar -czvf /sdcard/termux-backup.tar.gz -C /data/data/com.termux/files/home .'
alias restore-termux='tar -xzvf /sdcard/termux-backup.tar.gz -C /data/data/com.termux/files/home'

# Prompt hijau dengan panah
GREEN='\[\033[0;32m\]'   # hijau
RESET='\[\033[0m\]'
export PS1="${GREEN}➤ ${RESET}"
