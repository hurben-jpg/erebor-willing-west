import urllib.request
import shutil
import os

url = "https://github.com/espressif/esp-hosted/releases/download/release%2Ffg-v1.0.0.0.0/esp_hosted_fg-esp32c6-sdio-v1.0.0.0.0.zip"
output_file = "d:\\PROJECTS\\Antigravity\\Erebor\\firmware.zip"

print(f"Downloading {url}...")
try:
    with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print("Download complete.")
except Exception as e:
    print(f"Error: {e}")
