import urllib.request
import re

url = "https://github.com/espressif/esp-hosted/releases"
try:
    print(f"Fetching {url}...")
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        # Look for links to zip/bin files for ESP32-C6 SDIO FG
        # Pattern: href="/espressif/esp-hosted/releases/download/..."
        links = re.findall(r'href="(/espressif/esp-hosted/releases/download/[^"]+)"', html)
        
        found = False
        for link in links:
            if "esp32c6" in link.lower() and "sdio" in link.lower() and "fg" in link.lower():
                full_url = "https://github.com" + link
                print(f"Found firmware: {full_url}")
                found = True
        
        if not found:
            print("No matching firmware found in releases page.")
            # Fallback: try to construct the URL for 1.0.0.0.0
            print("Trying to construct URL for release 1.0.0.0.0...")
            # https://github.com/espressif/esp-hosted/releases/download/release%2Ffg-v1.0.0.0.0/esp_hosted_fg-esp32c6-sdio-v1.0.0.0.0.zip
            # Note: URL encoding might be needed
            pass

except Exception as e:
    print(f"Error: {e}")
