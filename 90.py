import sys
import subprocess
import random
import requests
import socket
import base64
import json
import uuid
import string
import time
from ipaddress import ip_network

# ================== STYLING ==================
OKGREEN = '\033[92m'
WARNING = '\033[0;33m'
FAIL = '\033[91m'
ENDC = '\033[0m'
LITBU = '\033[94m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
BOLD = '\033[1m'

colors = [OKGREEN, LITBU, CYAN, PURPLE]
RAND_COLOR = random.choice(colors)

BANNER = f"""
{RAND_COLOR}
{OKGREEN}╔════════════════════════════════════════════════════════════════════════╗
║                    {BOLD}ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 🍏🧑‍💻🌿💀{ENDC}{OKGREEN}                              ║
║                  IP Range Scanner and Config Gen -  Made by Ayhan Mansur                   ║
╚════════════════════════════════════════════════════════════════════════╝{ENDC}
"""

SCAN_LIMIT = 120000
DEFAULT_PORTS = [22, 80, 443, 8080, 8443, 3306, 5432, 3389, 5900]

# ================== Helper functions ==================
def random_uuid():
    return str(uuid.uuid4())

def random_password(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def download_list(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        lines = [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith('#')]
        return lines
    except Exception as e:
        print(f"{FAIL}❌ Failed to download from {url}: {e}{ENDC}")
        return []

def scan_host(ip):
    param = '-n' if sys.platform.startswith('win') else '-c'
    try:
        result = subprocess.run(['ping', param, '1', str(ip)],
                                capture_output=True, text=True, timeout=2)
        return result.returncode == 0
    except:
        return False

def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports_on_ip(ip, ports):
    open_ports = []
    for port in ports:
        if scan_port(ip, port):
            open_ports.append(port)
            print(f"   {OKGREEN}🔓 Port {port} open on {ip}{ENDC}")
    return open_ports

def scan_network(network_str, scanned_so_far, ports_to_scan):
    try:
        network = ip_network(network_str, strict=False)
        remaining = SCAN_LIMIT - scanned_so_far
        addresses = list(network.hosts())
        if len(addresses) > remaining:
            addresses = addresses[:remaining]
            print(f"{WARNING}⚠️ Limit reached: scanning only {remaining} of {len(network.hosts())} addresses in {network_str}{ENDC}")

        color = random.choice(colors)
        print(f"{color}🔍 Scanning {network_str} ({len(addresses)} addresses, total scanned so far: {scanned_so_far + len(addresses)}/{SCAN_LIMIT})...{ENDC}")

        results = {}
        for ip in addresses:
            ip_str = str(ip)
            if scan_host(ip_str):
                print(f"{OKGREEN}   ✅ {ip_str} is active{ENDC}")
                open_ports = scan_ports_on_ip(ip_str, ports_to_scan)
                if open_ports:
                    results[ip_str] = open_ports
            # تأخیر ۲ ثانیه
            time.sleep(2)
        return results, len(addresses)
    except Exception as e:
        print(f"{FAIL}❌ Error in range {network_str}: {e}{ENDC}")
        return {}, 0

# ================== Config generators for V2Ray ==================
def generate_vless_config(ip, port, sni_domain):
    uid = random_uuid()
    return f"vless://{uid}@{ip}:{port}?security=none&encryption=none&type=tcp&sni={sni_domain}#AyhanX_{ip}_{port}"

def generate_trojan_config(ip, port, sni_domain):
    pw = random_password()
    return f"trojan://{pw}@{ip}:{port}?sni={sni_domain}#AyhanX_{ip}_{port}"

def generate_vmess_config(ip, port, sni_domain):
    uid = random_uuid()
    config = {
        "v": "2",
        "ps": f"AyhanX_{ip}_{port}",
        "add": ip,
        "port": port,
        "id": uid,
        "aid": "0",
        "net": "tcp",
        "type": "none",
        "tls": "",
        "sni": sni_domain
    }
    json_str = json.dumps(config, separators=(',', ':'))
    encoded = base64.b64encode(json_str.encode()).decode()
    return f"vmess://{encoded}"

# ================== MAIN ==================
def main():
    print(BANNER)

    start_choice = input(f"{CYAN}❓ Do you want to start scan? [Y/n]: {ENDC}").strip().lower()
    if start_choice == 'n':
        print(f"{YELLOW}🚫 Scan cancelled by user.{ENDC}")
        sys.exit(0)

    # *** اصلاح لینک‌ها به raw ***
    ranges_url = "https://raw.githubusercontent.com/AyhanMansur/ZQ-Xray/main/%E2%84%A4%E2%84%9A-%F0%9D%95%8F%F0%9D%95%A3%F0%9D%95%92%F0%9D%95%AA/cf.rages.txt"
    print(f"{LITBU}📡 Downloading IP ranges from GitHub...{ENDC}")
    ranges = download_list(ranges_url)
    if not ranges:
        print(f"{FAIL}❌ No IP ranges found. Exiting.{ENDC}")
        sys.exit(1)
    print(f"{OKGREEN}✅ Downloaded {len(ranges)} IP ranges.{ENDC}")

    # لینک sni.txt هم باید raw باشد
    sni_url = "https://raw.githubusercontent.com/AyhanMansur/QZ-Scanner/refs/heads/main/%E2%84%9A%E2%84%A4-%F0%9D%95%8A%F0%9D%95%94%F0%9D%95%92%F0%9D%95%9F%F0%9D%95%9F%F0%9D%95%96%F0%9D%95%A3%20%F0%9F%8D%8F%F0%9F%A7%91%E2%80%8D%F0%9F%92%BB%F0%9F%8C%BF/sni.txt"
    print(f"{LITBU}📡 Downloading SNI list from GitHub...{ENDC}")
    sni_list = download_list(sni_url)
    if not sni_list:
        print(f"{FAIL}❌ No SNI found. Using default (www.google.com).{ENDC}")
        sni_list = ["www.google.com"]
    print(f"{OKGREEN}✅ Downloaded {len(sni_list)} SNI domains.{ENDC}")

    ports_input = input(f"{CYAN}Enter ports to scan (comma-separated, e.g., 22,80,443,8080) or press Enter for default: {ENDC}").strip()
    if ports_input:
        try:
            ports = [int(p.strip()) for p in ports_input.split(',')]
        except:
            print(f"{FAIL}Invalid port list. Using defaults.{ENDC}")
            ports = DEFAULT_PORTS
    else:
        ports = DEFAULT_PORTS

    print(f"{WARNING}⚠️ Scan limit: {SCAN_LIMIT} addresses (2 sec delay per IP){ENDC}")
    print(f"{LITBU}🚀 Starting IP and port scan...{ENDC}\n")

    all_results = {}
    scanned_so_far = 0
    processed_ranges = 0

    for r in ranges:
        if scanned_so_far >= SCAN_LIMIT:
            print(f"{WARNING}⚠️ Scan limit reached ({SCAN_LIMIT} addresses). Stopping...{ENDC}")
            break
        processed_ranges += 1
        results, scanned = scan_network(r, scanned_so_far, ports)
        all_results.update(results)
        scanned_so_far += scanned

    print(f"\n{BOLD}{OKGREEN}📊 Final Summary (IP + Port Scan):{ENDC}")
    print(f"{CYAN}   ➤ IP ranges processed: {processed_ranges}{ENDC}")
    print(f"{CYAN}   ➤ Addresses scanned (ping): {scanned_so_far}{ENDC}")
    total_active = len(all_results)
    print(f"{OKGREEN}   ➤ Active hosts with open ports: {total_active}{ENDC}")

    if not all_results:
        print(f"{YELLOW}No active hosts with open ports found. Exiting.{ENDC}")
        return

    print(f"\n{YELLOW}📝 Active hosts and open ports:{ENDC}")
    for ip, open_ports in all_results.items():
        print(f"   {OKGREEN}► {ip}: {', '.join(map(str, open_ports))}{ENDC}")

    print(f"\n{CYAN}Select protocol for V2Ray config generation:{ENDC}")
    print("1. vless")
    print("2. trojan")
    print("3. vmess")
    proto_choice = input(f"{CYAN}Enter choice (1/2/3): {ENDC}").strip()
    while proto_choice not in ['1','2','3']:
        proto_choice = input(f"{FAIL}Invalid. Enter 1,2,3: {ENDC}").strip()

    configs = []
    for ip, ports_list in all_results.items():
        for port in ports_list:
            chosen_sni = random.choice(sni_list)
            if proto_choice == '1':
                configs.append(generate_vless_config(ip, port, chosen_sni))
            elif proto_choice == '2':
                configs.append(generate_trojan_config(ip, port, chosen_sni))
            else:
                configs.append(generate_vmess_config(ip, port, chosen_sni))

    print(f"\n{BOLD}{OKGREEN}📝 Generated V2Ray Configurations (ready to use):{ENDC}")
    for cfg in configs:
        print(f"   {OKGREEN}► {cfg}{ENDC}")

    save_choice = input(f"\n{CYAN}Save configs to file? [y/N]: {ENDC}").strip().lower()
    if save_choice == 'y':
        filename = f"ayhanx_v2ray_configs_{random.randint(1000,9999)}.txt"
        with open(filename, 'w') as f:
            f.write("\n".join(configs))
        print(f"{OKGREEN}✅ Saved to {filename}{ENDC}")

if __name__ == "__main__":
    main()
