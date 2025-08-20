
#!/usr/bin/env python3
import os
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import asyncio
import websockets

# ===== CONFIG =====
DEFAULT_PORT = 8080
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

# ===== SERVER HANDLER =====
class TermuxHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.endswith(".html"):
            self.send_header("Content-type", "text/html")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"{CYAN}[REQ]{RESET} {self.address_string()} - {format % args}")

# ===== WATCHDOG HANDLER =====
class ReloadHandler(FileSystemEventHandler):
    def __init__(self, ws_server):
        self.ws_server = ws_server

    def on_modified(self, event):
        if event.src_path.endswith((".html", ".js", ".css")):
            print(f"{YELLOW}[MODIFIED]{RESET} {event.src_path} → Reload browser")
            self.ws_server.broadcast_reload()

# ===== WEBSOCKET MINI SERVER =====
class WSServer:
    def __init__(self, port=9000):
        self.port = port
        self.clients = set()

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)

    def broadcast_reload(self):
        asyncio.run(self._broadcast())

    async def _broadcast(self):
        if self.clients:
            await asyncio.wait([client.send("reload") for client in self.clients])

    def start(self):
        asyncio.run(self._run_server())

    async def _run_server(self):
        async with websockets.serve(self.handler, "0.0.0.0", self.port):
            print(f"{GREEN}[INFO]{RESET} WebSocket live reload aktif di ws://0.0.0.0:{self.port}")
            await asyncio.Future()  # run forever

# ===== START HTTP SERVER =====
def start_server(directory, port):
    os.chdir(directory)
    server = HTTPServer(("0.0.0.0", port), TermuxHTTPRequestHandler)
    print(f"\n{GREEN}[INFO]{RESET} 🚀 Mini server aktif di http://0.0.0.0:{port}\n")
    server.serve_forever()

# ===== UTILS =====
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "localhost"
    finally:
        s.close()
    return ip

# ===== MAIN =====
def main():
    print(f"{MAGENTA}" + "="*50 + f"{RESET}")
    print(f"{MAGENTA}🔥 Termux-style Super Mini Server 🔥{RESET}")
    print(f"{MAGENTA}" + "="*50 + f"{RESET}")

    project_name = input(f"{BLUE}📂 Nama proyek: {RESET}").strip()
    if not project_name:
        print(f"{RED}❌ Nama proyek tidak boleh kosong!{RESET}")
        return

    port_input = input(f"{BLUE}🔌 Masukkan port (default {DEFAULT_PORT}): {RESET}").strip()
    try:
        port = int(port_input) if port_input else DEFAULT_PORT
    except ValueError:
        print(f"{RED}❌ Port tidak valid, pakai default {DEFAULT_PORT}{RESET}")
        port = DEFAULT_PORT

    project_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_path, exist_ok=True)
    print(f"{GREEN}[INFO]{RESET} Folder proyek: {project_path}")

    # ===== AUTO INDEX.HTML =====
    index_file = os.path.join(project_path, "index.html")
    if not os.path.exists(index_file):
        with open(index_file, "w") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Welcome</title>
<style>
body {{ font-family: Arial, sans-serif; text-align:center; padding-top:50px; background:#f0f0f0; }}
h1 {{ color: #4CAF50; }}
p {{ color: #333; }}
</style>
</head>
<body>
<h1>🔥 Server Aktif! 🔥</h1>
<p>Project: {project_name}</p>
<p>Port: {port}</p>
<script>
let ws = new WebSocket("ws://localhost:9000");
ws.onmessage = () => location.reload();
</script>
</body>
</html>""")

    url = f"http://localhost:{port}"
    ip_local = get_local_ip()
    print(f"{GREEN}[INFO]{RESET} Akses dari HP lain di jaringan Wi-Fi: http://{ip_local}:{port}")

    # Start HTTP server
    threading.Thread(target=start_server, args=(project_path, port), daemon=True).start()

    # Start WebSocket server for live reload
    ws_server = WSServer()
    threading.Thread(target=ws_server.start, daemon=True).start()

    # Watchdog untuk live reload
    observer = Observer()
    observer.schedule(ReloadHandler(ws_server), path=project_path, recursive=True)
    observer.start()

    # Open browser otomatis
    try:
        webbrowser.get("chrome").open(url)
    except:
        try:
            webbrowser.open(url)
        except:
            print(f"{YELLOW}[INFO]{RESET} Buka manual: {url}")

    print(f"{GREEN}[INFO]{RESET} Tekan Ctrl+C untuk hentikan server")
    print(f"{GREEN}[INFO]{RESET} Terminal commands: ls, cd <folder>, exit\n")

    # Terminal interaktif ala Termux
    try:
        while True:
            cmd = input(f"{MAGENTA}termux-server> {RESET}").strip()
            if cmd.lower() in ("exit", "quit"):
                print(f"{GREEN}[INFO]{RESET} Server dihentikan.")
                break
            elif cmd.lower() == "ls":
                for f in os.listdir(project_path):
                    print(f" - {f}")
            elif cmd.lower().startswith("cd "):
                new_dir = cmd[3:].strip()
                path = os.path.join(project_path, new_dir)
                if os.path.isdir(path):
                    os.chdir(path)
                    print(f"{GREEN}[INFO]{RESET} Pindah ke {path}")
                else:
                    print(f"{RED}[ERROR]{RESET} Folder tidak ada!")
            else:
                print(f"{YELLOW}[INFO]{RESET} Perintah: ls, cd <folder>, exit")
    except KeyboardInterrupt:
        print(f"\n{GREEN}[INFO]{RESET} Server dihentikan.")
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
