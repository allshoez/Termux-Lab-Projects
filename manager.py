#!/usr/bin/env python3
import os, curses, shutil, subprocess

ICONS = {
    "folder": "📂",
    "file": "📄",
    "image": "🖼️",
    "video": "🎞️",
    "audio": "🎵",
    "archive": "📦",
    "hidden": "•",
    "up_dir": "↑"
}

SELECTED_ITEMS = set()
SHOW_HIDDEN = False

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
    items = [".."] if path != os.path.abspath(os.sep) else []
    try:
        for i in os.listdir(path):
            if not show_hidden and i.startswith("."): continue
            items.append(i)
    except: return [".."]
    dirs = [i for i in items if i!=".." and os.path.isdir(os.path.join(path,i))]
    files= [i for i in items if i!=".." and not os.path.isdir(os.path.join(path,i))]
    return ([".."] if ".." in items else []) + sorted(dirs,key=str.lower)+sorted(files,key=str.lower)

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

def file_manager(stdscr):
    global SELECTED_ITEMS, SHOW_HIDDEN
    curses.curs_set(0); curses.start_color()
    curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_YELLOW)
    curses.init_pair(4,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(5,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(6,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(7,curses.COLOR_BLACK,curses.COLOR_GREEN)

    current = "/sdcard" if os.path.exists("/sdcard") else "/"
    selected, scroll, msg = 0, 0, "Spasi=👉Select | Enter=Buka | A=Aksi | h=Hidden | H=Home | q=Quit"

    while True:
        stdscr.clear(); h,w=stdscr.getmaxyx()
        stdscr.addstr(0,0,f"📂 {current} | Dipilih: {len(SELECTED_ITEMS)}",curses.color_pair(4)|curses.A_BOLD)
        stdscr.addstr(1,0,"-"*(w-1),curses.color_pair(4))

        items = list_dir(current,SHOW_HIDDEN)
        if not items: selected=-1
        elif selected>=len(items): selected=len(items)-1
        elif selected<0: selected=0

        start=2; viewh=h-6
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
            if y<h-2: stdscr.addstr(y,0,line[:w-1],color)

        stdscr.addstr(h-3,0,"-"*(w-1),curses.color_pair(4))
        stdscr.addstr(h-2,0,msg[:w-1],curses.color_pair(6)); msg=""
        stdscr.refresh()

        key=stdscr.getch(); keyc=chr(key) if 32<=key<=126 else None

        if key in (10,13): # Enter
            if selected==-1: continue
            chosen=os.path.join(current,items[selected])
            if os.path.isdir(chosen): current,selected,scroll=chosen,0,0; SELECTED_ITEMS.clear()
            elif os.path.isfile(chosen): subprocess.run(["xdg-open",chosen],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
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
