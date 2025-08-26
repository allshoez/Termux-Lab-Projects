
from flask import Flask
import os, time
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#ffffff" />
  <meta name="viewport" content="width=device-width, initial-scale=1.2"/>
  <link rel="apple-touch-icon" href="/icon/icon-192.png" />
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
  <title>Catatan GPT</title>
  <style>
    body {
      background: #000;
      color: #0ff;
      font-family: 'Inter', sans-serif;
      display: flex;
      flex-direction: column;
      height: 90vh;
      margin: 0;
      font-size: 20px;
    }
    h1 {
      text-align: center;
      padding: 5px;
      background: #111;
      color: #0ff;
      text-shadow: 0 0 10px #0ff;
    }
    #chatbox {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
    }
    .message {
      display: inline-block;
      margin: 5px 0;
      padding: 10px 15px;
      border-radius: 20px;
      max-width: 70%;
      box-shadow: 0 0 10px #0ff;
    }
    .user {
      background: #0f0;
      color: #000;
      float: right;
      clear: both;
      border-radius: 8px 0px 10px 0px;
    }
    .bot {
      background: #fff;
      color: #000;
      float: left;
      clear: both;
      border-radius: 8px 0px 20px 0px;
    }
    #inputArea {
      display: flex;
      padding: 10px;
      background: #111;
      border-top: 2px solid #0ff;
    }
    #userInput {
      flex: 1;
      padding: 12px;
      font-size: 16px;
      border: none;
      border-radius: 20px;
      background: #000;
      color: #0ff;
    }
    #sendBtn {
      margin-left: 10px;
      padding: 12px 20px;
      font-size: 16px;
      border: none;
      border-radius: 20px;
      background: #0ff;
      color: #000;
      cursor: pointer;
    }
    #menu {
      position: absolute;
      top: 10px;
      right: 10px;
      cursor: pointer;
      color: #0ff;
    }
    #popup {
      position: absolute;
      top: 80px;
      right: 10px;
      background: #111;
      border: 1px solid #0ff;
      display: none;
      border-radius: 10px;
    }
    #popup button {
      display: block;
      width: 100%;
      background: #000;
      color: #0ff;
      border: none;
      padding: 10px;
      text-align: left;
    }
    
    /* Modal */
    #modal {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.7);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 999;
    }
    #modalContent {
      background: #111;
      border: 2px solid #0ff;
      border-radius: 10px;
      padding: 10px;
      width: 90%;
      max-width: 600px;
      height: 50%;
      display: flex;
      flex-direction: column;
    }
    #modalTextarea {
      flex: 1;
      width: 100%;
      background: #000;
      color: #0ff;
      border: none;
      resize: none;
      padding: 10px;
      font-family: monospace;
      font-size: 14px;
    }
    #modalSaveBtn {
      margin-top: 10px;
      padding: 10px;
      border: none;
      background: #0ff;
      color: #000;
      cursor: pointer;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <p>
    <p>
  <h1>💬 Catatan </h1>
  <p>
  <div id="menu">☰ Menu</div>
  <div id="popup">
    <button onclick="lihatDataset()">📜 Lihat Dataset</button>
    <button onclick="editDataset()">✏️ Edit Dataset</button>
    <button id="importBtn">🔎 Import Data</button>
    <button id="exportBtn">📂 Export Data</button>
  </div>

  <div id="chatbox"></div>

  <div id="inputArea">
    <input type="text" id="userInput" placeholder="Tulis di sini..." />
    <button id="sendBtn">></button>
  </div>

  <!-- Modal -->
  <div id="modal">
    <div id="modalContent">
      <textarea id="modalTextarea"></textarea>
      <button id="modalSaveBtn">💾 Simpan</button>
    </div>
  </div>

  <!-- File input hidden -->
  <input type="file" id="fileInput" accept=".json" style="display:none;">

  <script>
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const menu = document.getElementById('menu');
    const popup = document.getElementById('popup');

    let lastKey = null;

    sendBtn.onclick = handleInput;
    userInput.addEventListener('keypress', e => { if (e.key === 'Enter') handleInput(); });
    menu.onclick = () => popup.style.display = popup.style.display === 'block' ? 'none' : 'block';

    function addMessage(sender, text) {
      const div = document.createElement('div');
      div.className = `message ${sender}`;
      div.innerText = text; // no jam
      chatbox.appendChild(div);
      chatbox.scrollTop = chatbox.scrollHeight;
    }

    function getDataset() {
      return JSON.parse(localStorage.getItem('dataset') || '{}');
    }

    function saveDataset(data) {
      localStorage.setItem('dataset', JSON.stringify(data));
    }

    function handleInput() {
      const text = userInput.value.trim();
      if (!text) return;
      addMessage('user', text);
      let dataset = getDataset();
      let reply = '';

      if (lastKey) {
        dataset[lastKey] = text;
        saveDataset(dataset);
        reply = `Simpan: ${lastKey} ➜ ${text}`;
        lastKey = null;
      } else {
        let found = false;
        for (const key in dataset) {
          if (text.toLowerCase().includes(key.toLowerCase())) {
            reply = `${key} ➜ ${dataset[key]}`;
            found = true;
            break;
          }
        }
        if (!found) {
          lastKey = text;
          reply = 'Data belum ada. Apa jawabannya?';
        }
      }

      addMessage('bot', reply);
      userInput.value = '';
    }

    function openModal(text, saveCallback) {
      const modal = document.getElementById('modal');
      const textarea = document.getElementById('modalTextarea');
      const saveBtn = document.getElementById('modalSaveBtn');

      textarea.value = text;
      modal.style.display = 'flex';

      saveBtn.onclick = () => {
        saveCallback(textarea.value);
        modal.style.display = 'none';
      };
    }

    document.getElementById('modal').addEventListener('click', function(e) {
      if (e.target.id === 'modal') {
        this.style.display = 'none';
      }
    });

    function lihatDataset() {
      const dataset = getDataset();
      openModal(JSON.stringify(dataset, null, 2), () => {});
    }

    function editDataset() {
      const dataset = getDataset();
      openModal(JSON.stringify(dataset, null, 2), newText => {
        try {
          saveDataset(JSON.parse(newText));
          alert('Dataset diperbarui!');
        } catch (e) {
          alert('Format JSON salah!');
        }
      });
    }

    // Import Export
    let dataset = [];

    document.getElementById('importBtn').addEventListener('click', function() {
      document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', function(e) {
      const file = e.target.files[0];
      const reader = new FileReader();

      reader.onload = function(event) {
        try {
          dataset = JSON.parse(event.target.result);
          console.log('Dataset di-import:', dataset);
          alert('Import sukses! Lihat console log.');
        } catch (err) {
          console.error('File bukan JSON valid:', err);
          alert('File bukan JSON valid.');
        }
      };

      reader.readAsText(file);
    });

    document.getElementById('exportBtn').addEventListener('click', function() {
      const dataStr = JSON.stringify(dataset, null, 2);
      const blob = new Blob([dataStr], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = 'dataset.json';
      a.click();

      URL.revokeObjectURL(url);
    });

    // Pesan awal tanpa jam
    addMessage('bot', '🤖 Masukan data ➜ kalau belum ada ➜ bot minta data.');
    
// Tutup popup kalau klik di luar popup
document.addEventListener('click', (e) => {
  // kalau klik target bukan menu dan bukan popup (termasuk anaknya)
  if (!popup.contains(e.target) && e.target !== menu) {
    popup.style.display = 'none';
  }
});

// Tutup popup otomatis kalau user pindah tab/window
window.addEventListener('blur', () => {
  popup.style.display = 'none';
});
  </script>
</body>
</html>"""

if __name__ == "__main__":
    def run_flask():
        app.run(host="127.0.0.1", port=5000)

    t = Thread(target=run_flask)
    t.start()
    time.sleep(2)  # tunggu server siap
    # otomatis muncul pilihan browser di Android
    os.system('am start -a android.intent.action.VIEW -d "http://127.0.0.1:5000"')
    t.join()
