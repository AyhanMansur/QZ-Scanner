import sys
import subprocess
import random
from ipaddress import ip_network
OKGREEN = '\033[92m'
WARNING = '\033[0;33m'
FAIL = '\033[91m'
ENDC = '\033[0m'
LITBU = '\033[94m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
PURPLE = '\033[0;35m'
BOLD = '\033[1m'
colors = [OKGREEN, LITBU, CYAN, PURPLE, YELLOW]
RAND_COLOR = random.choice(colors)
BANNER = f"""
{RAND_COLOR}
{OKGREEN}╔════════════════════════════════════════════════════════════════════════╗
║                    {BOLD}ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 🍏🧑‍💻🌿💀{ENDC}{OKGREEN}                              ║
║                  Advanced IP Range Scanner - Ayhan Mansur                   ║
╚════════════════════════════════════════════════════════════════════════╝{ENDC}
"""

def scan_host(ip):
    """Check if IP is alive using ping"""
    param = '-n' if sys.platform.startswith('win') else '-c'
    result = subprocess.run(['ping', param, '1', str(ip)], 
                            capture_output=True, text=True)
    return result.returncode == 0

def scan_network(network_str):
    """Scan all IPs inside a given network range"""
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

def main():
    print(BANNER)
    
    # Get filename from command line or use default
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "ranges.txt"
    
    # Ask if user wants to input single IP range manually
    use_manual = input(f"{CYAN}❓ Do you want to enter an IP range manually? (y/n): {ENDC}").strip().lower()
    
    ranges = []
    
    if use_manual == 'y':
        manual_range = input(f"{LITBU}🌐 Enter IP range (ex: 192.168.1.0/24): {ENDC}").strip()
        if manual_range:
            ranges.append(manual_range)
    else:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                ranges = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"{FAIL}❌ File {filename} not found.{ENDC}")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"{WARNING}⚠️ Encoding error. Trying with cp1252...{ENDC}")
            with open(filename, 'r', encoding='cp1252') as f:
                ranges = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not ranges:
        print(f"{FAIL}❌ No IP ranges provided. Exiting.{ENDC}")
        sys.exit(1)
    
    print(f"{LITBU}📡 ℚℤ-𝕊𝕔𝕒𝕟𝕟𝕖𝕣 - Reading {len(ranges)} range(s){ENDC}")
    
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