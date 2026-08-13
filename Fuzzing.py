import requests
import sys

TARGET_URL = "https://example.com"  # Base URL without trailing slash
WORDLIST_PATH = "common_paths.txt"   # e.g., from Seclists

def fuzz_directory():
    try:
        with open(WORDLIST_PATH, "r") as wl:
            paths = wl.readlines()
    except FileNotFoundError:
        print("[-] Wordlist not found. Provide a valid path.")
        sys.exit(1)

    print(f"[*] Starting content discovery on {TARGET_URL}...")
    
    for path in paths:
        path = path.strip()
        if not path:
            continue
            
        # Ensure path begins with a slash
        formatted_path = f"/{path}" if not path.startswith("/") else path
        url = f"{TARGET_URL}{formatted_path}"
        
        try:
            # Using head requests to save bandwidth and improve performance
            res = requests.head(url, timeout=3, allow_redirects=True)
            
            # Filter out generic 404 responses
            if res.status_code not in [404, 502, 503]:
                print(f"[!] Found: {url} (Status: {res.status_code})")
        except requests.exceptions.RequestException:
            pass

if __name__ == "__main__":
    fuzz_directory()
