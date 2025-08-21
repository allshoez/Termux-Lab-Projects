
from flask import Flask, send_from_directory, jsonify
import os
import time
from threading import Thread

app = Flask(__name__)

VIDEOS_DIR = os.path.join(os.path.dirname(__file__), "videos")

# API: scan semua mp4 di subfolder
@app.route("/api/videos")
def api_videos():
    video_list = []
    for root, dirs, files in os.walk(VIDEOS_DIR):
        for file in files:
            if file.lower().endswith(".mp4"):
                rel_path = os.path.relpath(os.path.join(root, file), VIDEOS_DIR).replace("\\","/")
                video_list.append(rel_path)
    return jsonify(video_list)

# serve file video
@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)

# Halaman index
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mini Shorts Offline</title>
<style>
body,html{margin:0;padding:0;height:100%;background:#000;color:#fff;font-family:Arial;overflow:hidden;}
#menu{position:absolute;top:0;width:100%;display:flex;justify-content:center;background:rgba(0,0,0,0.6);z-index:10;padding:5px 0;}
#menu button{margin:0 5px;padding:5px 10px;background:#555;border:none;color:#fff;cursor:pointer;}
#menu button.active{background:#f00;}
.short-container{width:100%;height:100%;position:relative;margin-top:40px;}
video{width:100%;height:100%;object-fit:cover;}
.overlay{position:absolute;bottom:80px;left:10px;color:#fff;font-size:18px;max-width:65%;text-shadow:1px 1px 5px #000;}
.controls{position:absolute;bottom:80px;right:10px;display:flex;flex-direction:column;gap:15px;color:#fff;font-size:14px;text-shadow:1px 1px 5px #000;text-align:center;}
.playPause{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:50px;color:rgba(255,255,255,0.7);display:none;cursor:pointer;}
</style>
</head>
<body>
<div id="menu"></div>
<div class="short-container">
  <video id="shortVideo" autoplay muted playsinline></video>
  <div class="overlay" id="videoTitle"></div>
  <div class="controls">
    <div>❤️ <span id="likes">100</span></div>
    <div>💬 <span id="comments">20</span></div>
    <div>🔗 Share</div>
  </div>
  <div class="playPause" id="playPauseBtn">▶️</div>
</div>
<script>
let videos=[],allVideos={},index=0,currentCategory="";
const videoEl=document.getElementById('shortVideo');
const titleEl=document.getElementById('videoTitle');
const likesEl=document.getElementById('likes');
const commentsEl=document.getElementById('comments');
const playPauseBtn=document.getElementById('playPauseBtn');
const menuEl=document.getElementById('menu');

fetch('/api/videos').then(res=>res.json()).then(list=>{
    allVideos={};
    list.forEach(f=>{
        const parts=f.split('/');
        const cat=parts[0];
        const file=parts.slice(1).join('/');
        if(!allVideos[cat]) allVideos[cat]=[];
        allVideos[cat].push({
            src:'/videos/'+f,    // fix path
            title:file.replace(/\.mp4$/i,''),
            likes:Math.floor(Math.random()*200+50),
            comments:Math.floor(Math.random()*50+5)
        });
    });
    const categoryOrder=Object.keys(allVideos);
    categoryOrder.forEach((cat,idx)=>{
        const btn=document.createElement('button');
        btn.textContent=cat;
        if(idx===0) btn.classList.add('active');
        btn.onclick=()=>switchCategory(cat,btn);
        menuEl.appendChild(btn);
    });
    currentCategory=categoryOrder[0];
    videos=allVideos[currentCategory];
    loadVideo(0);
});

function switchCategory(cat,btnClicked){
    currentCategory=cat;
    videos=allVideos[cat];
    index=0;
    menuEl.querySelectorAll('button').forEach(b=>b.classList.remove('active'));
    btnClicked.classList.add('active');
    loadVideo(index);
}

function loadVideo(i){
    if(videos.length===0) return;
    const vid=videos[i];
    videoEl.src=vid.src;
    titleEl.textContent=vid.title;
    likesEl.textContent=vid.likes;
    commentsEl.textContent=vid.comments;
    videoEl.play();
}

// autoplay next
videoEl.addEventListener('ended',()=>{ index=(index+1)%videos.length; loadVideo(index); });
// pause/play overlay
videoEl.addEventListener('click',()=>{ if(videoEl.paused){videoEl.play();playPauseBtn.style.display='none';} else{videoEl.pause();playPauseBtn.style.display='block';} });
playPauseBtn.addEventListener('click',()=>{videoEl.play();playPauseBtn.style.display='none';});
// swipe up/down
let startY=0;
videoEl.addEventListener('touchstart',e=>{startY=e.touches[0].clientY;});
videoEl.addEventListener('touchend',e=>{
    let endY=e.changedTouches[0].clientY;
    if(startY-endY>50){ index=(index+1)%videos.length; loadVideo(index);}
    else if(endY-startY>50){ index=(index-1+videos.length)%videos.length; loadVideo(index);}
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    def run_flask():
        app.run(host="127.0.0.1", port=5000)

    t = Thread(target=run_flask)
    t.start()
    time.sleep(2)  # tunggu server siap
    os.system('am start -a android.intent.action.VIEW -d "http://127.0.0.1:5000" com.android.chrome')
    t.join()


