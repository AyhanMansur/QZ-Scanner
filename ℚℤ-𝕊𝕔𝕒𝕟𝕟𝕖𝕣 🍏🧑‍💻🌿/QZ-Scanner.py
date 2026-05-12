import sys
import subprocess
import random
import requests
from ipaddress import ip_network

# کدهای رنگی
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
LITBU = '\033[94m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
PURPLE = '\033[95m'
BOLD = '\033[1m'

colors = [OKGREEN, LITBU, CYAN, PURPLE]

def print_banner():
    """چاپ بنر بدون استفاده از f-string طولانی"""
    print()
    print(random.choice(colors) + "▄████  ███▄ ▄███▓ ▄▄▄       ██▓ ██▓     ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀" + ENDC)
    print(random.choice(colors) + "██▒ ▀█▒▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    ▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒" + ENDC)
    print(random.choice(colors) + "▒██░▄▄▄░▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░" + ENDC)
    print(random.choice(colors) + "░▓█  ██▓▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄" + ENDC)
    print(random.choice(colors) + "░▒▓███▀▒▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄" + ENDC)
    print(random.choice(colors) + " ░▒   ▒ ░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒" + ENDC)
    print(random.choice(colors) + "  ░   ░ ░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░ ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░" + ENDC)
    print(random.choice(colors) + "░ ░   ░ ░      ░     ░   ▒    ▒ ░  ░ ░    ░  ░░ ░  ░   ▒   ░        ░ ░░ ░" + ENDC)
    print("      ░        ░         ░  ░ ░      ░  ░ ░  ░  ░      ░  ░░ ░      ░  ░" + ENDC)
    print(OKGREEN + "╔════════════════════════════════════════════════════════════════════════╗" + ENDC)
    print(OKGREEN + "║                    " + BOLD + "ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 🍏🧑‍💻🌿💀" + ENDC + OKGREEN + "                              ║" + ENDC)
    print(OKGREEN + "║                  Advanced IP Range Scanner - Ayhan Mansur                   ║" + ENDC)
    print(OKGREEN + "╚════════════════════════════════════════════════════════════════════════╝" + ENDC + ENDC)

SCAN_LIMIT = 120000

def scan_host(ip):
    """بررسی فعال بودن یک IP با پینگ"""
    param = '-n' if sys.platform.startswith('win') else '-c'
    try:
        result = subprocess.run(['ping', param, '1', str(ip)],
                                capture_output=True, text=True, timeout=2)
        return result.returncode == 0
    except:
        return False

def scan_network(network_str, scanned_count):
    """اسکن شبکه با رعایت محدودیت"""
    try:
        network = ip_network(network_str, strict=False)
        remaining = SCAN_LIMIT - scanned_count
        addresses = list(network.hosts())
        
        if len(addresses) > remaining:
            addresses = addresses[:remaining]
            print(WARNING + "⚠️ Limit reached: scanning only " + str(remaining) + " of " + str(len(network.hosts())) + " addresses in " + network_str + ENDC)
        
        color = random.choice(colors)
        print(color + "🔍 Scanning " + network_str + " (" + str(len(addresses)) + " addresses, total scanned so far: " + str(scanned_count + len(addresses)) + "/" + str(SCAN_LIMIT) + ")..." + ENDC)
        
        active_hosts = []
        for ip in addresses:
            if scan_host(ip):
                active_hosts.append(str(ip))
                print(OKGREEN + "   ✅ " + str(ip) + " is active" + ENDC)
        
        return active_hosts, len(addresses)
    except Exception as e:
        print(FAIL + "❌ Error in range " + network_str + ": " + str(e) + ENDC)
        return [], 0

def main():
    print_banner()
    
    # پرسش شروع اسکن
    start_choice = input(CYAN + "❓ Do you want to start scan? [Y/n]: " + ENDC).strip().lower()
    if start_choice == 'n':
        print(YELLOW + "🚫 Scan cancelled by user." + ENDC)
        sys.exit(0)
    
    # لینک مستقیم فایل
    url = "https://raw.githubusercontent.com/AyhanMansur/QZ-Scanner/refs/heads/main/%E2%84%9A%E2%84%A4-%F0%9D%95%8A%F0%9D%95%94%F0%9D%95%92%F0%9D%95%9F%F0%9D%95%9F%F0%9D%95%96%F0%9D%95%A3%20%F0%9F%8D%8F%F0%9F%A7%91%E2%80%8D%F0%9F%92%BB%F0%9F%8C%BF/Ranges.txt"
    
    print(LITBU + "📡 ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 - Downloading range list from GitHub..." + ENDC)
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(FAIL + "❌ Failed to download ranges.txt: " + str(e) + ENDC)
        sys.exit(1)
    
    ranges = []
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            ranges.append(line)
    
    if not ranges:
        print(FAIL + "❌ No IP ranges found in the downloaded file." + ENDC)
        sys.exit(1)
    
    print(OKGREEN + "✅ Downloaded " + str(len(ranges)) + " IP ranges." + ENDC)
    print(YELLOW + "⚠️ Scan limit: " + str(SCAN_LIMIT) + " addresses" + ENDC)
    print(LITBU + "🚀 Starting scan..." + ENDC + "\n")
    
    all_active = []
    scanned_so_far = 0
    processed_ranges = 0
    
    for r in ranges:
        if scanned_so_far >= SCAN_LIMIT:
            print(WARNING + "⚠️ Scan limit reached (" + str(SCAN_LIMIT) + " addresses). Stopping..." + ENDC)
            break
        processed_ranges += 1
        active, scanned = scan_network(r, scanned_so_far)
        all_active.extend(active)
        scanned_so_far += scanned
    
    print("\n" + BOLD + OKGREEN + "📊 Final Summary:" + ENDC)
    print(CYAN + "   ➤ IP ranges processed: " + str(processed_ranges) + ENDC)
    print(CYAN + "   ➤ Addresses scanned: " + str(scanned_so_far) + ENDC)
    print(OKGREEN + "   ➤ Active hosts found: " + str(len(all_active)) + ENDC)
    
    if all_active:
        print("\n" + YELLOW + "📝 List of active IPs:" + ENDC)
        for ip in all_active:
            print("   " + OKGREEN + "► " + ip + ENDC)

if __name__ == "__main__":
    main()
