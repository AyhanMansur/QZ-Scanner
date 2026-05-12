import sys
import subprocess
import random
import requests
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
║                  Advanced IP Range Scanner - Ayhan Mansur                   ║
╚════════════════════════════════════════════════════════════════════════╝{ENDC}
"""

# ================== SCANNER FUNCTIONS ==================
def scan_host(ip):
    param = '-n' if sys.platform.startswith('win') else '-c'
    result = subprocess.run(['ping', param, '1', str(ip)],
                            capture_output=True, text=True)
    return result.returncode == 0

def scan_network(network_str):
    try:
        network = ip_network(network_str, strict=False)
        color = random.choice(colors)
        print(f"{color}🔍 Scanning {network_str} ({network.num_addresses} addresses)...{ENDC}")

        hosts = list(network.hosts())
        active_hosts = []
        for ip in hosts:
            if scan_host(ip):
                active_hosts.append(str(ip))
                print(f"{OKGREEN}   ✅ {ip} is active{ENDC}")
        return active_hosts
    except Exception as e:
        print(f"{FAIL}❌ Error in range {network_str}: {e}{ENDC}")
        return []

# ================== MAIN ==================
def main():
    print(BANNER)

    # پرسش شروع اسکن با پیش‌فرض Yes
    start_choice = input(f"{CYAN}❓ Do you want to start scan? [Y/n]: {ENDC}").strip().lower()
    if start_choice == 'n':
        print(f"{YELLOW}🚫 Scan cancelled by user.{ENDC}")
        sys.exit(0)

    # لینک مستقیم فایل Ranges.txt در گیت‌هاب
    url = "https://raw.githubusercontent.com/AyhanMansur/QZ-Scanner/refs/heads/main/%E2%84%9A%E2%84%A4-%F0%9D%95%8A%F0%9D%95%94%F0%9D%95%92%F0%9D%95%9F%F0%9D%95%9F%F0%9D%95%96%F0%9D%95%A3%20%F0%9F%8D%8F%F0%9F%A7%91%E2%80%8D%F0%9F%92%BB%F0%9F%8C%BF/Ranges.txt"

    print(f"{LITBU}📡 ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 - Downloading range list from GitHub...{ENDC}")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"{FAIL}❌ Failed to download ranges.txt: {e}{ENDC}")
        sys.exit(1)

    ranges = [
        line.strip() for line in content.splitlines()
        if line.strip() and not line.startswith('#')
    ]

    if not ranges:
        print(f"{FAIL}❌ No IP ranges found in the downloaded file.{ENDC}")
        sys.exit(1)

    print(f"{OKGREEN}✅ Downloaded {len(ranges)} IP ranges.{ENDC}")
    print(f"{LITBU}🚀 Starting scan...{ENDC}\n")

    all_active = []
    for r in ranges:
        all_active.extend(scan_network(r))

    print(f"\n{BOLD}{OKGREEN}📊 Final Summary:{ENDC}")
    print(f"{CYAN}   ➤ Ranges scanned: {len(ranges)}{ENDC}")
    print(f"{OKGREEN}   ➤ Active hosts: {len(all_active)}{ENDC}")
    if all_active:
        print(f"\n{YELLOW}📝 List of active IPs:{ENDC}")
        for ip in all_active:
            print(f"   {OKGREEN}► {ip}{ENDC}")

if __name__ == "__main__":
    main()
