import requests
import json

TARGET = "https://example.com"

# The essential headers we want to verify
SECURITY_HEADERS = {
    "X-Frame-Options": "Prevents Clickjacking attacks.",
    "Content-Security-Policy": "Mitigates XSS and data injection vectors.",
    "Strict-Transport-Security": "Enforces secure HTTPS connections.",
    "X-Content-Type-Options": "Prevents MIME-sniffing vulnerabilities.",
    "Referrer-Policy": "Controls how much referrer information is shared."
}

def audit_headers(url):
    print(f"[*] Analyzing security headers for: {url}\n")
    try:
        response = requests.get(url, timeout=5)
        response_headers = response.headers
        
        missing_count = 0
        for header, description in SECURITY_HEADERS.items():
            # Check case-insensitively
            matching_key = next((k for k in response_headers if k.lower() == header.lower()), None)
            
            if matching_key:
                print(f"[+] PRESENT: {header}")
                print(f"    Value: {response_headers[matching_key]}\n")
            else:
                print(f"[-] MISSING: {header}")
                print(f"    Risk: {description}\n")
                missing_count += 1
                
        print(f"[*] Audit complete. Missing {missing_count} out of {len(SECURITY_HEADERS)} core security headers.")
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection failed: {e}")

if __name__ == "__main__":
    audit_headers(TARGET)
