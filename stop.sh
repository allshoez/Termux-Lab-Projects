echo '#!/bin/bash
echo "=== Termux FORCE STOP SEMUA ==="

# Ambil semua PID milik user Termux
USER=$(whoami)
PIDS=$(ps -u $USER -o pid=)

# Kill semua proses milik user Termux kecuali skrip ini sendiri
for pid in $PIDS; do
    if [ "$pid" != $$ ]; then
        kill -9 $pid 2>/dev/null
    fi
done

echo "⚠️ Semua proses Termux dimatikan! Seperti force stop aplikasi Android."' > ~/stop.sh