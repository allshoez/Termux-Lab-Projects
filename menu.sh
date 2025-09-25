
#!/bin/bash

=======================

File Manager HP Full Hybrid + List Rapi + Lihat folder/file back-friendly

=======================

Cek whiptail

command -v whiptail >/dev/null 2>&1 || { echo >&2 "Install whiptail dulu: pkg install whiptail"; exit 1; }

Fungsi warna

colors=(34 32 36 35 33 37)
function color_line() {
text="$1"
index="$2"
color=${colors[$((index % ${#colors[@]}))]}
echo -e "\e[1;${color}m${text}\e[0m"
}

=======================

Fungsi daftar file rapi

=======================

list_files() {
echo -e "\e[1;33mDaftar File & Folder Saat Ini:\e[0m"
printf "%-10s %-12s %-8s %-6s %-8s %s\n" "Perm" "Owner" "Size" "Month" "Day" "Nama File"
echo "---------------------------------------------------------------"
for f in *; do
perm=$(stat -c "%A" "$f")
owner=$(stat -c "%U" "$f")
size=$(stat -c "%s" "$f")
month=$(stat -c "%b" "$f")
day=$(stat -c "%d" "$f")
if [ -d "$f" ]; then
printf "%-10s %-12s %-8s %-6s %-8s \e[1;34m%s\e[0m\n" "$perm" "$owner" "$size" "$month" "$day" "$f"
else
printf "%-10s %-12s %-8s %-6s %-8s %s\n" "$perm" "$owner" "$size" "$month" "$day" "$f"
fi
done
echo
}

=======================

Submenu Manage

=======================

manage_submenu() {
while true; do
clear
list_files
color_line "1. Buat folder baru" 0
color_line "2. Buat file baru" 1
color_line "3. Hapus folder" 2
color_line "4. Hapus file" 3
color_line "5. Rename folder" 4
color_line "6. Rename file" 5
color_line "7. Copy folder" 6
color_line "8. Copy file" 7
color_line "9. Lihat isi folder" 8
color_line "10. Lihat isi file" 9
color_line "11. Back" 10
echo
read -p "Pilih menu : " sub
case $sub in
1)
echo -e "\e[1;33mfolder:\e[0m"
read d
[ -n "$d" ] && mkdir -p "$d"
;;
2)
echo -e "\e[1;36mFile:\e[0m"
read f
[ -n "$f" ] && touch "$f"
;;
3)
echo -e "\e[1;31mFolder untuk dihapus:\e[0m"
read d
[ -d "$d" ] && rm -r "$d"
;;
4)
echo -e "\e[1;31mFile untuk dihapus:\e[0m"
read f
[ -f "$f" ] && rm "$f"
;;
5)
echo -e "\e[1;33mFolder lama:\e[0m"
read old
echo -e "\e[1;32mFolder baru:\e[0m"
read new
[ -d "$old" ] && mv "$old" "$new"
;;
6)
echo -e "\e[1;33mFile lama:\e[0m"
read old
echo -e "\e[1;32mFile baru:\e[0m"
read new
[ -f "$old" ] && mv "$old" "$new"
;;
7)
echo -e "\e[1;34mFolder sumber:\e[0m"
read src
echo -e "\e[1;34mFolder tujuan:\e[0m"
read dst
[ -d "$src" ] && cp -r "$src" "$dst"
;;
8)
echo -e "\e[1;34mFile sumber:\e[0m"
read src
echo -e "\e[1;34mFile tujuan:\e[0m"
read dst
[ -f "$src" ] && cp "$src" "$dst"
;;
9)
echo -e "\e[1;36mMasukkan nama folder untuk dilihat isinya:\e[0m"
read folder
if [ -d "$folder" ]; then
echo -e "\e[1;33mIsi folder $folder:\e[0m"
ls -lah "$folder"
echo
read -n1 -r -p "Tekan sembarang tombol untuk kembali..."
else
echo "Folder tidak ditemukan."
read -n1 -r -p "Tekan sembarang tombol untuk kembali..."
fi
;;
10)
echo -e "\e[1;36mMasukkan nama file untuk dilihat isinya:\e[0m"
read file
if [ -f "$file" ]; then
echo -e "\e[1;33mIsi file $file:\e[0m"
cat "$file"
echo
read -n1 -r -p "Tekan sembarang tombol untuk kembali..."
else
echo "File tidak ditemukan."
read -n1 -r -p "Tekan sembarang tombol untuk kembali..."
fi
;;
11) break;;
*) echo "Pilihan salah, coba lagi.";;
esac
done
}

=======================

Menu utama whiptail

=======================

while true; do
OPTION=$(whiptail --title "File Manager HP" --menu "Pilih menu:" 20 60 10 \
"1" "Buat file" \
"2" "Buat folder" \
"3" "Multi buat folder/file" \
"4" "Manage file/folder" \
"5" "Exit" 3>&1 1>&2 2>&3)

exitstatus=$?
[ $exitstatus != 0 ] && break

case $OPTION in
    1)
        echo -e "\e[1;36mMasukkan nama file (contoh: app.py):\e[0m"
        read FILE
        [ -n "$FILE" ] && touch "$FILE"
        ;;
    2)
        echo -e "\e[1;33mMasukkan nama folder (contoh: Ayam):\e[0m"
        read FOLDER
        [ -n "$FOLDER" ] && mkdir -p "$FOLDER"
        ;;
    3)
        while true; do
            echo -e "\e[1;33mFolder (Enter skip / x Back):\e[0m"
            read FOLDER
            [ "$FOLDER" == "x" ] && break
            [ -n "$FOLDER" ] && mkdir -p "$FOLDER"
            echo -e "\e[1;36mFile (Enter skip / x Back):\e[0m"
            read FILE
            [ "$FILE" == "x" ] && break
            [ -n "$FILE" ] && {
                if [ -n "$FOLDER" ]; then touch "$FOLDER/$FILE"; else touch "$FILE"; fi
            }
        done
        ;;
    4) manage_submenu;;
    5) break;;
esac

done

clear
echo "Terima kasih sudah menggunakan File Manager HP Full Hybrid!"
