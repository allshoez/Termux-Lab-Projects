// ===== Utils =====
const $ = s => document.querySelector(s);
const chatEl = $('#chat'), promptEl = $('#prompt');

// ===== State =====
const state = {
  provider: 'gemini',
  system: '',
  history: [],
  gemini: { key:'', model:'gemini-1.5-flash', temperature: 1 },
  openai: { key:'', model:'gpt-4o-mini', temperature: 1 },
};

// ===== Local Storage =====
function saveLocal(){
  localStorage.setItem('catbot_settings', JSON.stringify({
    provider: state.provider,
    system: state.system,
    gemini: state.gemini,
    openai: state.openai
  }));
  updateBadges();
}

function loadLocal(){
  const raw = localStorage.getItem('catbot_settings');
  if(!raw) return;
  try{
    const s = JSON.parse(raw);
    state.provider = s.provider ?? state.provider;
    state.system = s.system ?? '';
    state.gemini = Object.assign(state.gemini, s.gemini||{});
    state.openai = Object.assign(state.openai, s.openai||{});
  }catch(e){}
  $('#providerSel').value = state.provider;
  $('#systemPrompt').value = state.system || '';
  $('#geminiKey').value = state.gemini.key || '';
  $('#geminiModel').value = state.gemini.model || 'gemini-1.5-flash';
  $('#gemTemp').value = state.gemini.temperature ?? 1;
  $('#openaiKey').value = state.openai.key || '';
  $('#openaiModel').value = state.openai.model || 'gpt-4o-mini';
  $('#oaTemp').value = state.openai.temperature ?? 1;
  updateBadges();
}

function updateBadges(){
  $('#providerBadge').textContent = state.provider==='gemini'?'Gemini':'OpenAI';
  $('#status').textContent = 'online';
}

// ===== Popup Toggle =====
const popup = $('#popup');
$('#openPopup').onclick = () => popup.classList.add('active');
$('#closePopup').onclick = () => popup.classList.remove('active');
popup.addEventListener('click', e => { if(e.target===popup) popup.classList.remove('active'); });

const mediaPopup = $('#mediaPopup');
$('#btnClear').onclick = () => mediaPopup.classList.add('active');
document.querySelectorAll('.closePopup').forEach(btn => btn.onclick = () => mediaPopup.classList.remove('active'));
mediaPopup.addEventListener('click', e => { if(e.target===mediaPopup) mediaPopup.classList.remove('active'); });

// ===== Save / Wipe =====
$('#btnSave').onclick = () => {
  state.provider = $('#providerSel').value;
  state.system = $('#systemPrompt').value.trim();
  state.gemini.key = $('#geminiKey').value.trim();
  state.gemini.model = $('#geminiModel').value;
  state.gemini.temperature = parseFloat($('#gemTemp').value)||1;
  state.openai.key = $('#openaiKey').value.trim();
  state.openai.model = $('#openaiModel').value;
  state.openai.temperature = parseFloat($('#oaTemp').value)||1;

  if(state.provider==='openai' && !state.openai.key){
    return toast('❌ OpenAI API key kosong!');
  }
  if(state.provider==='gemini' && !state.gemini.key){
    return toast('❌ Gemini API key kosong!');
  }

  saveLocal();
  toast('Disimpan ✅');
  popup.classList.remove('active');
};

$('#btnWipe').onclick = () => {
  if(!confirm('Hapus semua setelan lokal?')) return;
  localStorage.removeItem('catbot_settings');
  location.reload();
};

// ===== Provider Toggle =====
$('#providerBadge').onclick = () => {
  state.provider = (state.provider==='gemini'?'openai':'gemini');
  saveLocal();
  toast('Provider: '+(state.provider==='gemini'?'Gemini':'OpenAI'));
};

// ===== Chat Functions =====
function addMsg(role, content, type='text'){
  const wrap = document.createElement('div');
  wrap.className = 'msg ' + (role==='user'?'user':'bot');

  if(type === 'text') wrap.innerHTML = content;
  else if(type==='image'){
    const img = document.createElement('img');
    img.src = content;
    img.className = 'preview';
    wrap.appendChild(img);
  } else if(type==='file'){
    const a = document.createElement('a');
    a.href = content;
    a.textContent = content.split('/').pop();
    a.target='_blank';
    a.className='fileLink';
    wrap.appendChild(a);
  }

  const copyBtn = document.createElement('button');
  copyBtn.className='copyBtn';
  copyBtn.textContent='📋';
  copyBtn.onclick=()=>{ if(type==='text') navigator.clipboard.writeText(content); else alert('Hanya teks bisa dicopy'); };
  wrap.appendChild(copyBtn);

  const meta = document.createElement('div');
  meta.className='meta';
  meta.textContent = new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
  wrap.appendChild(meta);

  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function escapeHtml(s){return (s+'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}

// ===== Event Listeners =====
$('#btnSend').onclick = onSubmit;
promptEl.addEventListener('keydown', e => { if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); onSubmit(); } });
$('#btnClearChat').onclick = () => { chatEl.innerHTML=''; state.history=[]; mediaPopup.classList.remove('active'); };

// ===== AI Call =====
async function onSubmit(){
  const text = promptEl.value.trim();
  if(!text) return;
  promptEl.value = '';
  addMsg('user', text);
  state.history.push({role:'user', content:text});
  addMsg('assistant', '⏳ sedang mengetik...');

  try{
    let reply;
    if(state.provider==='gemini'){
      if(!state.gemini.key) throw new Error('Gemini API key kosong!');
      reply = await callGemini(text);
    } else {
      if(!state.openai.key) throw new Error('OpenAI API key kosong!');
      reply = await callOpenAI(text);
    }
    chatEl.removeChild(chatEl.lastElementChild);
    addMsg('assistant', reply);
    state.history.push({role:'assistant', content:reply});
  }catch(err){
    chatEl.removeChild(chatEl.lastElementChild);
    addMsg('assistant', '❌ '+(err?.message||err));
  }
}

// ===== Gemini API =====
async function callGemini(prompt){
  const {key, model, temperature} = state.gemini;
  const tail = state.history.slice(-8).map(m=>({ role: m.role==='assistant'?'model':'user', parts:[{text:m.content}] }));
  const body = { contents: tail.concat([{role:'user', parts:[{text:prompt}]}]), generationConfig:{temperature} };
  if(state.system) body.systemInstruction={role:'user', parts:[{text: state.system}]};
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(key)}`;
  const res = await fetch(url,{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  const data = await res.json();
  if(!res.ok) throw new Error(data?.error?.message || `Gemini ${res.status}`);
  return data?.candidates?.[0]?.content?.parts?.map(p=>p.text).join('')?.trim() || '(kosong)';
}

// ===== OpenAI API =====
async function callOpenAI(prompt){
  const {key, model, temperature} = state.openai;
  const msgs = [];
  if(state.system) msgs.push({role:'system', content:state.system});
  for(const m of state.history.slice(-12)) msgs.push({role:m.role, content:m.content});
  msgs.push({role:'user', content:prompt});
  const res = await fetch('https://api.openai.com/v1/chat/completions',{
    method:'POST',
    headers:{'Content-Type':'application/json','Authorization':`Bearer ${key}`},
    body:JSON.stringify({ model, messages: msgs, temperature })
  });
  const data = await res.json();
  if(!res.ok) throw new Error(data?.error?.message || `OpenAI ${res.status}`);
  return (data?.choices?.[0]?.message?.content || '').trim() || '(kosong)';
}

// ===== Toast =====
function toast(txt){
  const el = document.createElement('div');
  el.textContent = txt;
  el.style.cssText = 'position:fixed;left:50%;bottom:84px;transform:translateX(-50%);background:#0b2a3a;color:#c9eaff;border:1px solid #124a63;padding:10px 14px;border-radius:10px;z-index:60;box-shadow:0 10px 30px rgba(0,0,0,.4);font-size:13px';
  document.body.appendChild(el); 
  setTimeout(()=>el.remove(),1500);
}

// ===== Media Handler =====
function handleFileInput(accept, capture=false, type='file'){
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = accept;
  if(capture) input.capture = 'environment';

  input.onchange = () => {
    const file = input.files[0];
    if(!file) return;
    const url = URL.createObjectURL(file);
    addMsg('user', url, type);
    sendToAI(file, type);
  }
  input.click();
}

document.getElementById('btnCamera').onclick = () => handleFileInput('image/*', true, 'image');
document.getElementById('btnPhoto').onclick = () => handleFileInput('image/*', false, 'image');
document.getElementById('btnFile').onclick = () => handleFileInput('*/*', false, 'file');

async function sendToAI(file, type){
  const formData = new FormData();
  formData.append('file', file);
  formData.append('type', type);
  try{
    const res = await fetch('/api/upload', { method:'POST', body: formData });
    const data = await res.json();
    addMsg('assistant', data.reply);
  }catch(e){
    addMsg('assistant', '❌ Gagal kirim file ke AI');
  }
}

// ===== Init =====
loadLocal();