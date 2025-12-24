import json
import os
from colorama import Fore, Style, init                                        init(autoreset=True)

FILE_HARIAN = "data.json"
FILE_TAHUNAN = "penjualan.json"        
# --- Utility ---
def parse_angka(s):
    """Convert string dengan titik ribuan ke float, aman dari error."""
    if not s:
        return 0.0
    s_clean = s.replace(".", "").replace(",", ".")
    try:
        return float(s_clean)
    except ValueError:
        return 0.0

def load_file(file_path):                  if not os.path.exists(file_path):          return []
    with open(file_path, "r") as f:
        try:                                       data = json.load(f)                    if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):                                                  data = []
            clean_data = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                nama = item.get("nama", "-")
                harga = item.get("harga", "0")
                laba  = item.get("laba", "0")                                                 clean_data.append({"nama": nama, "harga": harga, "laba": laba})
            return clean_data
        except json.JSONDecodeError:
            return []

def save_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# --- Tambah data ---
def tambah_data(file_path, tipe_data):
    print(Fore.CYAN + f"\n➕ Tambah Data {tipe_data}\n" + Style.RESET_ALL)
    nama = input(Fore.YELLOW + "Nama barang: " + Style.RESET_ALL).strip()
    harga = input(Fore.YELLOW + "Harga : " + Style.RESET_ALL).strip()
    laba = input(Fore.YELLOW + "Laba : " + Style.RESET_ALL).strip()

    if not nama:
        print(Fore.RED + "❌ Nama wajib diisi!\n")
        return
    if not harga:
        harga = "0"
    if not laba:
        laba = "0"

    data = load_file(file_path)
    data.append({"nama": nama, "harga": harga, "laba": laba})
    save_file(file_path, data)
    print(Fore.GREEN + "✅ Data berhasil ditambahkan!\n")

# --- Lihat data ---
def lihat_data(file_path, tipe_data):      data = load_file(file_path)
    if not data:                               print(Fore.RED + f"📭 Tidak ada data {tipe_data}.\n")
        return

    print(Fore.MAGENTA + f"\n=== Daftar Catatan {tipe_data} ===" + Style.RESET_ALL)
    total_harga = 0.0
    total_laba = 0.0

    for i, item in enumerate(data, 1):
        nama = item.get("nama", "-")
        harga_str = item.get("harga", "0")                                            laba_str  = item.get("laba", "0")

        harga_val = parse_angka(harga_str)
        laba_val  = parse_angka(laba_str)

        total_harga += harga_val
        total_laba  += laba_val

        print(Fore.CYAN + f"\n{i}.")
        print(Fore.YELLOW + f"Nama  : {nama}")                                        print(Fore.YELLOW + f"Harga : {harga_str}")
        print(Fore.GREEN + f"Laba  : {laba_str}" + Style.RESET_ALL)
                                           print(Fore.MAGENTA + "\n============================")
    print(Fore.YELLOW + f"Total Harga: {int(total_harga):,}")                     print(Fore.GREEN + f"Total Laba : {int(total_laba):,}\n" + Style.RESET_ALL)
                                       # --- Edit / Hapus data ---
def edit_data(file_path, tipe_data):
    data = load_file(file_path)
    if not data:
        print(Fore.RED + f"📭 Tidak ada data {tipe_data} untuk diedit.\n")
        return

    lihat_data(file_path, tipe_data)
    try:
        idx = int(input(Fore.YELLOW + "Masukkan nomor data yang ingin diedit: " + Style.RESET_ALL)) - 1
        if idx < 0 or idx >= len(data):            print(Fore.RED + "❌ Nomor tidak valid!\n")                                   return
    except ValueError:                         print(Fore.RED + "❌ Masukkan angka yang benar!\n")
        return
                                           item = data[idx]
    nama = input(Fore.YELLOW + f"Nama lama: {item['nama']}\nNama baru (kosongkan jika tidak diubah): " + Style.RESET_ALL) or item['nama']
    harga = input(Fore.YELLOW + f"Harga lama: {item['harga']}\nHarga baru (kosongkan jika tidak diubah): " + Style.RESET_ALL) or item['harga']                  laba  = input(Fore.YELLOW + f"Laba lama: {item['laba']}\nLaba baru (kosongkan jika tidak diubah): " + Style.RESET_ALL) or item['laba']

    data[idx] = {"nama": nama, "harga": harga, "laba": laba}
    save_file(file_path, data)
    print(Fore.GREEN + "✅ Data berhasil diperbarui!\n")
                                       def hapus_data(file_path, tipe_data):
    data = load_file(file_path)
    if not data:
        print(Fore.RED + f"📭 Tidak ada data {tipe_data} untuk dihapus.\n")
        return                         
    lihat_data(file_path, tipe_data)
    try:                                       idx = int(input(Fore.YELLOW + "Masukkan nomor data yang ingin dihapus: " + Style.RESET_ALL)) - 1                     if idx < 0 or idx >= len(data):
            print(Fore.RED + "❌ Nomor tidak valid!\n")
            return                         except ValueError:
        print(Fore.RED + "❌ Masukkan angka yang benar!\n")
        return                         
    data.pop(idx)
    save_file(file_path, data)
    print(Fore.GREEN + "✅ Data berhasil dihapus!\n")
                                       # --- Menu ---
def menu():
    while True:
        print(Fore.CYAN + "\n=== CATATAN HARGA TERMUX ===" + Style.RESET_ALL)
        print(Fore.YELLOW + "1. Tambah Catatan Harian")                               print(Fore.YELLOW + "2. Tambah Catatan Tahunan")
        print(Fore.YELLOW + "3. Lihat Data Harian")
        print(Fore.YELLOW + "4. Lihat Data Tahunan")
        print(Fore.YELLOW + "5. Edit Data Harian")
        print(Fore.YELLOW + "6. Edit Data Tahunan")
        print(Fore.YELLOW + "7. Hapus Data Harian")                                   print(Fore.YELLOW + "8. Hapus Data Tahunan")                                  print(Fore.YELLOW + "x. Keluar")                                              pilihan = input(Fore.CYAN + "Pilih menu: " + Style.RESET_ALL)
                                               if pilihan == "1":
            tambah_data(FILE_HARIAN, "Harian")                                        elif pilihan == "2":
            tambah_data(FILE_TAHUNAN, "Tahunan")
        elif pilihan == "3":                       lihat_data(FILE_HARIAN, "Harian")
        elif pilihan == "4":
            lihat_data(FILE_TAHUNAN, "Tahunan")
        elif pilihan == "5":
            edit_data(FILE_HARIAN, "Harian")
        elif pilihan == "6":
            edit_data(FILE_TAHUNAN, "Tahunan")
        elif pilihan == "7":                       hapus_data(FILE_HARIAN, "Harian")
        elif pilihan == "8":                       hapus_data(FILE_TAHUNAN, "Tahunan")                                       elif pilihan == "x":
            print(Fore.LIGHTBLACK_EX + "👋 Keluar dari program..." + Style.RESET_ALL)
            break                              else:
            print(Fore.RED + "❌ Pilihan tidak valid!\n")

if __name__ == "__main__":
    menu()