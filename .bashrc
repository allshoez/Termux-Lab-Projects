

# === Alias Python Scripts ===


alias tes-='> tes.py && nano tes.py'
alias tes='python3 tes.py'
alias total='python3 buku.py'
alias bt='python3 bukutoko.py'
alias buku-='> buku.py && nano buku.py'
alias catatan='cd /sdcard/catatan && python3 app.py'
alias tabel='python tabel.py'
alias fm-='> file_manager.py && nano file_manager.py'
alias fm='python3 file_manager.py'
alias cfm='cat file_manager.py'
alias catat='cd ~/catatan_penjualan && python3 main.py'



# == Menu ===

alias menu='bash ~/menu.sh'
alias manager='python ~/manager.py'
alias bot='python bot.py'
alias cekwa='bash ~/cekwa.sh'
alias botcat='python ~/botcat.py'
alias z4='bash ~/z4.sh'
alias backup='cd ~/backup'
alias ai='python ~/ai.py'
alias flask-gen='python ~/flask-gen.py'
alias botjs='node catbot.js'
alias convert='bash ~/convert.sh'
alias torent='py torent.py'
alias srt='python srt.py'
alias l='ls'
alias c='cd'
alias resi='python3 resi.py'
alias bf='bash ~/buatFile.sh'
alias catbot='python catbot.py'
alias dll='bash ~/dl.sh'

alias sub='python sub.py'
alias sub-='> sub.py && nano sub.py'
alias ram='bash ~/cek-memory.sh'



alias xx='bash ~/stop.sh'
alias yarn='cd /sdcard/Bot && yarn dev'
alias catat='python ~/yarn.py'

# === Alias Shell Scripts ===
alias memory='cd ~/memory && ls && cd'
alias dd='bash ~/download.sh'
alias kompres='bash ~/kompres-video.sh'

alias yt='$HOME/yt.in'
alias github='$HOME/github.in'

alias dl='bash ~/dl.in'
alias data='nano ~/data.json'

# Edit bash_profile + reload otomatis
alias ebp='nano ~/.bash_profile && source ~/.bash_profile'


# ==== Alias Praktis Termux ====
alias rc='nano ~/.bashrc && source ~/.bashrc'
alias openhtml='termux-open '
alias httpserver='python3 -m http.server 8080'
alias cbot='python /sdcard/Bot/app.py'

# ===== Termux Config & Environment =====
export PATH=$HOME/bin:/data/data/com.termux/files/usr/bin:$PATH
export TERM=xterm-256color

# Aliases standar
alias nano='nano'
alias ls='ls --color=auto'
alias ll='ls -lah'
alias cls='clear'
alias sc='cd /sdcard && ls'

# Alias Backup & Restore Termux
alias backup-termux='tar -czvf /sdcard/termux-backup.tar.gz -C /data/data/com.termux/files/home .'
alias restore-termux='tar -xzvf /sdcard/termux-backup.tar.gz -C /data/data/com.termux/files/home'

# === Folder navigasi cepat ===
alias cd.='cd ..'
alias cd..='cd ..'
alias trash='cd ~/trash'

# === JSON data ===


# Fungsi buka file cepat
alias sdcard='cd /sdcard && ls'

# Buat alias aman
alias n=' nano'
alias py='python3'
alias x='exit'
alias dns='bash ~/dns.sh'

# Prompt panah kedip terus-menerus
export PS1="\[\033[5;32m\]➤\[\033[0m\] "


alias 43='python3 /sdcard/conv_mp3/run.py'
alias mp3='python3 /sdcard/conv_mp3/app.py'
alias conv='cd /sdcard/conv_mp3'
