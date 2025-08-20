

import json
import os
from collections import Counter

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

GREEN = '\033[92m'
YELLOW = '\033[93m'
WHITE = '\033[97m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
RESET = '\033[0m'

def pilih_bulan():
    bulan = input(CYAN + "Bulan-tahun (ex: januari-2025): " + RESET).lower()
    file_path = os.path.join(DATA_DIR, f"{bulan}.json")
    trash_path = os.path.join(DATA_DIR, f"trash_{bulan}.json")
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
    if not os.path.exists(trash_path):
        with open(trash_path, "w") as f:
            json.dump([], f)
    return file_path, trash_path

def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data_list):
    with open(file_path, "w") as f:
        json.dump(data_list, f, indent=4)

def format_rupiah(value):
    if isinstance(value, str):
        value = value.replace(".", "").replace(",", "")
        if value.isdigit():
            value = int(value)
        else:
            return value
    if value < 1000:
        value *= 1000
    return f"{value:,}".replace(",", ".")

def tampilkan_item(item, idx=None):
    if idx is not None:
        print(MAGENTA + f"[{idx}] " + RESET, end="")
    print(GREEN + f"Nama   : {item['nama']}" + RESET)
    print("--------")
    print(YELLOW + f"Harga  : {format_rupiah(item['harga'])}" + RESET)
    print("--------")
    print(WHITE + f"Laba   : {format_rupiah(item['laba'])}" + RESET)
    print("--------")

def tambah_data(data_list):
    nama = input(GREEN + "Nama  : " + RESET)
    if nama.strip() == "":
        print(RED + "Nama tidak boleh kosong!" + RESET)
        return
    try:
        harga = input(YELLOW + "Harga : " + RESET)
        laba = input(WHITE + "Laba  : " + RESET)
        harga = int(harga.replace(".", "")) if "." in harga else int(harga)
        laba = int(laba.replace(".", "")) if "." in laba else int(laba)
    except ValueError:
        print(RED + "Harga/Laba harus angka!" + RESET)
        return
    data_list.append({"nama": nama, "harga": harga, "laba": laba})
    print(CYAN + f"Data '{nama}' berhasil ditambahkan.\n" + RESET)

def cek_total(data_list):
    total_harga = sum(int(str(d['harga']).replace(".", "")) for d in data_list)
    total_laba = sum(int(str(d['laba']).replace(".", "")) for d in data_list)
    print(MAGENTA + f"Total Harga : {format_rupiah(total_harga)}")
    print(MAGENTA + f"Total Laba  : {format_rupiah(total_laba)}" + RESET)

def cari_terbanyak(data_list):
    if not data_list:
        print(RED + "Data kosong." + RESET)
        return
    counter = Counter([d['nama'] for d in data_list])
    urutan = counter.most_common()
    print(CYAN + "\n=== Data Terbanyak ===" + RESET)
    for i, (nama, jumlah) in enumerate(urutan, 1):
        total = sum(d['harga'] for d in data_list if d['nama'] == nama)
        print(f"{i}. {nama}")
        print(f"Jumlahnya : {jumlah} pcs")
        print(f"Total     : {format_rupiah(total)}\n")

def edit_data(data_list):
    if not data_list:
        print(RED + "Data kosong." + RESET)
        return
    for i, item in enumerate(data_list, 1):
        tampilkan_item(item, i)
    try:
        idx = int(input(CYAN + "Pilih nomor yang mau diedit: " + RESET)) - 1
        if idx < 0 or idx >= len(data_list):
            print(RED + "Nomor tidak valid." + RESET)
            return
        item = data_list[idx]
        print(YELLOW + f"Edit data '{item['nama']}' (biarkan kosong jika tidak diubah)" + RESET)
        nama = input(f"Nama [{item['nama']}]: ").strip() or item['nama']
        harga_input = input(f"Harga [{item['harga']}]: ").strip()
        laba_input = input(f"Laba [{item['laba']}]: ").strip()
        harga = int(harga_input) if harga_input else item['harga']
        laba = int(laba_input) if laba_input else item['laba']
        data_list[idx] = {"nama": nama, "harga": harga, "laba": laba}
        print(GREEN + "Data berhasil diedit." + RESET)
    except ValueError:
        print(RED + "Input tidak valid." + RESET)

def hapus_data(data_list, trash_list):
    if not data_list:
        print(RED + "Data kosong." + RESET)
        return
    for i, item in enumerate(data_list, 1):
        tampilkan_item(item, i)
    try:
        idx = int(input(CYAN + "Pilih nomor yang mau dihapus: " + RESET)) - 1
        if idx < 0 or idx >= len(data_list):
            print(RED + "Nomor tidak valid." + RESET)
            return
        trash_list.append(data_list.pop(idx))
        print(RED + "Data berhasil dipindahkan ke tempat sampah." + RESET)
    except ValueError:
        print(RED + "Input tidak valid." + RESET)

def restore_data(data_list, trash_list):
    if not trash_list:
        print(RED + "Tempat sampah kosong." + RESET)
        return
    for i, item in enumerate(trash_list, 1):
        tampilkan_item(item, i)
    try:
        idx = int(input(CYAN + "Pilih nomor yang mau direstore: " + RESET)) - 1
        if idx < 0 or idx >= len(trash_list):
            print(RED + "Nomor tidak valid." + RESET)
            return
        data_list.append(trash_list.pop(idx))
        print(GREEN + "Data berhasil direstore." + RESET)
    except ValueError:
        print(RED + "Input tidak valid." + RESET)

def main():
    file_path, trash_path = pilih_bulan()
    data_list = load_data(file_path)
    trash_list = load_data(trash_path)

    while True:
        print(CYAN + "\n=== MENU TERMUX STYLE ===" + RESET)
        print(GREEN + "[T] Tambah Data")
        print(YELLOW + "[C] Cari Data Terbanyak")
        print(WHITE + "[K] Keterangan / Total")
        print(MAGENTA + "[A] Edit Data Bulanan")
        print(RED + "[B] Hapus Data")
        print(CYAN + "[R] Restore Data Terhapus")
        print(RED + "[Q] Keluar" + RESET)

        pilihan = input(CYAN + "Pilih menu: " + RESET).strip().upper()

        if pilihan == "T":
            tambah_data(data_list)
            save_data(file_path, data_list)
        elif pilihan == "C":
            cari_terbanyak(data_list)
        elif pilihan == "K":
            for item in data_list:
                tampilkan_item(item)
            cek_total(data_list)
        elif pilihan == "A":
            edit_data(data_list)
            save_data(file_path, data_list)
        elif pilihan == "B":
            hapus_data(data_list, trash_list)
            save_data(file_path, data_list)
            save_data(trash_path, trash_list)
        elif pilihan == "R":
            restore_data(data_list, trash_list)
            save_data(file_path, data_list)
            save_data(trash_path, trash_list)
        elif pilihan == "Q":
            print(CYAN + "Keluar aplikasi." + RESET)
            break
        else:
            print(RED + "Pilihan tidak valid." + RESET)

if __name__ == "__main__":
    main()


