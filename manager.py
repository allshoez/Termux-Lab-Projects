#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import getpass
from colorama import Fore, Style, init

init(autoreset=True)

TRASH = os.path.expanduser("~/trash")
os.makedirs(TRASH, exist_ok=True)

# ===== Util =====
def pause():
    input(Fore.YELLOW + "\n⏎ Tekan ENTER untuk kembali..." + Style.RESET_ALL)

def clear():
    os.system("clear")

def try_open_with_editor(path):
    """Coba buka file dengan nano, kalau ga ada pakai less/cat."""
    try:
        subprocess.run(["nano", path])
    except FileNotFoundError:
        try:
            subprocess.run(["less", path])
        except FileNotFoundError:
            # fallback: print first lines
            try:
                with open(path, "r", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if i > 200: break
                        print(line.rstrip())
            except Exception as e:
                print(Fore.RED + f"⚠️ Tidak bisa membuka file: {e}" + Style.RESET_ALL)

# ===== List Folder =====
def list_folder(path):
    if not os.path.isdir(path):
        print(Fore.RED + f"[!] Folder {path} tidak ditemukan" + Style.RESET_ALL)
        return
    print(Fore.CYAN + f"\n📂 Isi folder: {path}" + Style.RESET_ALL)
    files = sorted(os.listdir(path))
    if not files:
        print(Fore.YELLOW + "[kosong]" + Style.RESET_ALL)
    else:
        for f in files:
            full = os.path.join(path, f)
            if os.path.isdir(full):
                print(Fore.BLUE + "📁 " + f + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "📄 " + f + Style.RESET_ALL)

# ===== Buat Folder / File =====
def create_folder(path):
    name = input("📂 Nama folder baru: ").strip()
    if name:
        os.makedirs(os.path.join(path, name), exist_ok=True)
        print(Fore.GREEN + f"[✔] Folder {name} dibuat!" + Style.RESET_ALL)

def create_file(path):
    name = input("📄 Nama file baru: ").strip()
    if name:
        open(os.path.join(path, name), "w").close()
        print(Fore.GREEN + f"[✔] File {name} dibuat!" + Style.RESET_ALL)

# ===== Rename =====
def rename_item(path):
    list_folder(path)
    old = input("✏️ Nama lama: ").strip()
    new = input("✏️ Nama baru: ").strip()
    oldp = os.path.join(path, old)
    newp = os.path.join(path, new)
    if os.path.exists(oldp):
        os.rename(oldp, newp)
        print(Fore.GREEN + f"[✔] {old} → {new}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[!] Tidak ditemukan" + Style.RESET_ALL)

# ===== Hapus / Trash =====
def delete_item(path, permanent=False):
    list_folder(path)
    target = input("🗑️ Nama file/folder: ").strip()
    full = os.path.join(path, target)
    if not os.path.exists(full):
        print(Fore.RED + "[!] Tidak ditemukan" + Style.RESET_ALL)
        return
    if permanent:
        if os.path.isdir(full):
            shutil.rmtree(full)
        else:
            os.remove(full)
        print(Fore.GREEN + "[✔] Dihapus permanen" + Style.RESET_ALL)
    else:
        dest = os.path.join(TRASH, f"{target}_{int(os.path.getmtime(full))}")
        shutil.move(full, dest)
        print(Fore.GREEN + "[✔] Dipindahkan ke trash" + Style.RESET_ALL)

# ===== Cari File Global Fleksibel =====
def cari_file(query, base_dir):
    hasil = []

    for root, _, files in os.walk(base_dir):
        for f in files:
            if query.lower() in f.lower():
                hasil.append(os.path.join(root, f))

    if hasil:
        print(Fore.CYAN + f"\n📂 Hasil pencarian untuk '{query}':" + Style.RESET_ALL)
        for i, path in enumerate(hasil, 1):
            print(Fore.YELLOW + f"{i:02d}. " + Fore.GREEN + path + Style.RESET_ALL)

        pilih = input(Fore.CYAN + "\nPilih nomor untuk buka file (kosong = batal): " + Style.RESET_ALL).strip()
        if pilih.isdigit():
            idx = int(pilih) - 1
            if 0 <= idx < len(hasil):
                target = hasil[idx]
                print(Fore.CYAN + f"\n➡️ Membuka: {target}" + Style.RESET_ALL)
                try_open_with_editor(target)
            else:
                print(Fore.RED + "Pilihan tidak valid." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "Batal." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\n❌ Tidak ditemukan file yang cocok dengan '{query}'." + Style.RESET_ALL)
    pause()

# ===== Kompres Folder ke zip (dengan opsi password) =====
def compress_folder_to_zip():
    print(Fore.CYAN + "\n📦 Kompres Folder ke ZIP" + Style.RESET_ALL)
    folder = input("Masukkan path folder yang akan dikompres: ").strip()
    if not folder or not os.path.isdir(folder):
        print(Fore.RED + "Folder tidak ditemukan." + Style.RESET_ALL)
        pause()
        return

    dest_dir = input("Simpan zip ke folder (default /sdcard): ").strip() or "/sdcard"
    os.makedirs(dest_dir, exist_ok=True)

    default_name = os.path.basename(os.path.abspath(folder)).replace(" ", "_")
    zip_name = input(f"Nama zip (default '{default_name}.zip'): ").strip() or f"{default_name}.zip"
    if not zip_name.lower().endswith(".zip"):
        zip_name += ".zip"

    set_pwd = input("Set password untuk zip? (y/N): ").strip().lower() == "y"
    password = None
    if set_pwd:
        show = input("Tampilkan saat mengetik password? (y/N): ").strip().lower() == "y"
        if show:
            pwd1 = input("Masukkan password: ")
            pwd2 = input("Ulangi password: ")
        else:
            pwd1 = getpass.getpass("Masukkan password (tersembunyi): ")
            pwd2 = getpass.getpass("Ulangi password: ")
        if pwd1 != pwd2:
            print(Fore.RED + "Password tidak cocok. Batal." + Style.RESET_ALL)
            pause()
            return
        password = pwd1

    out_path = os.path.join(dest_dir, zip_name)

    if password:
        zip_cmd = shutil.which("zip")
        if zip_cmd:
            print(Fore.CYAN + f"\nMembuat ZIP terenkripsi ke: {out_path}" + Style.RESET_ALL)
            try:
                subprocess.run([zip_cmd, "-r", "-P", password, out_path, "."], cwd=folder)
                print(Fore.GREEN + "[✔] Berhasil membuat zip terenkripsi." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[!] Gagal menjalankan zip: {e}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[!] zip command tidak ditemukan. Membuat zip tanpa password." + Style.RESET_ALL)
            try:
                shutil.make_archive(os.path.splitext(out_path)[0], 'zip', root_dir=folder)
                print(Fore.GREEN + "[✔] Berhasil membuat zip (tanpa password)." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[!] Gagal membuat zip: {e}" + Style.RESET_ALL)
    else:
        try:
            shutil.make_archive(os.path.splitext(out_path)[0], 'zip', root_dir=folder)
            print(Fore.GREEN + f"[✔] Berhasil membuat zip: {out_path}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Gagal membuat zip: {e}" + Style.RESET_ALL)
    pause()

# ===== Manager Area =====
def manager_area(path, name):
    while True:
        clear()
        print(Fore.CYAN + f"🖥️ === {name} ===" + Style.RESET_ALL)
        print("1. Lihat isi folder")
        print("2. Rename/Edit")
        print("3. Hapus permanen")
        print("4. Hapus ke trash")
        print("5. Buat folder baru")
        print("6. Buat file baru")
        print("7. Cari file global")
        print("8. Kompres folder -> zip")
        print("X. Kembali")
        opt = input("➡️ Pilih opsi: ").strip()
        if opt == "1": list_folder(path); pause()
        elif opt == "2": rename_item(path); pause()
        elif opt == "3": delete_item(path, True); pause()
        elif opt == "4": delete_item(path, False); pause()
        elif opt == "5": create_folder(path); pause()
        elif opt == "6": create_file(path); pause()
        elif opt == "7":
            query = input("Masukkan nama file/keyword: ").strip()
            if query: cari_file(query, path)
        elif opt == "8": compress_folder_to_zip()
        elif opt.lower() == "x": break

# ===== Main Menu =====
def main():
    while True:
        clear()
        print(Fore.MAGENTA + "🗂️ === TERMUX MANAGER PRO STYLE (Python) ===" + Style.RESET_ALL)
        print("1. Kelola Home Termux (~)")
        print("2. Kelola SDCard (/sdcard)")
        print("X. Keluar")
        opt = input("➡️ Pilih menu: ").strip()
        if opt == "1": manager_area(os.path.expanduser("~"), "HOME TERMUX (~)")
        elif opt == "2": manager_area("/sdcard", "STORAGE HP (/sdcard)")
        elif opt.lower() == "x":
            print(Fore.GREEN + "✔ Terima kasih sudah menggunakan Python Manager Pro!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()