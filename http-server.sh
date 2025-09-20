
#!/bin/bash

echo "=== Termux HTTP Server Fixed All-in-One ==="

echo "Masukkan path folder proyek:"
read ROOT
ROOT="${ROOT/#\~/$HOME}"

if [ ! -d "$ROOT" ]; then
    echo "Folder $ROOT tidak ditemukan!"
    exit 1
fi

cd "$ROOT" || { echo "Gagal masuk folder $ROOT"; exit 1; }

echo "Folder proyek: $ROOT"

echo "Masukkan port server (default 3000):"
read PORT
PORT=${PORT:-3000}

# Cek file di folder itu saja (tidak scan subfolder)
if [ -f "package.json" ]; then
    echo "package.json ditemukan → jalankan yarn dev/start..."
    if grep -q '"dev"' package.json; then
        yarn install
        yarn dev &>/dev/null &
    elif grep -q '"start"' package.json; then
        yarn install
        yarn start &>/dev/null &
    else
        [ -f "index.js" ] && node index.js &>/dev/null &
    fi

elif [ -f "server.js" ] || [ -f "index.js" ] || ls *.mjs 1> /dev/null 2>&1; then
    FILE=$(ls server.js index.js *.mjs | head -n1)
    echo "File JS ditemukan ($FILE) → jalankan Node.js..."
    node "$FILE" &>/dev/null &

elif [ -f "app.py" ]; then
    echo "Python app.py ditemukan → jalankan Flask..."
    export FLASK_APP=app.py
    flask run --host=0.0.0.0 --port=$PORT &>/dev/null &

elif [ -f "index.html" ]; then
    echo "index.html ditemukan → jalankan static server..."
    python3 -m http.server $PORT &>/dev/null &

else
    echo "Folder tidak punya file server → jalankan static server minimal jika ada index.html"
fi

URL="http://127.0.0.1:$PORT"
echo "Membuka browser → $URL"
termux-open-url "$URL"

echo "Proyek dijalankan!"
