
    #!/usr/bin/env python3

import os
import sys
import requests
import socket
import re
import time
import json
import hashlib
import subprocess
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
    print(f"{CYAN}[+] OSINT TOOL v4.0 - FULL WORKING{RESET}")
    print(f"{GREEN}[+] Status: FULL UNLOCKED{RESET}")
    print(f"{MAGENTA}[+] Owner: PineDorX{RESET}\n")

class OSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    # ============================================================
    # EMAIL OSINT
    # ============================================================
    def email_lookup(self, email):
        print(f"\n{GREEN}[+] EMAIL OSINT: {email}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        # 1. HaveIBeenPwned
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            resp = self.session.get(url)
            if resp.status_code == 200:
                data = resp.json()
                print(f"{RED}[!] Breaches Found: {len(data)}{RESET}")
                for breach in data:
                    print(f"  - {breach.get('Name', 'Unknown')} ({breach.get('BreachDate', 'N/A')})")
            else:
                print(f"{GREEN}[+] No breaches found{RESET}")
        except Exception as e:
            print(f"{YELLOW}[-] Pwned check failed: {str(e)[:50]}{RESET}")
        
        # 2. Email Reputation (emailrep.io)
        try:
            url = f"https://emailrep.io/{email}"
            resp = self.session.get(url)
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n{YELLOW}[+] Email Reputation:{RESET}")
                print(f"  Reputation: {data.get('reputation', 'N/A')}")
                print(f"  Suspicious: {data.get('suspicious', 'False')}")
                print(f"  Malicious: {data.get('malicious', 'False')}")
        except Exception as e:
            print(f"{YELLOW}[-] Reputation check failed{RESET}")
        
        # 3. Gravatar
        try:
            hash_email = hashlib.md5(email.lower().encode()).hexdigest()
            gravatar_url = f"https://www.gravatar.com/avatar/{hash_email}?d=404"
            resp = self.session.get(gravatar_url)
            if resp.status_code == 200:
                print(f"\n{GREEN}[+] Gravatar: https://www.gravatar.com/avatar/{hash_email}{RESET}")
            else:
                print(f"{YELLOW}[-] No Gravatar found{RESET}")
        except:
            pass
        
        # 4. Hunter.io (email verification)
        try:
            # Simulasi cek format email
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                print(f"{GREEN}[+] Email format: VALID{RESET}")
                domain = email.split('@')[1]
                print(f"{GREEN}[+] Domain: {domain}{RESET}")
        except:
            pass
    
    # ============================================================
    # IP OSINT
    # ============================================================
    def ip_lookup(self, ip):
        print(f"\n{GREEN}[+] IP OSINT: {ip}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        # 1. IP-API (GeoIP)
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,timezone,lat,lon"
            resp = self.session.get(url)
            data = resp.json()
            if data.get('status') == 'success':
                print(f"{YELLOW}[+] GeoIP Info:{RESET}")
                print(f"  Country: {data.get('country', 'N/A')}")
                print(f"  Region: {data.get('regionName', 'N/A')}")
                print(f"  City: {data.get('city', 'N/A')}")
                print(f"  ISP: {data.get('isp', 'N/A')}")
                print(f"  Organization: {data.get('org', 'N/A')}")
                print(f"  AS: {data.get('as', 'N/A')}")
                print(f"  Timezone: {data.get('timezone', 'N/A')}")
            else:
                print(f"{RED}[-] IP-API failed{RESET}")
        except Exception as e:
            print(f"{YELLOW}[-] GeoIP check failed: {str(e)[:50]}{RESET}")
        
        # 2. IP Info (ipinfo.io)
        try:
            url = f"https://ipinfo.io/{ip}/json"
            resp = self.session.get(url)
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n{YELLOW}[+] IPInfo:{RESET}")
                print(f"  Hostname: {data.get('hostname', 'N/A')}")
                print(f"  Location: {data.get('loc', 'N/A')}")
                print(f"  Org: {data.get('org', 'N/A')}")
        except:
            pass
        
        # 3. AbuseIPDB Check
        try:
            url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
            # AbuseIPDB butuh API key, ini simulasi
            print(f"\n{YELLOW}[+] AbuseIPDB:{RESET}")
            print(f"  Note: Requires API key for full data")
            print(f"  URL: https://www.abuseipdb.com/check/{ip}")
        except:
            pass
        
        # 4. Reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"\n{GREEN}[+] Reverse DNS: {hostname}{RESET}")
        except:
            pass
    
    # ============================================================
    # DOMAIN OSINT
    # ============================================================
    def domain_lookup(self, domain):
        print(f"\n{GREEN}[+] DOMAIN OSINT: {domain}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        # 1. Whois (pakai whois service)
        try:
            import whois
            w = whois.whois(domain)
            print(f"{YELLOW}[+] Whois Info:{RESET}")
            if w.domain_name:
                print(f"  Domain: {w.domain_name}")
            if w.registrar:
                print(f"  Registrar: {w.registrar}")
            if w.creation_date:
                print(f"  Created: {w.creation_date}")
            if w.expiration_date:
                print(f"  Expires: {w.expiration_date}")
            if w.name_servers:
                ns = w.name_servers
                if isinstance(ns, list):
                    ns = ns[:3]
                print(f"  Nameservers: {', '.join(ns)}")
        except ImportError:
            print(f"{YELLOW}[-] whois module not installed. Run: pip install whois{RESET}")
        except Exception as e:
            print(f"{YELLOW}[-] Whois failed: {str(e)[:50]}{RESET}")
        
        # 2. DNS Lookup
        try:
            import dns.resolver
            print(f"\n{YELLOW}[+] DNS Records:{RESET}")
            record_types = ['A', 'MX', 'NS', 'TXT', 'CNAME']
            for record in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record)
                    for rdata in answers:
                        print(f"  {record}: {rdata}")
                except:
                    pass
        except ImportError:
            print(f"{YELLOW}[-] dnspython not installed. Run: pip install dnspython{RESET}")
        except:
            pass
    
    # ============================================================
    # SUBDOMAIN SCAN
    # ============================================================
    def subdomain_scan(self, domain):
        print(f"\n{GREEN}[+] SUBDOMAIN SCAN: {domain}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        subdomains = [
            "www", "mail", "ftp", "admin", "dev", "test", "api", "internal",
            "dashboard", "panel", "cpanel", "webmail", "blog", "shop", "store",
            "support", "help", "docs", "wiki", "app", "login", "signup",
            "backup", "db", "database", "server", "ns1", "ns2", "cdn",
            "beta", "alpha", "stage", "staging", "demo", "portal", "secure",
            "m", "mobile", "old", "new", "vpn", "remote", "proxy"
        ]
        found = []
        total = len(subdomains)
        print(f"{CYAN}[+] Scanning {total} subdomains...{RESET}")
        
        for i, sub in enumerate(subdomains):
            target = f"{sub}.{domain}"
            try:
                socket.gethostbyname(target)
                found.append(target)
                print(f"{GREEN}  [+] Found: {target}{RESET}")
            except:
                pass
            # Progress
            if (i + 1) % 10 == 0:
                print(f"{CYAN}  Progress: {i+1}/{total}{RESET}")
        
        if found:
            print(f"\n{GREEN}[+] Total found: {len(found)}{RESET}")
        else:
            print(f"{YELLOW}[-] No subdomains found{RESET}")
    
    # ============================================================
    # SOCIAL MEDIA OSINT
    # ============================================================
    def social_lookup(self, username):
        print(f"\n{GREEN}[+] SOCIAL MEDIA OSINT: {username}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        platforms = {
            "Instagram": f"https://www.instagram.com/{username}/",
            "Twitter": f"https://twitter.com/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "YouTube": f"https://www.youtube.com/@{username}",
            "Pinterest": f"https://www.pinterest.com/{username}",
            "Tumblr": f"https://{username}.tumblr.com",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Telegram": f"https://t.me/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "Snapchat": f"https://www.snapchat.com/add/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "DeviantArt": f"https://www.deviantart.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "Patreon": f"https://www.patreon.com/{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "Tinder": f"https://tinder.com/@{username}"
        }
        
        found_count = 0
        for name, url in platforms.items():
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    print(f"{GREEN}  [+] Found: {name} -> {url}{RESET}")
                    found_count += 1
                else:
                    print(f"{CYAN}  [-] {name}: Not found{RESET}")
            except Exception as e:
                print(f"{CYAN}  [-] {name}: Error checking{RESET}")
            time.sleep(0.1)  # Jangan banjir request
        
        print(f"\n{GREEN}[+] Total platforms found: {found_count}{RESET}")
    
    # ============================================================
    # PHONE OSINT
    # ============================================================
    def phone_lookup(self, phone):
        print(f"\n{GREEN}[+] PHONE OSINT: {phone}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        # Clean phone number
        phone_clean = re.sub(r'[^0-9+]', '', phone)
        
        # Determine country
        print(f"{YELLOW}[+] Phone Information:{RESET}")
        print(f"  Raw: {phone}")
        print(f"  Clean: {phone_clean}")
        
        # Indonesia check
        if phone_clean.startswith('62') or phone_clean.startswith('0'):
            print(f"  Country: Indonesia (ID)")
            if phone_clean.startswith('081') or phone_clean.startswith('082') or phone_clean.startswith('083'):
                print(f"  Carrier: Telkomsel")
            elif phone_clean.startswith('085') or phone_clean.startswith('086'):
                print(f"  Carrier: Indosat")
            elif phone_clean.startswith('087'):
                print(f"  Carrier: XL")
            elif phone_clean.startswith('088'):
                print(f"  Carrier: Smartfren")
            elif phone_clean.startswith('089'):
                print(f"  Carrier: Three (3)")
            else:
                print(f"  Carrier: Unknown")
        else:
            print(f"  Country: Unknown")
            print(f"  Carrier: Unknown")
        
        # Check on haveibeenpwned (phone)
        try:
            url = f"https://haveibeenpwned.com/account/{phone_clean}"
            resp = self.session.get(url)
            if resp.status_code == 200:
                print(f"\n{GREEN}[+] Phone found in breaches (check manually){RESET}")
        except:
            pass
    
    # ============================================================
    # AUTO DETECT SCAN
    # ============================================================
    def auto_scan(self, target):
        print(f"\n{RED}[+] AUTO SCAN DETECTED: {target}{RESET}")
        print(f"{CYAN}────────────────────────────────────{RESET}")
        
        # Check if email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            self.email_lookup(target)
            return
        
        # Check if IP
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
            self.ip_lookup(target)
            return
        
        # Check if phone (numeric)
        if re.match(r'^\+?[0-9]{10,15}$', target):
            self.phone_lookup(target)
            return
        
        # If domain or username
        if '.' in target:
            self.domain_lookup(target)
            self.subdomain_scan(target)
        else:
            self.social_lookup(target)
            self.domain_lookup(f"{target}.com")

# ============================================================
# MAIN MENU
# ============================================================

def main():
    clear_screen()
    show_banner()
    
    osint = OSINT()
    
    while True:
        print(f"\n{CYAN}═══════════════════════════════════════════════════════════════{RESET}")
        print(f"{BOLD}{YELLOW}OSINT TOOL v4.0 - MAIN MENU{RESET}")
        print(f"{CYAN}═══════════════════════════════════════════════════════════════{RESET}")
        print()
        print(f"{WHITE}1. Email OSINT (Pwned + Reputation){RESET}")
        print(f"{WHITE}2. IP OSINT (GeoIP + DNS){RESET}")
        print(f"{WHITE}3. Domain OSINT (Whois + DNS){RESET}")
        print(f"{WHITE}4. Subdomain Scan (Bruteforce){RESET}")
        print(f"{WHITE}5. Social Media OSINT (Username){RESET}")
        print(f"{WHITE}6. Phone OSINT (Carrier + Info){RESET}")
        print(f"{WHITE}7. AUTO SCAN (Detect Input Type){RESET}")
        print(f"{WHITE}8. TEST (Check API Connections){RESET}")
        print(f"{RED}0. Exit{RESET}")
        print()
        
        choice = input(f"{CYAN}Select (0-8): {RESET}")
        
        if choice == "0":
            print(f"{RED}[-] Exiting...{RESET}")
            sys.exit()
        
        elif choice == "1":
            target = input(f"{YELLOW}Email: {RESET}")
            osint.email_lookup(target)
        
        elif choice == "2":
            target = input(f"{YELLOW}IP Address: {RESET}")
            osint.ip_lookup(target)
        
        elif choice == "3":
            target = input(f"{YELLOW}Domain: {RESET}")
            osint.domain_lookup(target)
        
        elif choice == "4":
            target = input(f"{YELLOW}Domain: {RESET}")
            osint.subdomain_scan(target)
        
        elif choice == "5":
            target = input(f"{YELLOW}Username: {RESET}")
            osint.social_lookup(target)
        
        elif choice == "6":
            target = input(f"{YELLOW}Phone Number: {RESET}")
            osint.phone_lookup(target)
        
        elif choice == "7":
            target = input(f"{YELLOW}Target (email/IP/domain/phone/username): {RESET}")
            osint.auto_scan(target)
        
        elif choice == "8":
            print(f"\n{YELLOW}[+] Testing API Connections...{RESET}")
            try:
                resp = requests.get("https://httpbin.org/ip", timeout=5)
                print(f"{GREEN}[+] Internet: OK{RESET}")
            except:
                print(f"{RED}[-] No Internet Connection{RESET}")
            
            try:
                resp = requests.get("https://ip-api.com/json/8.8.8.8", timeout=5)
                if resp.status_code == 200:
                    print(f"{GREEN}[+] IP-API: OK{RESET}")
            except:
                print(f"{RED}[-] IP-API: FAILED{RESET}")
            
            try:
                resp = requests.get("https://haveibeenpwned.com/api/v3/breaches", timeout=5)
                if resp.status_code == 200:
                    print(f"{GREEN}[+] HaveIBeenPwned: OK{RESET}")
            except:
                print(f"{RED}[-] HaveIBeenPwned: FAILED{RESET}")
            
            try:
                resp = requests.get("https://ipinfo.io/json", timeout=5)
                if resp.status_code == 200:
                    print(f"{GREEN}[+] IPInfo: OK{RESET}")
            except:
                print(f"{RED}[-] IPInfo: FAILED{RESET}")
        
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