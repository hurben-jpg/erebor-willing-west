import urllib.request
import re

url = "https://github.com/espressif/esp-hosted/releases"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        links = re.findall(r'href="([^"]+)"', html)
        for link in links:
            if "download" in link and "zip" in link:
                print(link)
except Exception as e:
    print(f"Error: {e}")
