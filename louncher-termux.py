

import os
import shutil
import subprocess
import json
import time
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_FILE = "termux_dashboard.json"
BACKUP_DIR = "/sdcard/backup_projects"

# ===== Utils =====
def clear():
    os.system("clear")

def pause():
    input(Fore.YELLOW + "\nTekan ENTER untuk kembali..." + Style.RESET_ALL)

def pretty_path(p):
    try:
        return os.path.abspath(os.path.expanduser(p))
    except Exception:
        return p

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "projects" in data and isinstance(data["projects"], list):
                    return data
        except json.JSONDecodeError:
            pass
    return {"projects": []}

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

# ===== Spinner =====
class Spinner:
    def __init__(self, text="Menjalankan..."):
        self.text = text
        self.frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

    def start(self):
        for i in range(10):
            print(Fore.MAGENTA + f"\r{self.frames[i%len(self.frames)]} {self.text}", end="", flush=True)
            time.sleep(0.08)
        print("\r" + " "*40 + "\r", end="")

# ===== Home Termux Menu =====
def list_files(path):
    if not os.path.exists(path):
        print(Fore.RED + f"[!] Folder {path} tidak ditemukan!")
        return
    print(Fore.CYAN + f"📂 Isi folder: {path}\n")
    for f in os.listdir(path):
        full_path = os.path.join(path, f)
        if os.path.isdir(full_path):
            print(Fore.YELLOW + f"[DIR] {f}")
        else:
            print(Fore.GREEN + f"      {f}")

def rename_item(path):
    old_name = input(Fore.CYAN + "Masukkan nama file/folder lama: ").strip()
    new_name = input(Fore.CYAN + "Masukkan nama baru: ").strip()
    try:
        os.rename(os.path.join(path, old_name), os.path.join(path, new_name))
        print(Fore.GREEN + "[✔] Berhasil rename!")
    except Exception as e:
        print(Fore.RED + f"[!] Gagal rename: {e}")

def delete_item(path):
    target = input(Fore.CYAN + "Masukkan nama file/folder yang akan dihapus: ").strip()
    full_path = os.path.join(path, target)
    if not os.path.exists(full_path):
        print(Fore.RED + "[!] File/folder tidak ditemukan!")
        return
    confirm = input(Fore.RED + f"Yakin hapus {target}? (y/n): ").lower()
    if confirm == "y":
        try:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            print(Fore.GREEN + "[✔] Berhasil dihapus!")
        except Exception as e:
            print(Fore.RED + f"[!] Gagal hapus: {e}")

def menu_home():
    path = os.path.expanduser("~")
    while True:
        clear()
        print(Fore.BLUE + "=== HOME TERMUX ===")
        print("1. Lihat isi folder")
        print("2. Rename file/folder")
        print("3. Hapus file/folder")
        print("4. Kembali ke menu utama")
        pilih = input(Fore.CYAN + "Pilih: ").strip()
        if pilih == "1":
            list_files(path); pause()
        elif pilih == "2":
            rename_item(path); pause()
        elif pilih == "3":
            delete_item(path); pause()
        elif pilih == "4":
            break

def menu_sdcard():
    path = "/sdcard"
    while True:
        clear()
        print(Fore.MAGENTA + "=== STORAGE HP (/sdcard) ===")
        print("1. Lihat isi folder")
        print("2. Rename file/folder")
        print("3. Hapus file/folder")
        print("4. Kembali ke menu utama")
        pilih = input(Fore.CYAN + "Pilih: ").strip()
        if pilih == "1":
            list_files(path); pause()
        elif pilih == "2":
            rename_item(path); pause()
        elif pilih == "3":
            delete_item(path); pause()
        elif pilih == "4":
            break

def copy_project():
    sd_path = "/sdcard"
    home_path = os.path.expanduser("~")
    list_files(sd_path)
    folder = input(Fore.CYAN + "Masukkan nama folder/project dari sdcard: ").strip()
    src = os.path.join(sd_path, folder)
    dst = os.path.join(home_path, folder)
    if not os.path.exists(src):
        print(Fore.RED + "[!] Folder tidak ditemukan di sdcard!"); return
    if os.path.exists(dst):
        overwrite = input(Fore.RED + "Folder sudah ada di home, timpa? (y/n): ").lower()
        if overwrite != "y": return
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(Fore.GREEN + "[✔] Project berhasil dicopy ke home Termux!")

# ===== Backup & Restore =====
def backup_project(path, name):
    if not os.path.exists(path):
        print(Fore.RED + f"[!] Folder {path} tidak ada, backup gagal!")
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    dst = os.path.join(BACKUP_DIR, name)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(path, dst)
    print(Fore.GREEN + f"[✔] Project '{name}' berhasil dibackup ke SDCard!")

def restore_project():
    if not os.path.exists(BACKUP_DIR):
        print(Fore.RED + "[!] Tidak ada backup di SDCard."); return
    print(Fore.CYAN + "📂 Daftar project backup:")
    for f in os.listdir(BACKUP_DIR):
        print(f"- {f}")
    name = input(Fore.CYAN + "Masukkan nama project yang mau di-restore: ").strip()
    src = os.path.join(BACKUP_DIR, name)
    dst = os.path.expanduser(f"~/{name}")
    if not os.path.exists(src):
        print(Fore.RED + "[!] Project tidak ditemukan di backup!"); return
    if os.path.exists(dst):
        overwrite = input(Fore.RED + "Folder sudah ada di home, timpa? (y/n): ").lower()
        if overwrite != "y": return
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(Fore.GREEN + f"[✔] Project '{name}' berhasil di-restore ke home Termux!")

# ===== Termux Dashboard Pro =====
def list_projects(cfg):
    print(Fore.BLUE + "=== DAFTAR PROJECT ===")
    if not cfg["projects"]:
        print(Fore.YELLOW + "Belum ada project. Tambah dulu via [A]."); return
    for i, p in enumerate(cfg["projects"], start=1):
        print(Fore.GREEN + f"[{i}] " + Fore.WHITE + p["name"])
        print(Fore.CYAN  + "   📁 " + Fore.WHITE + pretty_path(p.get("path","")))
        print(Fore.CYAN  + "   ▶  " + Fore.MAGENTA + p.get("command",""))

def add_project(cfg):
    print(Fore.BLUE + "=== TAMBAH PROJECT ===")
    name = input(Fore.CYAN + "Nama project: ").strip()
    path = input(Fore.CYAN + "Path folder: ").strip()
    cmd  = input(Fore.CYAN + "Command jalankan: ").strip()
    if not name or not cmd:
        print(Fore.RED + "Nama & command wajib diisi."); return
    cfg["projects"].append({"name": name, "path": path, "command": cmd})
    save_config(cfg)
    backup_project(path, name)
    print(Fore.GREEN + f"✅ Project '{name}' ditambahkan & dibackup!")

def run_project(cfg, index):
    proj = cfg["projects"][index]
    path = proj.get("path","")
    cmd  = proj.get("command","")
    if path: os.chdir(os.path.expanduser(path))
    confirm = input(Fore.YELLOW + f"Jalankan project '{proj['name']}'? (y/n): ").lower()
    if confirm != "y": return
    spinner = Spinner(text=f"Jalanin '{proj['name']}'")
    spinner.start()
    subprocess.run(cmd, shell=True)
    print(Fore.GREEN + "✅ Selesai!")

def tools_menu():
    while True:
        clear()
        print(Fore.MAGENTA + "=== TOOLS / INSTALLER ===")
        print("1  - Install Flask")
        print("2  - Install Node.js + Express")
        print("3  - Install Termcolor")
        print("4  - Install Termux-style")
        print("5  - Ganti Bahasa (ID/EN)")
        print("6  - Install Git")
        print("7  - Install Python3 + pip")
        print("8  - Install wget & curl")
        print("9  - Install unzip & zip")
        print("10 - Install nano & vim")
        print("11 - Scan IP Wi-Fi")
        print("12 - Text ke Suara (TTS)")
        print("13 - Kunci Folder")
        print("14 - Port Scanner")
        print("15 - Speedtest Internet")
        print("16 - Check Storage Info")
        print("17 - None")
        print("18 - None")
        print("19 - None")
        print("20 - None")
        print("0  - Kembali")
        pilih = input(Fore.CYAN + "Pilih tool: ").strip().upper()
        if pilih == "O": break
        elif pilih in [str(i) for i in range(1,21)]:
            print(Fore.YELLOW + f"Pilihan {pilih}, konfirmasi sebelum dijalankan")
            konfirm = input(Fore.YELLOW + "Yakin mau jalankan? (y/n): ").lower()
            if konfirm != "y": continue
            print(Fore.GREEN + f"Menjalankan tool nomor {pilih}... (simulasi)")
            pause()
        else:
            print(Fore.RED + "Input tidak valid."); pause()

# ===== Main Menu =====
def main():
    cfg = load_config()
    while True:
        clear()
        print(Fore.BLUE + "=== LAUNCHER TERMUX ===")
        print("T. Home Termux (~)")
        print("S. Storage HP (/sdcard)")
        print("C. Copy Project dari SDCard ke Home Termux")
        print("D. Tools / Installer")
        print("L. List Projects / Dashboard Pro")
        print("A. Tambah Project")
        print("R. Restore Project dari Backup SDCard")
        print("X. Keluar")
        pilih = input(Fore.CYAN + "Pilih menu: ").strip().upper()
        if pilih == "T": menu_home()
        elif pilih == "S": menu_sdcard()
        elif pilih == "C": copy_project(); pause()
        elif pilih == "D": tools_menu()
        elif pilih == "L": list_projects(cfg); pause()
        elif pilih == "A": add_project(cfg); pause()
        elif pilih == "R": restore_project(); pause()
        elif pilih == "X":
            konfirm = input(Fore.RED + "Yakin mau keluar? (y/n): ").lower()
            if konfirm == "y":
                clear()
                print(Fore.GREEN + "Terima kasih sudah menggunakan Launcher Termux!")
                time.sleep(1)
                os._exit(0)
        else:
            print(Fore.RED + "Input tidak valid."); pause()

if __name__ == "__main__":
    main()
