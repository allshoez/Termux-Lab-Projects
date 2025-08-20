// server.js
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3000;

// ===== Middleware =====
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname))); // buat akses file statis

// ===== Upload setup =====
const uploadFolder = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadFolder)) fs.mkdirSync(uploadFolder);

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadFolder),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    const name = Date.now() + '-' + Math.round(Math.random()*1e6);
    cb(null, name + ext);
  }
});
const upload = multer({ storage });

// ===== Routes =====

// Tes server
app.get('/', (req, res) => res.send('CatBot Server aktif!'));

// Upload media (foto / file / kamera)
app.post('/api/upload', upload.single('file'), (req, res) => {
  if(!req.file) return res.status(400).json({error:'File kosong'});
  
  // Path file untuk frontend
  const fileUrl = `/uploads/${req.file.filename}`;
  
  // Contoh reply AI dummy
  let reply = '(AI) Terima kasih file diterima: ' + req.file.originalname;
  
  // Bisa dihubungkan ke Gemini API di sini jika mau
  res.json({ fileUrl, reply });
});

// Biar file uploads bisa diakses frontend
app.use('/uploads', express.static(uploadFolder));

// Start server
app.listen(PORT, () => console.log(`Server CatBot jalan di http://localhost:${PORT}`));