import json, os
from colorama import Fore, Style, init

init(autoreset=True)

DATA_FILE = "data.json"

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            raw_data = json.load(f)
            # Normalisasi key: strip + lowercase
            data = {k.strip().lower(): v for k, v in raw_data.items()}
        except:
            data = {}
else:
    data = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def input_multiline(prompt):
    print(prompt + " (Enter kosong = selesai / batal):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

# Header menu
print(Fore.CYAN + "=== CatBot Python ===")
print(Fore.YELLOW + "  L = Lihat data")
print(Fore.YELLOW + "  E = Edit data")
print(Fore.YELLOW + "  X = Exit\n")

while True:
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
        continue

    elif tanya_lc == "e":
        key = input(Fore.YELLOW + "Pertanyaan yang mau diedit: " + Style.RESET_ALL).strip().lower()
        if key in data:
            print(Fore.YELLOW + f"Jawaban lama:\n{data[key]}")
            baru = input_multiline(Fore.GREEN + "Jawaban baru")
            if baru:
                data[key] = baru
                save_data()
                print(Fore.CYAN + "✔️ Jawaban berhasil diupdate.")
            else:
                print(Fore.RED + "❌ Edit dibatalkan.")
        else:
            print(Fore.RED + "❌ Pertanyaan itu belum ada di data.")
        continue

    # Flexible substring match
    found = False
    for key, val in data.items():
        if key in tanya_lc or tanya_lc in key:
            print(Fore.CYAN + "Bot  :" + Style.RESET_ALL + "\n" + val)
            found = True
            break

    if not found:
        # Belum ada jawaban
        print(Fore.RED + "Bot  : (Belum ada jawaban)")
        jawaban = input_multiline(Fore.GREEN + "Isi jawaban")
        if jawaban:
            data[tanya_lc] = jawaban
            save_data()
            print(Fore.CYAN + "✔️ Jawaban disimpan.")
        else:
            print(Fore.YELLOW + "↩️  Batal, tidak disimpan.")