import json, os, random
from colorama import Fore, Style, init

init(autoreset=True)

DATA_FILE = "data.json"
BACKUP_DIR = "backup"
BACKUP_FILE = "data.backup.json"

COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Pastikan folder backup ada
os.makedirs(BACKUP_DIR, exist_ok=True)

# Load data
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                raw_data = json.load(f)
                data = {k.strip().lower(): v for k, v in raw_data.items()}
            except:
                data = {}
    else:
        data = {}

load_data()

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Backup otomatis
    backup_path = os.path.join(BACKUP_DIR, BACKUP_FILE)
    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def manual_backup():
    backup_path = os.path.join(BACKUP_DIR, BACKUP_FILE)
    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(Fore.CYAN + f"✔️ Backup berhasil: {backup_path}")

def input_multiline(prompt):
    print(prompt + " (Enter kosong = selesai / batal):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def clear_screen():
    os.system("clear")  # 'cls' kalau Windows

def show_header():
    print(Fore.CYAN + "=== CatBot Python ===")
    print(Fore.YELLOW + "  L = Lihat data")
    print(Fore.YELLOW + "  E = Edit data")
    print(Fore.YELLOW + "  D = Hapus data")
    print(Fore.YELLOW + "  CD = Cari data")
    print(Fore.YELLOW + "  BD = Backup Data")
    print(Fore.YELLOW + "  SD = Source Data")
    print(Fore.YELLOW + "  X = Exit\n")

def tampil_bot(jawaban):
    warna = random.choice(COLORS)
    print(f"{warna}Bot  :{Style.RESET_ALL}\n{jawaban}")

while True:
    clear_screen()
    show_header()
    tanya = input(Fore.GREEN + "Anda : " + Style.RESET_ALL).strip()
    if not tanya:
        continue

    tanya_lc = tanya.lower().strip()

    if tanya_lc == "x":
        print(Fore.CYAN + "CatBot keluar. Bye!")
        break

    elif tanya_lc == "l":
        if data:
            print(Fore.MAGENTA + json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(Fore.RED + "Belum ada data tersimpan.")
        input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
        continue

    elif tanya_lc == "e":
        key = input(Fore.YELLOW + "Pertanyaan yang mau diedit: " + Style.RESET_ALL).strip().lower()
        if key in data:
            print(Fore.YELLOW + f"Jawaban lama:\n{data[key]}")
            baru = input_multiline(Fore.GREEN + "Jawaban baru")
            if baru:
                data[key] = baru
                save_data()
                print(Fore.CYAN + "✔️ Jawaban berhasil diupdate dan backup dibuat.")
            else:
                print(Fore.RED + "❌ Edit dibatalkan.")
        else:
            print(Fore.RED + "❌ Pertanyaan itu belum ada di data.")
        input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
        continue

    elif tanya_lc == "d":
        key = input(Fore.YELLOW + "Pertanyaan yang mau dihapus: " + Style.RESET_ALL).strip().lower()
        if key in data:
            confirm = input(Fore.RED + f"Yakin hapus '{key}'? (y/n): " + Style.RESET_ALL).strip().lower()
            if confirm == "y":
                del data[key]
                save_data()
                print(Fore.CYAN + "✔️ Data berhasil dihapus dan backup dibuat.")
            else:
                print(Fore.YELLOW + "↩️  Hapus dibatalkan.")
        else:
            print(Fore.RED + "❌ Pertanyaan itu tidak ada di data.")
        input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
        continue

    elif tanya_lc == "cd":
        keyword = input(Fore.GREEN + "Masukkan kata kunci untuk dicari: " + Style.RESET_ALL).strip().lower()
        found = False
        for key, val in data.items():
            if keyword in key.lower() or keyword in val.lower():
                display_key = key.replace(keyword, Fore.YELLOW + keyword + Style.RESET_ALL)
                display_val = val.replace(keyword, Fore.YELLOW + keyword + Style.RESET_ALL)
                tampil_bot(f"{display_key} :\n{display_val}")
                found = True
        if not found:
            print(Fore.RED + "❌ Tidak ditemukan data yang cocok.")
        input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
        continue

    elif tanya_lc == "bd":
        manual_backup()
        input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
        continue

    elif tanya_lc == "sd":
        os.system(f"nano {DATA_FILE}")
        load_data()
        input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
        continue

    # Jawaban bot
    found = False
    for key, val in data.items():
        if key in tanya_lc or tanya_lc in key:
            tampil_bot(val)
            found = True
            break

    if not found:
        print(Fore.RED + "Bot  : (Belum ada jawaban)")
        jawaban = input_multiline(Fore.GREEN + "Isi jawaban")
        if jawaban:
            data[tanya_lc] = jawaban
            save_data()
            print(Fore.CYAN + "✔️ Jawaban disimpan dan backup dibuat.")
        else:
            print(Fore.YELLOW + "↩️  Batal, tidak disimpan.")

    input(Fore.GREEN + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)