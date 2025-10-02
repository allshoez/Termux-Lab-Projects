#!/usr/bin/env python3
import os, curses, shutil, subprocess

ICONS = {
    "folder": "📂",
    "file": "📄",
    "image": "🖼️",
    "video": "️🎬",
    "audio": "🎧",
    "archive": "📜",
    "hidden": "📌",
    "up_dir": "↑"
}

SELECTED_ITEMS = set()
SHOW_HIDDEN = False
MAX_PREVIEW_LINES = 100 
VIEW_MODE = "NORMAL" 
FILTER_QUERY = "" # Variabel global baru untuk menyimpan string filter/search

def get_icon(item, path):
    full = os.path.join(path, item)
    if item == "..": return ICONS["up_dir"]
    if item.startswith("."): return ICONS["hidden"]
    if os.path.isdir(full): return ICONS["folder"]
    ext = item.lower().split('.')[-1]
    if ext in ("png","jpg","jpeg","gif","webp"): return ICONS["image"]
    if ext in ("mp4","mkv","avi","mov"): return ICONS["video"]
    if ext in ("mp3","flac","wav","ogg"): return ICONS["audio"]
    if ext in ("zip","tar","gz","rar"): return ICONS["archive"]
    return ICONS["file"]

def list_dir(path, show_hidden=False):
    # Dapatkan semua item
    items = [".."] if path != os.path.abspath(os.sep) else []
    full_list = []
    try:
        for i in os.listdir(path):
            if not show_hidden and i.startswith("."): continue
            full_list.append(i)
    except: return [".."]
    
    # Pisahkan dan urutkan
    dirs = [i for i in full_list if i!=".." and os.path.isdir(os.path.join(path,i))]
    files= [i for i in full_list if i!=".." and not os.path.isdir(os.path.join(path,i))]
    
    # Gabungkan, termasuk '..' di awal jika ada
    all_items = ([".."] if ".." in items else []) + sorted(dirs,key=str.lower)+sorted(files,key=str.lower)

    # --- Terapkan Filter Query ---
    global FILTER_QUERY
    if FILTER_QUERY:
        # Filter item yang nama file-nya mengandung query (case-insensitive)
        query = FILTER_QUERY.lower()
        filtered_items = [
            i for i in all_items 
            if i == ".." or query in i.lower()
        ]
        return filtered_items
        
    return all_items

def get_file_preview(path, max_lines, max_width):
    # ... (Fungsi ini tidak berubah)
    if not os.path.exists(path):
        return ["File tidak ditemukan."]
    
    if os.path.isdir(path):
        try:
            items = os.listdir(path)
            count = len(items)
            size = sum(os.path.getsize(os.path.join(path, i)) for i in items if os.path.isfile(os.path.join(path, i)))
            return [
                "*** INFO DIREKTORI ***",
                f"Nama: {os.path.basename(path)}",
                f"Isi: {count} item",
                f"Ukuran File Total: {size / (1024*1024):.2f} MB (Perkiraan)",
                "------------------------",
                "Isi Awal:",
            ] + [f"  - {i[:max_width-4]}" for i in sorted(items, key=str.lower)[:max_lines-6]]
        except Exception as e:
            return [f"ERROR: Tidak dapat membaca direktori. {e}"]
    
    if not os.path.isfile(path):
        return ["Bukan file atau direktori."]

    try:
        size = os.path.getsize(path)
        if size > 1024 * 1024 * 5: 
            return [
                "*** PREVIEW DIBATASI ***",
                f"Ukuran File: {size / (1024*1024):.2f} MB",
                "File terlalu besar untuk preview teks.",
                "Gunakan Enter untuk membuka file."
            ]
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f"| {line.rstrip()[:max_width-3]}" for i, line in enumerate(f) if i < max_lines]
            return [
                "*** PREVIEW SOURCE ***",
                f"Ukuran: {size / 1024:.2f} KB",
                "------------------------"
            ] + lines
    except UnicodeDecodeError:
        return [
            "*** PREVIEW GAGAL ***",
            "File mungkin merupakan biner atau tidak dapat di-decode.",
            "Gunakan Enter untuk membuka file."
        ]
    except Exception as e:
        return [f"ERROR: {e}"]

def get_input(stdscr, prompt, default=""):
    h,w = stdscr.getmaxyx()
    stdscr.addstr(h-2,0," "*(w-1))
    stdscr.addstr(h-2,0,prompt[:w-1],curses.color_pair(6)|curses.A_BOLD)
    curses.echo(); curses.curs_set(1)
    win = curses.newwin(1,w-len(prompt)-2,h-2,len(prompt))
    win.addstr(0,0,default[:w-len(prompt)-2]); win.move(0,len(default))
    val = win.getstr().decode()
    curses.noecho(); curses.curs_set(0)
    stdscr.addstr(h-2,0," "*(w-1))
    return val

def popup_menu(stdscr, options, title="Pilih Aksi"):
    # ... (Fungsi ini tidak berubah)
    h,w = stdscr.getmaxyx()
    ph = len(options)+2; pw = max(len(title), max(len(o) for o in options))+4
    starty, startx = max(0,h//2-ph//2), max(0,w//2-pw//2)
    win = curses.newwin(ph,pw,starty,startx); win.keypad(True)
    win.border(); win.addstr(0,2,f" {title} ",curses.A_BOLD)
    idx = 0
    while True:
        for i,opt in enumerate(options):
            if i==idx: win.attron(curses.color_pair(3)); win.addstr(i+1,2,opt); win.attroff(curses.color_pair(3))
            else: win.addstr(i+1,2,opt)
        key = win.getch()
        if key in (curses.KEY_UP,ord("k")): idx=(idx-1)%len(options)
        elif key in (curses.KEY_DOWN,ord("j")): idx=(idx+1)%len(options)
        elif key in (10,13): return options[idx]
        elif key==27: return "Batal"

def show_help(stdscr):
    # Perbarui list bantuan untuk menyertakan 's'
    HELP_OPTIONS = [
        "NAVIGASI & PINTASAN",
        "↑/k - Pindah ke atas",
        "↓/j - Pindah ke bawah",
        "Enter - Masuk Folder / Buka File",
        "Space - Tandai/Pilih File/Folder (Multi-select)",
        "s - Search/Filter berdasarkan nama file", # Tambahan
        "h - Tampilkan/Sembunyikan File Tersembunyi",
        "H - Pergi ke Home Termux (/data/data/...) ",
        "A - Tampilkan menu Aksi (Hapus, Rename, Copy, dll.)",
        "M - Ganti Mode Tampilan (Normal/Vertikal/Horizontal)",
        "? - Tampilkan menu Bantuan ini",
        "q - Keluar dari Manajer File",
        " ",
        "AKSI PILIHAN (Menu 'A')",
        "Hapus - Hapus file/folder yang dipilih",
        "Rename - Ubah nama item (hanya 1 item)",
        "Copy - Salin item ke tujuan",
        "Move - Pindahkan/Potong item ke tujuan",
        "Buat File - Buat file kosong baru",
        "Buat Folder - Buat folder baru",
        " ",
        "TEKAN ESC ATAU Q UNTUK KEMBALI"
    ]
    h,w = stdscr.getmaxyx()
    ph = len(HELP_OPTIONS)+2; pw = max(len(o) for o in HELP_OPTIONS)+4
    starty, startx = max(0,h//2-ph//2), max(0,w//2-pw//2)
    
    win = curses.newwin(ph,pw,starty,startx); win.keypad(True)
    win.border(); win.addstr(0,2," PANDUAN PENGGUNA ",curses.color_pair(4)|curses.A_BOLD)
    
    for i,opt in enumerate(HELP_OPTIONS):
        color = curses.color_pair(5)|curses.A_BOLD if opt.isupper() and len(opt)>1 and not opt.isspace() else curses.color_pair(1)
        if opt.isspace(): continue
        win.addstr(i+1,2,opt[:pw-4],color)
    
    while True:
        key = win.getch()
        if key in (27, ord('q')): break 

def file_manager(stdscr):
    global SELECTED_ITEMS, SHOW_HIDDEN, VIEW_MODE, FILTER_QUERY
    curses.curs_set(0); curses.start_color()
    curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_YELLOW)
    curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(5,curses.COLOR_GREEN,curses.COLOR_BLACK) 
    curses.init_pair(6,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(7,curses.COLOR_BLACK,curses.COLOR_GREEN)

    current = "/sdcard" if os.path.exists("/sdcard") else "/"
    selected, scroll, msg = 0, 0, "" 
    
    while True:
        stdscr.clear(); h,w=stdscr.getmaxyx()
        
        # --- PENENTUAN UKURAN PANEL BERDASARKAN MODE ---
        if VIEW_MODE == "NORMAL":
            list_w = w 
            preview_w = 0 
            list_h = h - 4 
            preview_y_start = h 
            list_y_limit = h - 3 
            viewh = list_h - 1 
        elif VIEW_MODE == "VERTICAL":
            list_w = w // 2 
            preview_w = w - list_w 
            list_h = h - 4 
            preview_y_start = 2 
            list_y_limit = h - 3 
            viewh = list_h - 1 
        else: # Horizontal Mode
            list_w = w 
            preview_w = w 
            list_h = (h - 4) // 2 
            preview_y_start = 2 + list_h 
            list_y_limit = preview_y_start 
            viewh = list_h - 1 
            
        # --- HEADER ---
        mode_text = f"[{VIEW_MODE}]"
        
        # Tambahkan indikator Filter aktif di header
        filter_status = f" | Filter: '{FILTER_QUERY}'" if FILTER_QUERY else ""
        stdscr.addstr(0,0,f"📂 {current} | Dipilih: {len(SELECTED_ITEMS)} | Mode: {mode_text}{filter_status}",curses.color_pair(4)|curses.A_BOLD)
        stdscr.addstr(1,0,"-"*(w-1),curses.color_pair(4))

        items = list_dir(current,SHOW_HIDDEN)
        if not items: selected=-1
        elif selected>=len(items): selected=len(items)-1
        elif selected<0: selected=0

        # --- PANEL DAFTAR FILE ---
        start=2
        if selected<scroll: scroll=selected
        elif selected>=scroll+viewh: scroll=selected-viewh+1

        for idx,item in enumerate(items[scroll:scroll+viewh]):
            abs_path=os.path.join(current,item)
            icon=get_icon(item,current)
            mark="👉" if item in SELECTED_ITEMS else "  "
            line=f"{mark} {icon} {item}"
            y=start+idx
            color=curses.color_pair(3) if idx+scroll==selected else curses.color_pair(2 if os.path.isdir(abs_path) else 1)
            if item in SELECTED_ITEMS: color=curses.color_pair(7)
            if y < list_y_limit: 
                stdscr.addstr(y,0,line[:list_w-1],color)
        
        for y in range(start + len(items[scroll:scroll+viewh]), list_y_limit):
            stdscr.addstr(y, 0, " " * (list_w - 1))


        # --- PEMISAH & PANEL PREVIEW ---
        if VIEW_MODE == "VERTICAL":
            stdscr.vline(2, list_w-1, '|', list_h-1, curses.color_pair(4)) 
        elif VIEW_MODE == "HORIZONTAL": 
            stdscr.addstr(list_y_limit - 1, 0, "="*(w-1), curses.color_pair(4))

        if VIEW_MODE != "NORMAL":
            preview_x = list_w if VIEW_MODE == "VERTICAL" else 0
            preview_h = h - 3 - preview_y_start
            
            preview_text = []
            if selected != -1:
                abs_path_selected = os.path.join(current, items[selected])
                preview_text = get_file_preview(abs_path_selected, preview_h, preview_w)
            else:
                preview_text = ["(Tidak ada item dipilih)"]

            for i, line in enumerate(preview_text[:preview_h]):
                y = preview_y_start + i
                if y < h - 3:
                    color = curses.color_pair(5) if line.startswith("***") else curses.color_pair(1)
                    stdscr.addstr(y, preview_x, line[:preview_w-1], color)
            
            for y in range(preview_y_start + len(preview_text[:preview_h]), h-3):
                 stdscr.addstr(y, preview_x, " " * (preview_w - 1))


        # --- FOOTER ---
        stdscr.addstr(h-3,0,"-"*(w-1),curses.color_pair(4))
        
        # Baris Bantuan Ringkas
        help_info = "Tekan '?' untuk Bantuan"
        stdscr.addstr(h-2,0,help_info[:w-1],curses.color_pair(4)) 
        
        # Baris pesan error/feedback
        stdscr.addstr(h-1,0," "*(w-1)) 
        stdscr.addstr(h-1,0,msg[:w-1],curses.color_pair(6)); msg=""
        
        stdscr.refresh()

        key=stdscr.getch(); keyc=chr(key) if 32<=key<=126 else None

        if key in (10,13): # Enter
            if selected==-1: continue
            chosen=os.path.join(current,items[selected])
            if os.path.isdir(chosen): current,selected,scroll=chosen,0,0; SELECTED_ITEMS.clear()
            elif os.path.isfile(chosen): subprocess.run(["xdg-open",chosen],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        elif keyc in ("s","S"): # --- FITUR SEARCH BARU ---
            # Dapatkan input dari pengguna, default-nya adalah query yang sudah ada
            new_query = get_input(stdscr, "Search/Filter: ", FILTER_QUERY)
            
            # Jika query baru berbeda, update global query dan reset view
            if new_query != FILTER_QUERY:
                FILTER_QUERY = new_query
                selected, scroll = 0, 0
                msg = f"Filter aktif: '{FILTER_QUERY}'" if FILTER_QUERY else "Filter dinonaktifkan"
            
            # Jika pengguna menekan Enter/ESC tanpa mengubah, tidak terjadi apa-apa.
            
        elif keyc in ("a","A"):
            if selected==-1: continue
            opts=["Hapus","Rename","Copy","Move","Buat File","Buat Folder","Batal"]
            choice=popup_menu(stdscr,opts)
            targets=list(SELECTED_ITEMS) if SELECTED_ITEMS else [items[selected]]
            try:
                if choice=="Hapus":
                    for t in targets:
                        path=os.path.join(current,t)
                        if os.path.isdir(path): shutil.rmtree(path)
                        else: os.remove(path)
                    msg=f"{len(targets)} terhapus"; SELECTED_ITEMS.clear()
                elif choice=="Rename":
                    if len(targets)!=1: msg="Pilih 1 file/folder"
                    else:
                        new=get_input(stdscr,"Nama baru: ",targets[0])
                        if new: os.rename(os.path.join(current,targets[0]),os.path.join(current,new))
                elif choice=="Copy":
                    dest=get_input(stdscr,"Tujuan copy: ",current)
                    if dest: [shutil.copytree(os.path.join(current,t),os.path.join(dest,t),dirs_exist_ok=True) if os.path.isdir(os.path.join(current,t)) else shutil.copy2(os.path.join(current,t),dest) for t in targets]
                elif choice=="Move":
                    dest=get_input(stdscr,"Tujuan move: ",current)
                    if dest: [shutil.move(os.path.join(current,t),dest) for t in targets]
                elif choice=="Buat File":
                    name=get_input(stdscr,"Nama file baru: ")
                    if name: open(os.path.join(current,name),"w").close()
                elif choice=="Buat Folder":
                    name=get_input(stdscr,"Nama folder baru: ")
                    if name: os.makedirs(os.path.join(current,name),exist_ok=True)
            except Exception as e: msg=f"ERR: {e}"
        elif keyc in ("m","M"):
            opts = ["Mode Normal (Hanya Daftar)", "Mode Vertikal (Dampingan)", "Mode Horizontal (Atas-Bawah)", "Batal"]
            choice = popup_menu(stdscr, opts, title="Pilih Mode Tampilan")
            if choice == "Mode Normal (Hanya Daftar)":
                VIEW_MODE = "NORMAL"
                msg = "Mode diatur ke Normal"
            elif choice == "Mode Vertikal (Dampingan)":
                VIEW_MODE = "VERTICAL"
                msg = "Mode diatur ke Vertikal"
            elif choice == "Mode Horizontal (Atas-Bawah)":
                VIEW_MODE = "HORIZONTAL"
                msg = "Mode diatur ke Horizontal"
            stdscr.clear(); stdscr.refresh() 
        elif keyc == "?":
            show_help(stdscr)
        elif key==curses.KEY_UP: selected=(selected-1)%len(items)
        elif key==curses.KEY_DOWN: selected=(selected+1)%len(items)
        elif key==ord(" "):
            if items[selected]!="..":
                if items[selected] in SELECTED_ITEMS: SELECTED_ITEMS.remove(items[selected])
                else: SELECTED_ITEMS.add(items[selected])
        elif keyc=="h": SHOW_HIDDEN=not SHOW_HIDDEN; SELECTED_ITEMS.clear()
        elif keyc=="H": current,selected,scroll="/data/data/com.termux/files/home",0,0; SELECTED_ITEMS.clear()
        elif keyc=="q": break

if __name__=="__main__":
    curses.wrapper(file_manager)
