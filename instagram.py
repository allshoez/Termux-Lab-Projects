from flask import Flask, send_from_directory, jsonify
import os
import socket
from threading import Thread

app = Flask(__name__)
VIDEOS_DIR = "/sdcard/tiktok/videos"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

@app.route("/api/videos")
def api_videos():
    video_list = []
    for root, dirs, files in os.walk(VIDEOS_DIR):
        for file in files:
            if file.lower().endswith(".mp4"):
                rel_path = os.path.relpath(os.path.join(root, file), VIDEOS_DIR).replace("\\","/")
                video_list.append(rel_path)
    return jsonify(video_list)

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(VIDEOS_DIR, filename)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mini Shorts Grid Final</title>
<style>
body,html{margin:0;padding:0;background:#000;color:#fff;font-family:Arial;}
.grid-container{display:grid;grid-template-columns:1fr 1fr;gap:2px;overflow-y:auto;height:100vh;}
.grid-container video{width:100%;height:200px;object-fit:cover;cursor:pointer;background:#111;}
.fullscreen-container{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000;z-index:999;overflow-y:auto;}
.fullscreen-video{width:100%;height:80vh;object-fit:cover;margin:10px 0;}
.mute-btn{position:fixed;top:10px;right:10px;font-size:28px;color:#fff;z-index:1000;cursor:pointer;}
.close-btn{position:fixed;top:10px;left:10px;font-size:28px;color:#fff;z-index:1000;cursor:pointer;}
.pause-overlay{
    position:fixed;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:60px;
    color:rgba(255,255,255,0.8);
    display:none;
    z-index:1001;
    text-align:center;
    background: rgba(0,0,0,0.2);
    padding:20px;
    border-radius:20px;
    transition: opacity 0.3s ease;
}
</style>
</head>
<body>
<div class="grid-container" id="gridContainer"></div>

<div class="fullscreen-container" id="fsContainer">
  <div class="mute-btn" id="muteBtn">🔊</div>
  <div class="close-btn" id="closeBtn">❌</div>
  <div id="fsVideosWrapper"></div>
</div>

<div class="pause-overlay" id="pauseOverlay">⏸</div>

<script>
let videos=[];
const gridContainer = document.getElementById('gridContainer');
const fsContainer = document.getElementById('fsContainer');
const fsVideosWrapper = document.getElementById('fsVideosWrapper');
const muteBtn = document.getElementById('muteBtn');
const closeBtn = document.getElementById('closeBtn');
const pauseOverlay = document.getElementById('pauseOverlay');
let isMuted = false;
let currentPlaying = null;
let fullscreenActive = false;

// Load video grid
fetch('/api/videos').then(res=>res.json()).then(list=>{
    videos = list;
    list.forEach(file=>{
        const vid = document.createElement('video');
        vid.src = '/videos/'+file;
        vid.controls = false;
        vid.autoplay = false;
        vid.muted = true;
        gridContainer.appendChild(vid);

        vid.onclick = ()=>{
            openFullscreen(fsContainer);
            fsVideosWrapper.innerHTML = '';
            videos.forEach(f=>{
                const fsVid = document.createElement('video');
                fsVid.src = '/videos/'+f;
                fsVid.autoplay = false;
                fsVid.muted = isMuted;
                fsVid.className = 'fullscreen-video';
                fsVid.playsInline = true;
                fsVideosWrapper.appendChild(fsVid);

                fsVid.addEventListener('click',()=>{
                    if(fsVid.paused){
                        playVideo(fsVid);
                        pauseOverlay.style.display='none';
                    } else {
                        fsVid.pause();
                        pauseOverlay.style.display='block';
                        pauseOverlay.style.opacity='1';
                        setTimeout(()=>{pauseOverlay.style.opacity='0';},300);
                    }
                });
            });
            fsContainer.style.display='block';
            fullscreenActive = true;
            history.pushState({fullscreen:true},"");

            // Play video yang di-tap
            const firstVideo = fsVideosWrapper.querySelector('video[src="'+vid.src+'"]');
            if(firstVideo){
                firstVideo.scrollIntoView({behavior:'auto'});
                playVideo(firstVideo);
            }
        }
    });
});

// Close fullscreen
closeBtn.addEventListener('click',(e)=>{
    e.stopPropagation();
    closeFullscreen();
});

function closeFullscreen(){
    fsContainer.style.display='none';
    fullscreenActive = false;
    if(currentPlaying) currentPlaying.pause();
    if(history.state && history.state.fullscreen) history.back();
}

// Mute/unmute fullscreen
muteBtn.addEventListener('click',(e)=>{
    e.stopPropagation();
    isMuted = !isMuted;
    muteBtn.textContent = isMuted ? '🔇':'🔊';
    if(currentPlaying) currentPlaying.muted = isMuted;
});

// Play video
function playVideo(vid){
    if(currentPlaying && currentPlaying!==vid) currentPlaying.pause();
    currentPlaying = vid;
    vid.play();
    vid.muted = isMuted;
}

// Scroll grid berat
gridContainer.addEventListener('wheel',(e)=>{
    e.preventDefault();
    gridContainer.scrollBy({top:e.deltaY*1.5});
},{passive:false});

// Scroll fullscreen → video terlihat
fsContainer.addEventListener('scroll',()=>{
    const fsVideos = Array.from(fsVideosWrapper.querySelectorAll('video'));
    let viewportHeight = window.innerHeight;
    for(let v of fsVideos){
        let rect = v.getBoundingClientRect();
        if(rect.top >=0 && rect.top < viewportHeight/2){
            playVideo(v);
            break;
        }
    }
});

// Scroll fullscreen berat
fsContainer.addEventListener('wheel',(e)=>{
    e.preventDefault();
    fsContainer.scrollBy({top:e.deltaY*1.2});
},{passive:false});

// Back Android/browser
window.addEventListener('popstate', (event) => {
    if(fullscreenActive){
        closeFullscreen();
    }
});

// Fullscreen API immersive
function openFullscreen(elem){
    if(elem.requestFullscreen){ elem.requestFullscreen(); }
    else if(elem.webkitRequestFullscreen){ elem.webkitRequestFullscreen(); }
    else if(elem.msRequestFullscreen){ elem.msRequestFullscreen(); }
}

// Visibility change: pause/play fullscreen dengan animasi
document.addEventListener('visibilitychange', () => {
    if(fullscreenActive && currentPlaying){
        if(document.hidden){
            currentPlaying.pause();
            pauseOverlay.style.display='block';
            pauseOverlay.style.opacity='1';
            setTimeout(()=>{pauseOverlay.style.opacity='0';},300);
        } else {
            currentPlaying.play();
            pauseOverlay.style.display='none';
        }
    }
});
</script>
</body>
</html>
"""

def run_flask():
    ip = get_local_ip()
    print(f"Server running at http://{ip}:5000")
    os.system(f'am start -a android.intent.action.VIEW -d "http://{ip}:5000" com.android.chrome')
    app.run(host=ip, port=5000)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
