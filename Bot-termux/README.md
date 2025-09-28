
😎 CatBot (Terminal Chatbot)

CatBot adalah chatbot sederhana berbasis Python yang berjalan di Termux atau terminal Linux.
ChatBot ini bisa menyimpan jawaban umum maupun script dalam file JSON, serta punya menu interaktif untuk melihat, menambah, menghapus, dan mengedit data.


---

📌 Fitur Utama

Simpan jawaban umum (teks singkat).

Simpan script multi-baris (pakai Enter 2x kosong untuk selesai).

Lihat, edit (via nano), dan hapus data.

Efek animasi spinner dan progress bar biar lebih hidup.

Tampilan chat interaktif dengan emoji.

Data tersimpan di folder memory/ dalam format JSON.



---

📂 Struktur File

memory/
 ├── data.json      # Menyimpan jawaban umum
 ├── datafile.json  # Menyimpan script
catbot.py           # File utama (script chatbot)


---

🚀 Cara Install & Jalankan

1. Clone / Simpan Script

git clone <repo-anda>
cd <repo-anda>

Atau kalau cuma pakai Termux:

nano catbot.py
# paste script yang ada

2. Install Python (jika belum)

pkg install python

3. Jalankan

python catbot.py


---

🎮 Cara Pakai

Ketik teks apapun → jika sudah ada di database, bot akan menjawab.

Kalau belum ada:

Pilih A untuk ajarin jawaban umum.

Pilih B untuk simpan script multi-baris.

Pilih C untuk batal.


Ketik + → buka menu manajemen data.

Ketik x → keluar dari chatbot.



---

📑 Menu Tambahan (+)

[1] Lihat data umum

[2] Lihat script

[3] Edit data umum (nano)

[4] Edit script (nano)

[5] Hapus data (pilih umum / script / semua)

[X] Kembali



---

🗑️ Contoh Hapus Semua Data

Dari menu +, pilih 5 → ALL untuk menghapus semua data.


---

💡 Tips

Data tersimpan otomatis di folder memory/.

Bisa backup file data.json & datafile.json untuk pindah ke perangkat lain.

Jalankan di layar penuh terminal biar tampilan lebih rapi.


