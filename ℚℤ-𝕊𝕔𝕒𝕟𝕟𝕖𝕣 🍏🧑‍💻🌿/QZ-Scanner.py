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
BANNER = f"""
{RAND_COLOR}
{OKGREEN}╔════════════════════════════════════════════════════════════════════════╗
║                    {BOLD}ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 🍏🧑‍💻🌿💀{ENDC}{OKGREEN}                              ║
║                  Advanced IP Range Scanner - Ayhan Mansur                   ║
╚════════════════════════════════════════════════════════════════════════╝{ENDC}
"""

SCAN_LIMIT = 120_000  # حداکثر تعداد آدرس‌های اسکن شده

def scan_host(ip):
    param = '-n' if sys.platform.startswith('win') else '-c'
    result = subprocess.run(['ping', param, '1', str(ip)],
                            capture_output=True, text=True)
    return result.returncode == 0

def scan_network(network_str, scanned_count):
    """اسکن شبکه با رعایت محدودیت - returns (active_hosts, new_scanned_count)"""
    try:
        network = ip_network(network_str, strict=False)
        remaining = SCAN_LIMIT - scanned_count
        addresses = list(network.hosts())
        
        # اگر تعداد آدرس‌های این رنج بیشتر از باقی‌مانده است، فقط تا سقف اسکن کن
        if len(addresses) > remaining:
            addresses = addresses[:remaining]
            print(f"{WARNING}⚠️ Limit reached: scanning only {remaining} of {len(network.hosts())} addresses in {network_str}{ENDC}")
        
        color = random.choice(colors)
        print(f"{color}🔍 Scanning {network_str} ({len(addresses)} addresses, total scanned so far: {scanned_count + len(addresses)}/{SCAN_LIMIT})...{ENDC}")
        
        active_hosts = []
        for ip in addresses:
            if scan_host(ip):
                active_hosts.append(str(ip))
                print(f"{OKGREEN}   ✅ {ip} is active{ENDC}")
        
        return active_hosts, len(addresses)
    except Exception as e:
        print(f"{FAIL}❌ Error in range {network_str}: {e}{ENDC}")
        return [], 0

def main():
    print(BANNER)
    
    # پرسش شروع اسکن
    start_choice = input(f"{CYAN}❓ Do you want to start scan? [Y/n]: {ENDC}").strip().lower()
    if start_choice == 'n':
        print(f"{YELLOW}🚫 Scan cancelled by user.{ENDC}")
        sys.exit(0)
    
    # لینک مستقیم فایل Ranges.txt
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
    print(f"{YELLOW}⚠️ Scan limit: {SCAN_LIMIT} addresses{ENDC}")
    print(f"{LITBU}🚀 Starting scan...{ENDC}\n")
    
    all_active = []
    scanned_so_far = 0
    
    for r in ranges:
        if scanned_so_far >= SCAN_LIMIT:
            print(f"{WARNING}⚠️ Scan limit reached ({SCAN_LIMIT} addresses). Stopping...{ENDC}")
            break
        active, scanned = scan_network(r, scanned_so_far)
        all_active.extend(active)
        scanned_so_far += scanned
    
    print(f"\n{BOLD}{OKGREEN}📊 Final Summary:{ENDC}")
    print(f"{CYAN}   ➤ IP ranges processed: {len(ranges[:ranges.index(r)+1] if scanned_so_far >= SCAN_LIMIT else len(ranges))}{ENDC}")
    print(f"{CYAN}   ➤ Addresses scanned: {scanned_so_far}{ENDC}")
    print(f"{OKGREEN}   ➤ Active hosts found: {len(all_active)}{ENDC}")
    if all_active:
        print(f"\n{YELLOW}📝 List of active IPs:{ENDC}")
        for ip in all_active:
            print(f"   {OKGREEN}► {ip}{ENDC}")

if __name__ == "__main__":
    main()
