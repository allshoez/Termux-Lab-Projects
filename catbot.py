from flask import Flask
import os, time
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chat WA-style</title>
<style>
body{margin:0;font-family:'Segoe UI',sans-serif;background:#f5f5f5;display:flex;flex-direction:column;height:100vh;font-size:20px}
header{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:#075e54;color:#fff;font-size:22px;font-weight:bold}
#chatbox{flex:1;padding:16px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;background:#e5ddd5}
.message{max-width:70%;padding:14px 18px;border-radius:16px;word-wrap:break-word;user-select:text;font-size:20px;line-height:1.5}
.user{background:#d0f0c0;align-self:flex-end;border-bottom-right-radius:2px}
.bot{background:#ffffff;align-self:flex-start;border-bottom-left-radius:2px}
@media screen and (max-width:480px){.message{max-width:90%}}
#inputArea{display:flex;padding:12px;background:#f0f0f0;border-top:1px solid #ccc}
#userInput{flex:1;padding:14px 16px;font-size:20px;border-radius:24px;border:1px solid #ccc;outline:none}
#sendBtn{margin-left:10px;padding:14px 18px;border:none;border-radius:50%;background:#4caf50;color:#fff;cursor:pointer;font-weight:bold;font-size:20px}
#menuBtn{font-size:26px;background:none;border:none;color:#fff;cursor:pointer}
#popupMenu{display:none;position:absolute;right:16px;top:60px;background:#fff;border-radius:10px;box-shadow:0 2px 6px rgba(0,0,0,0.25);z-index:10}
#popupMenu button{display:block;width:100%;padding:12px 16px;border:none;background:none;text-align:left;cursor:pointer;font-size:18px}
#popupMenu button:hover{background:#f1f1f1}
#modal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);align-items:center;justify-content:center;z-index:100}
#modalContent{background:#fff;border-radius:10px;padding:16px;width:90%;max-width:400px;display:flex;flex-direction:column}
#modalTextarea{flex:1;width:100%;min-height:300px;resize:vertical;font-size:20px;padding:12px;line-height:1.5;box-sizing:border-box}
#modalSaveBtn{margin-top:12px;padding:14px;width:100%;border:none;border-radius:6px;background:#075e54;color:#fff;font-size:20px;cursor:pointer;box-sizing:border-box}
</style>
</head>
<body>

<header>Chat Modern<button id="menuBtn">⋮</button></header>
<div id="popupMenu">
<button id="editBtn">✏️ Edit Data</button>
<button id="downloadBtn">💾 Download Data</button>
<button id="uploadBtn">📤 Upload Data</button>
<button id="copyBtn">📋 Copy Chat</button>
</div>

<div id="chatbox"></div>

<div id="inputArea">
<input type="text" id="userInput" placeholder="Ketik sesuatu...">
<button id="sendBtn">></button>
</div>

<input type="file" id="fileInput" accept=".json" style="display:none;">

<div id="modal">
  <div id="modalContent">
    <textarea id="modalTextarea"></textarea>
    <button id="modalSaveBtn">💾 Simpan</button>
  </div>
</div>

<script>
const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const menuBtn = document.getElementById('menuBtn');
const popupMenu = document.getElementById('popupMenu');
const fileInput = document.getElementById('fileInput');
const modal = document.getElementById('modal');
const textarea = document.getElementById('modalTextarea');
const saveBtn = document.getElementById('modalSaveBtn');

let dataset = JSON.parse(localStorage.getItem('dataset')||'{}');
let lastKey=null;

menuBtn.onclick=()=>popupMenu.style.display=popupMenu.style.display==='block'?'none':'block';
document.addEventListener('click',e=>{if(!popupMenu.contains(e.target)&&e.target!==menuBtn) popupMenu.style.display='none';});

function addMessage(sender,text){
  const div=document.createElement('div');
  div.className='message '+sender;
  div.innerText=text;
  chatbox.appendChild(div);
  chatbox.scrollTop=chatbox.scrollHeight;
}

function handleInput(){
  const text=userInput.value.trim();
  if(!text) return;
  addMessage('user',text);
  if(lastKey){
    dataset[lastKey]=text;
    localStorage.setItem('dataset',JSON.stringify(dataset));
    addMessage('bot',`Jawaban disimpan untuk: "${lastKey}"`);
    lastKey=null;
  } else {
    const lower=text.toLowerCase();
    if(dataset[lower]) addMessage('bot',dataset[lower]);
    else { lastKey=lower; addMessage('bot','Data belum ada. Apa jawabannya?'); }
  }
  userInput.value='';
}

sendBtn.onclick=handleInput;
userInput.addEventListener('keypress',e=>{if(e.key==='Enter') handleInput();});

document.getElementById('editBtn').onclick=()=>{textarea.value=JSON.stringify(dataset,null,2);modal.style.display='flex';};
saveBtn.onclick=()=>{try{dataset=JSON.parse(textarea.value);localStorage.setItem('dataset',JSON.stringify(dataset));alert('Data diperbarui!');modal.style.display='none';}catch(e){alert('Format JSON salah!');}};
modal.addEventListener('click',e=>{if(e.target===modal) modal.style.display='none';});
document.getElementById('downloadBtn').onclick=()=>{const blob=new Blob([JSON.stringify(dataset,null,2)],{type:"application/json"});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download="dataset.json";a.click();URL.revokeObjectURL(url);};
document.getElementById('uploadBtn').onclick=()=>fileInput.click();
fileInput.addEventListener('change',e=>{const file=e.target.files[0];const reader=new FileReader();reader.onload=function(ev){try{dataset=JSON.parse(ev.target.result);localStorage.setItem('dataset',JSON.stringify(dataset));alert('Upload berhasil!');}catch(err){alert('File bukan JSON valid.');}};reader.readAsText(file);});
document.getElementById('copyBtn').onclick=()=>{let msgs=[...chatbox.querySelectorAll('.message')].map(m=>m.classList.contains('user')?"👤 "+m.innerText:m.classList.contains('bot')?"🤖 "+m.innerText:m.innerText).join("\\n\\n");navigator.clipboard.writeText(msgs).then(()=>alert("Percakapan disalin!")).catch(()=>alert("Gagal menyalin."));};

addMessage('bot','Apa yang bisa saya bantu?');
</script>
</body>
</html>
"""

if __name__=="__main__":
    # Jalankan Flask di thread terpisah
    t = Thread(target=lambda: app.run(host="127.0.0.1",port=5000,debug=False,use_reloader=False))
    t.start()
    time.sleep(2)
    # buka browser Android
    os.system('am start -a android.intent.action.VIEW -d "http://127.0.0.1:5000"')
    t.join()