#!/data/data/com.termux/files/usr/bin/env python3
import os
import shutil
import time
from colorama import Fore, Style, init
init(autoreset=True)

TRASH_DIR = os.path.expanduser("~/trash")
os.makedirs(TRASH_DIR, exist_ok=True)

# ===== Utils =====
def clear():
    os.system("clear")

def pause():
    input(Fore.YELLOW + "\nTekan ENTER untuk kembali..." + Style.RESET_ALL)

# ===== Folder Listing =====
def list_folder(path):
    if not os.path.exists(path):
        print(Fore.RED + f"[!] Folder {path} tidak ditemukan!")
        return
    print(Fore.CYAN + f"\n📂 Isi folder: {path}\n")
    for f in os.listdir(path):
        full_path = os.path.join(path, f)
        if os.path.isdir(full_path):
            print(Fore.YELLOW + f"[DIR] {f}")
        else:
            print(Fore.GREEN + f"      {f}")

def list_folder_recursive(base_path):
    if not os.path.exists(base_path):
        print(Fore.RED + f"[!] Folder {base_path} tidak ditemukan!")
        return
    print(Fore.CYAN + f"\n📂 Isi folder: {base_path}\n")
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = '   ' * level
        print(Fore.YELLOW + f"{indent}[DIR] {os.path.basename(root)}")
        subindent = '   ' * (level + 1)
        for f in files:
            print(Fore.GREEN + f"{subindent}{f}")

# ===== Folder Operations =====
def create_folder(base_path):
    name = input(Fore.CYAN + "Nama folder baru: ").strip()
    if not name:
        print(Fore.RED + "[!] Nama folder tidak boleh kosong!"); return
    full_path = os.path.join(base_path, name)
    if os.path.exists(full_path):
        print(Fore.RED + "[!] Folder sudah ada!"); return
    os.makedirs(full_path)
    print(Fore.GREEN + f"[✔] Folder '{name}' berhasil dibuat di {base_path}")

def rename_folder(base_path):
    list_folder(base_path)
    old_name = input(Fore.CYAN + "Masukkan nama folder/file lama: ").strip()
    old_path = os.path.join(base_path, old_name)
    if not os.path.exists(old_path):
        print(Fore.RED + "[!] Folder/file tidak ditemukan!"); return
    new_name = input(Fore.CYAN + "Masukkan nama baru: ").strip()
    new_path = os.path.join(base_path, new_name)
    if os.path.exists(new_path):
        print(Fore.RED + "[!] Nama baru sudah ada!"); return
    os.rename(old_path, new_path)
    print(Fore.GREEN + "[✔] Berhasil diubah nama!")

def delete_folder(base_path):
    list_folder(base_path)
    target = input(Fore.CYAN + "Masukkan nama folder/file yang akan dihapus: ").strip()
    full_path = os.path.join(base_path, target)
    if not os.path.exists(full_path):
        print(Fore.RED + "[!] Folder/file tidak ditemukan!"); return
    confirm = input(Fore.RED + f"Yakin hapus '{target}'? (y/n): ").lower()
    if confirm != "y":
        print(Fore.YELLOW + "Batal menghapus."); return
    dest = os.path.join(TRASH_DIR, f"{target}_{int(time.time())}")
    shutil.move(full_path, dest)
    print(Fore.GREEN + f"[✔] '{target}' dipindahkan ke trash: {dest}")

def restore_folder():
    if not os.path.exists(TRASH_DIR) or not os.listdir(TRASH_DIR):
        print(Fore.YELLOW + "[!] Trash kosong."); return
    items = os.listdir(TRASH_DIR)
    print(Fore.CYAN + "\n📂 Daftar item di trash:")
    for i, f in enumerate(items, 1):
        print(Fore.GREEN + f"[{i}] {f}")
    pilih = input(Fore.CYAN + "Masukkan nomor item untuk restore: ").strip()
    if not pilih.isdigit() or int(pilih)<1 or int(pilih)>len(items):
        print(Fore.RED + "Input tidak valid."); return
    item = items[int(pilih)-1]
    src = os.path.join(TRASH_DIR, item)
    dst_name = "_".join(item.split("_")[:-1])
    dst = os.path.join(os.path.expanduser("~"), dst_name)
    if os.path.exists(dst):
        overwrite = input(Fore.RED + f"Folder '{dst_name}' sudah ada di home, timpa? (y/n): ").lower()
        if overwrite != "y":
            print(Fore.YELLOW + "Batal restore."); return
        shutil.rmtree(dst)
    shutil.move(src, dst)
    print(Fore.GREEN + f"[✔] '{dst_name}' berhasil di-restore ke home Termux!")

# ===== Folder Explorer =====
def explore_folder(base_path):
    while True:
        clear()
        print(Fore.BLUE + f"\n=== EXPLORER: {base_path} ===")
        print("1. Lihat isi folder (rekursif)")
        print("2. Rename/Edit folder/file")
        print("3. Hapus folder/file")
        print("X. Kembali")
        pilih = input(Fore.CYAN + "Pilih opsi: ").upper()
        if pilih == "1":
            list_folder_recursive(base_path); pause()
        elif pilih == "2":
            rename_folder(base_path); pause()
        elif pilih == "3":
            delete_folder(base_path); pause()
        elif pilih == "X":
            break

# ===== Home Manager =====
def home_manager():
    path = os.path.expanduser("~")
    while True:
        clear()
        print(Fore.BLUE + "\n=== HOME TERMUX (~) ===")
        print("A. Lihat isi folder")
        print("B. Rename/Edit folder")
        print("C. Hapus folder")
        print("D. Buat folder baru")
        print("E. Restore folder dari trash")
        print("X. Kembali")
        pilih = input(Fore.CYAN + "Pilih opsi: ").upper()
        if pilih == "A":
            list_folder(path)
            sel = input(Fore.CYAN + "Masukkan nama folder untuk eksplor: ").strip()
            full_path = os.path.join(path, sel)
            if os.path.exists(full_path) and os.path.isdir(full_path):
                explore_folder(full_path)
            else:
                print(Fore.RED + "[!] Folder tidak ditemukan!"); pause()
        elif pilih == "B":
            rename_folder(path); pause()
        elif pilih == "C":
            delete_folder(path); pause()
        elif pilih == "D":
            create_folder(path); pause()
        elif pilih == "E":
            restore_folder(); pause()
        elif pilih == "X":
            break

# ===== SDCard Manager =====
def sdcard_manager():
    path = "/sdcard"
    while True:
        clear()
        print(Fore.MAGENTA + "\n=== STORAGE HP (/sdcard) ===")
        print("A. Lihat isi folder")
        print("B. Salin folder ke Home Termux")
        print("C. Rename/Edit folder/file di SDCard")
        print("D. Buat folder baru di SDCard")
        print("X. Kembali")
        pilih = input(Fore.CYAN + "Pilih opsi: ").upper()
        if pilih == "A":
            list_folder(path)
            sel = input(Fore.CYAN + "Masukkan nama folder untuk eksplor: ").strip()
            full_path = os.path.join(path, sel)
            if os.path.exists(full_path) and os.path.isdir(full_path):
                explore_folder(full_path)
            else:
                print(Fore.RED + "[!] Folder tidak ditemukan!"); pause()
        elif pilih == "B":
            list_folder(path)
            folder = input(Fore.CYAN + "Masukkan nama folder untuk disalin: ").strip()
            src = os.path.join(path, folder)
            dst = os.path.join(os.path.expanduser("~"), folder)
            if not os.path.exists(src) or not os.path.isdir(src):
                print(Fore.RED + "[!] Folder tidak ditemukan!"); pause(); continue
            if os.path.exists(dst):
                overwrite = input(Fore.RED + "Folder sudah ada di home, timpa? (y/n): ").lower()
                if overwrite != "y": continue
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(Fore.GREEN + f"[✔] Folder '{folder}' berhasil disalin ke Home Termux!"); pause()
        elif pilih == "C":
            rename_folder(path); pause()
        elif pilih == "D":
            create_folder(path); pause()
        elif pilih == "X":
            break

# ===== Main Menu =====
def main():
    while True:
        clear()
        print(Fore.BLUE + "\n=== MANAGER TERMUX ===")
        print("1. Kelola Home Termux (~)")
        print("2. Kelola SDCard (/sdcard)")
        print("X. Keluar")
        pilih = input(Fore.CYAN + "Pilih menu: ").upper()
        if pilih == "1":
            home_manager()
        elif pilih == "2":
            sdcard_manager()
        elif pilih == "X":
            print(Fore.GREEN + "Terima kasih sudah menggunakan Manager Termux!")
            break
        else:
            print(Fore.RED + "Input tidak valid!"); pause()

if __name__ == "__main__":
    main()
