import requests
from concurrent.futures import ThreadPoolExecutor

# Input file containing raw subdomains (one per line)
SUBDOMAINS_FILE = "subdomains.txt"
OUTPUT_FILE = "live_targets.txt"
THREADS = 20
TIMEOUT = 5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BugBountyResearch/1.0"
}

def check_subdomain(subdomain):
    subdomain = subdomain.strip()
    if not subdomain:
        return None
    
    # Try HTTPS first, fall back to HTTP if it fails
    for protocol in ["https://", "http://"]:
        url = f"{protocol}{subdomain}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=False)
            result = f"[+] {url} | Status: {response.status_code} | Length: {len(response.content)}"
            print(result)
            return url
        except requests.exceptions.RequestException:
            continue
    return None

def main():
    try:
        with open(SUBDOMAINS_FILE, "r") as f:
            domains = f.readlines()
    except FileNotFoundError:
        print(f"[-] Error: Ensure '{SUBDOMAINS_FILE}' exists in this directory.")
        return

    print(f"[*] Probing {len(domains)} domains across {THREADS} threads...")
    
    live_hosts = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(check_subdomain, domains)
        for res in results:
            if res:
                live_hosts.append(res)
                
    with open(OUTPUT_FILE, "w") as f:
        for host in live_hosts:
            f.write(f"{host}\n")
            
    print(f"[*] Finished. Saved {len(live_hosts)} active hosts to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
