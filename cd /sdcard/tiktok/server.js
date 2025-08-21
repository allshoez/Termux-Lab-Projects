const fs = require('fs');
const path = require('path');
const express = require('express');

const app = express();
const PORT = 3000;

const videosFolder = path.join(__dirname, 'videos');
const outputFile = path.join(__dirname, 'videos.js');

function scanVideos() {
  let allVideos = {};
  if (!fs.existsSync(videosFolder)) return;

  const categories = fs.readdirSync(videosFolder)
    .filter(f => fs.statSync(path.join(videosFolder, f)).isDirectory());

  categories.forEach(cat => {
    const catPath = path.join(videosFolder, cat);
    const files = fs.readdirSync(catPath)
      .filter(f => f.toLowerCase().endsWith('.mp4'));

    if (files.length) {
      allVideos[cat] = files.map(f => ({
        src: `videos/${cat}/${f}`,
        title: f.split('.').slice(0, -1).join('.')
      }));
    }
  });

  fs.writeFileSync(outputFile, `const allVideos = ${JSON.stringify(allVideos, null, 2)};`, 'utf-8');
  console.log(`${outputFile} updated!`);
}

// Scan folder videos dan generate videos.js
scanVideos();

// serve semua file statis
app.use(express.static(__dirname));

// start server di semua interface supaya bisa diakses dari IP lokal / 127.0.0.1
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${PORT}`);
});