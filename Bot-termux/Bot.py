
#!/data/data/com.termux/files/usr/bin/env python3
import os, json, sys, time
from itertools import cycle

# ======== Setup ========
DATA_DIR = "memory"
DATA_GENERAL = os.path.join(DATA_DIR, "data.json")
DATA_SCRIPT = os.path.join(DATA_DIR, "datafile.json")
os.makedirs(DATA_DIR, exist_ok=True)
for f in [DATA_GENERAL, DATA_SCRIPT]:
    if not os.path.isfile(f):
        with open(f, "w") as fp: json.dump({}, fp)

# ======== Warna ========
YELLOW = '\033[1;33m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
MAGENTA = '\033[1;35m'
RESET = '\033[0m'

# ======== Fungsi ========
def load(file):
    with open(file) as f:
        try: return json.load(f)
        except: return {}

def save(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=2)

def spinner(task="Processing", duration=0.5):
    spin = cycle(['|', '/', '-', '\\'])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f"\r{CYAN}{task} {next(spin)}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " "*(len(task)+2) + "\r")

def progress_bar(task="Deleting", total=20, delay=0.05):
    for i in range(total+1):
        bar = '#' * i + '-' * (total-i)
        sys.stdout.write(f"\r{RED}{task}: [{bar}]{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

# ======== Chat History ========
chat_history = []

def show_chat():
    os.system("clear")
    print(f"{CYAN}=== 😎 CatBot === [ + ] ==={RESET}")
    for user, bot in chat_history:
        print(f"{YELLOW}😎 you: {RESET}{user}")
        print(f"{MAGENTA}🤖 Bot: {RESET}{bot}")
        print(f"{CYAN}{'-'*40}{RESET}")
    print("")

# ======== Fungsi Tambah Data ========
def add_general(key):
    print(f"{YELLOW}Masukkan jawaban umum (Enter 1x per line):{RESET}")
    line = input()
    data = load(DATA_GENERAL)
    data[key] = line
    save(DATA_GENERAL, data)
    spinner("Menyimpan")
    print(f"{GREEN}🤖 Bot: Jawaban umum tersimpan!{RESET}")

def add_script(key):
    print(f"{YELLOW}Masukkan script (Enter 2x kosong untuk selesai):{RESET}")
    lines = []
    empty_count = 0
    while True:
        l = input()
        if l == "":
            empty_count += 1
        else:
            empty_count = 0
            lines.append(l)
        if empty_count >= 2: break
    data = load(DATA_SCRIPT)
    data[key] = "\n".join(lines)
    save(DATA_SCRIPT, data)
    spinner("Menyimpan")
    print(f"{GREEN}🤖 Bot: Script tersimpan!{RESET}")

def view_data(file, title):
    data = load(file)
    if not data:
        print(f"{RED}⚠️ Tidak ada data di {title}{RESET}")
        return
    print(f"{CYAN}=== {title} ==={RESET}")
    for i, (k,v) in enumerate(data.items(), 1):
        print(f"{YELLOW}{i}. Key:{RESET} {MAGENTA}{k}{RESET}")
        print(f"{GREEN}{v}{RESET}")
        print(f"{CYAN}{'-'*40}{RESET}")

def delete_data(file):
    data = load(file)
    if not data:
        print(f"{RED}⚠️ Tidak ada data untuk dihapus{RESET}")
        return
    view_data(file, "Data yang bisa dihapus")
    choice = input("Masukkan nomor key yg mau dihapus (pisah koma) atau ALL: ").strip()
    if choice.lower() == "all":
        progress_bar("Menghapus")
        save(file, {})
        print(f"{GREEN}Semua data berhasil dihapus{RESET}")
        return
    try:
        nums = [int(x)-1 for x in choice.split(",")]
        keys = list(data.keys())
        for n in nums:
            if 0 <= n < len(keys):
                del data[keys[n]]
        save(file, data)
        print(f"{GREEN}Data terhapus!{RESET}")
    except:
        print(f"{RED}Input salah{RESET}")

# ======== Menu + ========
def menu_plus():
    spinner("Membuka menu")
    while True:
        os.system("clear")
        print(f"{CYAN}=== 😎 CatBot Menu ==={RESET}")
        print(f"[1] Lihat data umum")
        print(f"[2] Lihat script")
        print(f"[3] Edit data umum (nano)")
        print(f"[4] Edit script (nano)")
        print(f"[5] Hapus data")
        print(f"[X] Kembali")
        choice = input("➡ Pilih: ").strip().lower()
        if choice == "1": view_data(DATA_GENERAL, "Data Umum")
        elif choice == "2": view_data(DATA_SCRIPT, "Script")
        elif choice == "3": os.system(f"nano {DATA_GENERAL}")
        elif choice == "4": os.system(f"nano {DATA_SCRIPT}")
        elif choice == "5":
            print(f"A) Hapus data umum\nB) Hapus script\nC) Batal")
            del_choice = input("➡ Pilih: ").strip().lower()
            if del_choice == "a": delete_data(DATA_GENERAL)
            elif del_choice == "b": delete_data(DATA_SCRIPT)
        elif choice == "x": break
        input(f"{CYAN}Tekan Enter untuk kembali...{RESET}")

# ======== Loop Percakapan ========
while True:
    show_chat()
    key = input(f"{YELLOW}😎 you: {RESET}").strip()
    if key.lower() == "x": break
    if key == "+":
        menu_plus()
        continue

    data_gen = load(DATA_GENERAL)
    data_scr = load(DATA_SCRIPT)

    if key in data_gen:
        spinner("Membalas")
        bot_reply = data_gen[key]
        chat_history.append((key, bot_reply))
        continue
    if key in data_scr:
        spinner("Membalas")
        bot_reply = data_scr[key]
        chat_history.append((key, bot_reply))
        continue

    # Pilihan jika jawaban belum ada
    print(f"{CYAN}A : Ajarin{RESET}")
    print(f"{CYAN}B : Script{RESET}")
    print(f"{RED}C : Batal{RESET}")
    pilihan = input(f"{YELLOW}Pilih: {RESET}").strip().lower()
    if pilihan == "a":
        add_general(key)
        chat_history.append((key, "Jawaban umum tersimpan!"))
    elif pilihan == "b":
        add_script(key)
        chat_history.append((key, "Script tersimpan!"))
    elif pilihan == "c":
        chat_history.append((key, "❌ Batal"))

