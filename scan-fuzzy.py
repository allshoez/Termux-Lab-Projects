
import os
from fuzzywuzzy import fuzz
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

search_folder = "/sdcard"  # folder utama HP
THREADS = 8  # jumlah thread, bisa disesuaikan dengan HP

# Fungsi scan semua file
def scan_files(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# Fungsi untuk menilai warna berdasarkan kemiripan
def similarity_color(ratio):
    if ratio > 90:
        return Fore.GREEN
    elif ratio >= 80:
        return Fore.YELLOW
    else:
        return Fore.RED

# Fungsi untuk menghitung kemiripan satu file
def process_file(file_path, keyword):
    ratio_name = fuzz.partial_ratio(keyword.lower(), os.path.basename(file_path).lower())
    ratio_content = 0
    try:
        if file_path.endswith((".txt", ".py", ".log", ".csv", ".json")):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                ratio_content = fuzz.partial_ratio(keyword.lower(), content.lower())
    except Exception:
        pass
    ratio = max(ratio_name, ratio_content)
    if ratio > 70:
        return (file_path, ratio)
    return None

# Fungsi fuzzy search dengan multithreading
def fuzzy_search():
    keyword = input(Fore.CYAN + "Masukkan keyword untuk fuzzy search: " + Style.RESET_ALL)
    all_files = scan_files(search_folder)
    matches = []

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(lambda f: process_file(f, keyword), all_files)
        for r in results:
            if r:
                matches.append(r)

    matches.sort(key=lambda x: x[1], reverse=True)

    if matches:
        print(Fore.MAGENTA + f"\nDitemukan {len(matches)} file yang cocok:\n" + Style.RESET_ALL)
        for i, (file_path, ratio) in enumerate(matches):
            color = similarity_color(ratio)
            print(Fore.YELLOW + f"{i+1}. " + color + f"{file_path} " + Fore.CYAN + f"({ratio}%)" + Style.RESET_ALL)

        pilih = input(Fore.CYAN + "\nPilih nomor file yang ingin dibuka (pisahkan koma untuk banyak file, enter untuk batal): " + Style.RESET_ALL)
        if pilih:
            indices = [int(x.strip())-1 for x in pilih.split(",") if x.strip().isdigit()]
            for idx in indices:
                if 0 <= idx < len(matches):
                    file_to_open = matches[idx][0]
                    print(Fore.GREEN + f"Membuka file: {file_to_open}" + Style.RESET_ALL)
                    os.system(f'termux-open "{file_to_open}"')
    else:
        print(Fore.RED + "Tidak ada file yang cocok ditemukan." + Style.RESET_ALL)

# --- Menu utama ---
while True:
    print(Fore.BLUE + "\n=== FUZZY SCAN TERMUX STYLE MULTITHREAD ===" + Style.RESET_ALL)
    print(Fore.YELLOW + "[C] Cari File")
    print(Fore.RED + "[X] Keluar" + Style.RESET_ALL)
    choice = input(Fore.CYAN + "Pilihan: " + Style.RESET_ALL).upper()

    if choice == "C":
        fuzzy_search()
    elif choice == "X":
        print(Fore.GREEN + "Keluar program." + Style.RESET_ALL)
        break
    else:
        print(Fore.RED + "Pilihan tidak valid, coba lagi." + Style.RESET_ALL)


