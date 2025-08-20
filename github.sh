

#!/usr/bin/env bash
set -e

# ====== Config opsional ======
DEFAULT_BRANCH="main"
# Kalau mau fixed remote, isi di sini. Kalau kosong, skrip akan nanya saat A dipilih.
FIXED_REMOTE_URL=""

# ====== Util ======
has_cmd() { command -v "$1" >/dev/null 2>&1; }

err() { echo "✖ $*" >&2; }
ok()  { echo "✔ $*"; }

banner() {
  echo
  echo "========================================"
  echo "   Git Launcher (Termux-style) - ABC    "
  echo "========================================"
  echo "A) Setup awal (init + set remote + first push)"
  echo "B) Update cepat (add . + commit + push)"
  echo "C) Cek status & 5 log terakhir"
  echo "----------------------------------------"
  echo -n "Pilih [A/B/C]: "
}

require_git() {
  if ! has_cmd git; then
    err "git belum terpasang. Di Termux: pkg install git"
    exit 1
  fi
}

ensure_repo() {
  if [ ! -d ".git" ]; then
    err "Belum ada repo Git di folder ini. Jalankan opsi A dulu."
    exit 1
  fi
}

read_nonempty() {
  local prompt="$1"
  local var
  while true; do
    read -r -p "$prompt" var
    [ -n "$var" ] && { echo "$var"; return; }
    echo "Input tidak boleh kosong."
  done
}

first_push() {
  require_git

  # init kalau belum ada
  if [ ! -d ".git" ]; then
    ok "Inisialisasi repo Git..."
    git init
  else
    ok "Repo Git sudah ada, lanjut setup..."
  fi

  # set branch default
  CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
  if [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
    ok "Set branch ke $DEFAULT_BRANCH"
    git branch -M "$DEFAULT_BRANCH" 2>/dev/null || git checkout -B "$DEFAULT_BRANCH"
  fi

  # set remote
  if git remote get-url origin >/dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    ok "Remote origin sudah ada: $REMOTE_URL"
  else
    if [ -n "$FIXED_REMOTE_URL" ]; then
      REMOTE_URL="$FIXED_REMOTE_URL"
      ok "Pakai fixed remote: $REMOTE_URL"
    else
      REMOTE_URL=$(read_nonempty "Masukkan URL repo GitHub (HTTPS/SSH): ")
    fi
    git remote add origin "$REMOTE_URL"
    ok "Remote origin ditambahkan."
  fi

  # add + first commit kalau belum ada commit
  if ! git rev-parse HEAD >/dev/null 2>&1; then
    ok "Menambahkan semua file..."
    git add .
    msg="first commit"
    ok "Commit: $msg"
    git commit -m "$msg" || true
  fi

  ok "Push pertama ke $DEFAULT_BRANCH..."
  git push -u origin "$DEFAULT_BRANCH"
  ok "Selesai. 🚀"
}

quick_update() {
  require_git
  ensure_repo

  ok "Menambahkan semua perubahan..."
  git add .

  # pesan commit
  read -r -p "Pesan commit (kosongkan untuk auto): " MSG
  if [ -z "$MSG" ]; then
    MSG="update $(date '+%Y-%m-%d %H:%M:%S')"
  fi

  ok "Commit: $MSG"
  # commit boleh kosong (no changes) -> jangan error
  if git diff --cached --quiet; then
    echo "Tidak ada perubahan terindeks. Skip commit."
  else
    git commit -m "$MSG"
  fi

  # pastikan ada upstream
  BRANCH=$(git rev-parse --abbrev-ref HEAD)
  if ! git rev-parse --abbrev-ref "@{u}" >/dev/null 2>&1; then
    ok "Set upstream: origin/$BRANCH"
    git push -u origin "$BRANCH"
  else
    ok "Push ke origin/$BRANCH"
    git push
  fi

  ok "Update selesai. ✅"
}

status_log() {
  require_git
  ensure_repo

  echo
  echo "------ git status ------"
  git status
  echo
  echo "------ 5 commit terakhir ------"
  git --no-pager log -5 --oneline --graph --decorate
}

main() {
  trap 'echo; err "Dibatalkan."; exit 1' INT

  banner
  read -r CH
  case "${CH^^}" in
    A) first_push ;;
    B) quick_update ;;
    C) status_log ;;
    *) err "Pilihan tidak dikenal."; exit 1 ;;
  esac
}

main "$@"


