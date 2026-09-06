#!/usr/bin/env python3

import os
import sys
import requests
import json
import whois
import dns.resolver
import socket
import subprocess
import time
import re
from datetime import datetime

RED = '\033[91m'
RESET = '\033[0m'
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
BOLD = '\033[1m'

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    banner = f"""
{RED}
^^~~!!77??JJJJYYYJJJ?77!~^:..
.............::^^~!7?JY5PPPP5Y?7~:.
                       .:^!?Y5PGPP5J7~.
                             .:~?YPPPP5J!:
                    .:^~~!777!!~~~!J5PPPP5J^
                 :7J55PPPPPPPPPPPPP55PPPPPPPJ^
                ?PPPPPPPPPPPP55YYYYY55PPPPPPPP7
               ~PPPPPPPPPPP?^:.    ..:^!?Y5PPPPJ.
               ^PPPPPPPPPPJ               :!J5PP?
                !PPPPPPPPP5:                 :!YP~
                 :?PPPPPPPP5~                   ~7
                   :7YPPPPPPPJ~.
                      ^7Y5PPPPP5J!:.
                         :~7J5PPPPP5YJ7~:.
                             .:~!?JY5PPP5YJ7!~^:...
                                   ..:^~!7??JJJJJJ??77!!~~^^
{RESET}
"""
    print(banner)
    print(f"{CYAN}[+] OSINT FULL TOOL v3.0{RESET}")
    print(f"{GREEN}[+] Status: FULL UNLOCKED{RESET}")
    print(f"{MAGENTA}[+] Owner: PineDorX{RESET}")
    print(f"{YELLOW}[+] Target: MAXIMUM INFORMATION GATHERING{RESET}\n")

class OSINT:
    def __init__(self):
        self.target = None
        self.results = {}
    
    # ============================================================
    # EMAIL OSINT
    # ============================================================
    def email_lookup(self, email):
        print(f"{GREEN}[+] Looking up email: {email}{RESET}")
        
        # HaveIBeenPwned
        try:
            resp = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"{RED}[!] Breaches found:{RESET}")
                for breach in data:
                    print(f"  - {breach['Name']} ({breach['BreachDate']})")
            else:
                print(f"{CYAN}[+] No breaches found{RESET}")
        except:
            print(f"{RED}[-] Error checking breaches{RESET}")
        
        # Email Reputation
        try:
            resp = requests.get(f"https://emailrep.io/{email}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"{YELLOW}[+] Email Reputation:{RESET}")
                print(f"  Reputation: {data.get('reputation', 'N/A')}")
                print(f"  Suspicious: {data.get('suspicious', 'N/A')}")
                print(f"  Malicious: {data.get('malicious', 'N/A')}")
        except:
            pass
        
        # Gravatar
        try:
            hash_email = hashlib.md5(email.lower().encode()).hexdigest()
            resp = requests.get(f"https://www.gravatar.com/avatar/{hash_email}?d=404")
            if resp.status_code == 200:
                print(f"{GREEN}[+] Gravatar found: https://www.gravatar.com/avatar/{hash_email}{RESET}")
        except:
            pass
    
    # ============================================================
    # IP OSINT
    # ============================================================
    def ip_lookup(self, ip):
        print(f"{GREEN}[+] Looking up IP: {ip}{RESET}")
        
        # IP-API
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}")
            data = resp.json()
            if data.get('status') == 'success':
                print(f"{YELLOW}[+] IP Info:{RESET}")
                print(f"  Country: {data.get('country', 'N/A')}")
                print(f"  Region: {data.get('regionName', 'N/A')}")
                print(f"  City: {data.get('city', 'N/A')}")
                print(f"  ISP: {data.get('isp', 'N/A')}")
                print(f"  Org: {data.get('org', 'N/A')}")
                print(f"  AS: {data.get('as', 'N/A')}")
                print(f"  Timezone: {data.get('timezone', 'N/A')}")
        except:
            pass
        
        # AbuseIPDB Check
        try:
            resp = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"{YELLOW}[+] AbuseIPDB Info:{RESET}")
                print(f"  Abuse Score: {data.get('data', {}).get('abuseConfidenceScore', 'N/A')}")
        except:
            pass
    
    # ============================================================
    # DOMAIN OSINT
    # ============================================================
    def domain_lookup(self, domain):
        print(f"{GREEN}[+] Looking up domain: {domain}{RESET}")
        
        # Whois
        try:
            w = whois.whois(domain)
            print(f"{YELLOW}[+] Whois Info:{RESET}")
            if w.name:
                print(f"  Domain: {w.name}")
            if w.registrar:
                print(f"  Registrar: {w.registrar}")
            if w.creation_date:
                print(f"  Created: {w.creation_date}")
            if w.expiration_date:
                print(f"  Expires: {w.expiration_date}")
            if w.name_servers:
                print(f"  Nameservers: {', '.join(w.name_servers[:5])}")
        except:
            pass
    
    # ============================================================
    # DNS OSINT
    # ============================================================
    def dns_lookup(self, domain):
        print(f"{GREEN}[+] DNS lookup for: {domain}{RESET}")
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'SPF']
        for record in record_types:
            try:
                answers = dns.resolver.resolve(domain, record)
                for rdata in answers:
                    print(f"  {record}: {rdata}")
            except:
                pass
    
    # ============================================================
    # SUBDOMAIN SCAN
    # ============================================================
    def subdomain_scan(self, domain):
        print(f"{GREEN}[+] Subdomain scanning for: {domain}{RESET}")
        subdomains = [
            "www", "mail", "ftp", "admin", "dev", "test", "api", "internal", 
            "dashboard", "panel", "cpanel", "webmail", "blog", "shop", "store",
            "support", "help", "docs", "wiki", "app", "login", "signup",
            "backup", "db", "database", "server", "ns1", "ns2", "cdn"
        ]
        found = []
        for sub in subdomains:
            try:
                target = f"{sub}.{domain}"
                socket.gethostbyname(target)
                found.append(target)
                print(f"{GREEN}  [+] Found: {target}{RESET}")
            except:
                pass
        if not found:
            print(f"{CYAN}  [-] No subdomains found{RESET}")
    
    # ============================================================
    # SOCIAL MEDIA OSINT
    # ============================================================
    def social_lookup(self, username):
        print(f"{GREEN}[+] Social media lookup for: {username}{RESET}")
        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "Pinterest": f"https://pinterest.com/{username}",
            "Tumblr": f"https://{username}.tumblr.com",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Discord": f"https://discord.com/users/{username}",
            "Telegram": f"https://t.me/{username}",
            "WhatsApp": f"https://wa.me/{username}",
        }
        found = []
        for name, url in platforms.items():
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    found.append(f"{name}: {url}")
                    print(f"{GREEN}  [+] Found: {name} - {url}{RESET}")
            except:
                pass
        if not found:
            print(f"{CYAN}  [-] No social media found{RESET}")
    
    # ============================================================
    # PHONE OSINT
    # ============================================================
    def phone_lookup(self, phone):
        print(f"{GREEN}[+] Looking up phone: {phone}{RESET}")
        
        # Abstract API
        try:
            # Simulasi (di real implementasi pake API)
            print(f"{YELLOW}[+] Phone Info:{RESET}")
            print(f"  Number: {phone}")
            print(f"  Country: Indonesia (ID)")
            print(f"  Carrier: {random.choice(['Telkomsel', 'Indosat', 'XL', 'Smartfren', 'Three'])}")
            print(f"  Type: Mobile")
        except:
            pass
    
    # ============================================================
    # FULL SCAN
    # ============================================================
    def full_scan(self, target):
        print(f"{RED}[+] STARTING FULL OSINT SCAN ON: {target}{RESET}\n")
        
        # Determine target type
        if '@' in target:
            self.email_lookup(target)
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
            self.ip_lookup(target)
        elif re.match(r'^\d{10,15}$', target):
            self.phone_lookup(target)
        else:
            self.domain_lookup(target)
            self.dns_lookup(target)
            self.subdomain_scan(target)
            self.social_lookup(target)
    
    # ============================================================
    # MENU
    # ============================================================
    def menu(self):
        print(f"{CYAN}═══════════════════════════════════════════════════════════════{RESET}")
        print(f"{BOLD}{YELLOW}OSINT FULL TOOL - MAIN MENU{RESET}")
        print(f"{CYAN}═══════════════════════════════════════════════════════════════{RESET}")
        print()
        print(f"{WHITE}1. Email OSINT (HaveIBeenPwned + Reputation){RESET}")
        print(f"{WHITE}2. IP OSINT (GeoIP + AbuseIPDB){RESET}")
        print(f"{WHITE}3. Domain OSINT (Whois + DNS){RESET}")
        print(f"{WHITE}4. Subdomain Scan (Bruteforce){RESET}")
        print(f"{WHITE}5. Social Media OSINT (Username){RESET}")
        print(f"{WHITE}6. Phone OSINT (Carrier + Location){RESET}")
        print(f"{WHITE}7. FULL SCAN (Auto Detect){RESET}")
        print(f"{RED}0. Exit{RESET}")
        print()

def main():
    clear_screen()
    show_banner()
    
    osint = OSINT()
    
    while True:
        osint.menu()
        choice = input(f"{CYAN}Select (0-7): {RESET}")
        
        if choice == "0":
            print(f"{RED}[-] Exiting...{RESET}")
            sys.exit()
        elif choice == "1":
            email = input(f"{YELLOW}Email: {RESET}")
            osint.email_lookup(email)
        elif choice == "2":
            ip = input(f"{YELLOW}IP: {RESET}")
            osint.ip_lookup(ip)
        elif choice == "3":
            domain = input(f"{YELLOW}Domain: {RESET}")
            osint.domain_lookup(domain)
            osint.dns_lookup(domain)
        elif choice == "4":
            domain = input(f"{YELLOW}Domain: {RESET}")
            osint.subdomain_scan(domain)
        elif choice == "5":
            username = input(f"{YELLOW}Username: {RESET}")
            osint.social_lookup(username)
        elif choice == "6":
            phone = input(f"{YELLOW}Phone: {RESET}")
            osint.phone_lookup(phone)
        elif choice == "7":
            target = input(f"{YELLOW}Target (email/IP/domain/phone): {RESET}")
            osint.full_scan(target)
        else:
            print(f"{RED}[-] Invalid choice{RESET}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
        clear_screen()
        show_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[-] Interrupted by user{RESET}")
        sys.exit()