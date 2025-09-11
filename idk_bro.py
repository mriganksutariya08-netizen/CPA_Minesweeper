import os
import re
import wget
import requests
from urllib.parse import urljoin

# URL of the game page
url = "https://cardgames.io/minesweeper/"
save_dir = "downloaded_game"
os.makedirs(save_dir, exist_ok=True)

# Step 1: Download the HTML
html_path = os.path.join(save_dir, "index.html")
r = requests.get(url)
html = r.text
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

# Step 2: Find linked assets (src= and href=)
assets = re.findall(r'src="([^"]+)"|href="([^"]+)"', html)

# Flatten the matches
files_to_download = []
for src, href in assets:
    if src:
        files_to_download.append(src)
    if href:
        files_to_download.append(href)

# Step 3: Download each asset
for file_url in files_to_download:
    # Skip if it looks like an anchor (#something)
    if file_url.startswith("#"):
        continue

    # Build absolute URL
    full_url = urljoin(url, file_url)

    try:
        print(f"Downloading {full_url}")
        wget.download(full_url, out=save_dir)
    except Exception as e:
        print(f"Failed {full_url}: {e}")
