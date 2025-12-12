import sys
import os
import requests
import shutil
from urllib.parse import urlparse
# Import specific exception types for robust error handling
from requests.exceptions import RequestException, JSONDecodeError

# --- Helper Functions (Unchanged) ---

def get_filename_from_url(url):
    """Extracts a filename from the URL or generates a default one."""
    parsed = urlparse(url)
    # Check if path ends with a slash or is empty, if so, use a default name
    filename = os.path.basename(parsed.path.strip('/'))
    if not filename or '.' not in filename:
        # Tries to guess the extension from content-type header, but falls back to .dat
        return "downloaded_asset.dat"
    return filename

def download_file(url, output_dir="."):
    """Downloads a file from a URL to the output directory."""
    local_filename = get_filename_from_url(url)
    dest_path = os.path.join(output_dir, local_filename)

    print(f"Downloading asset from: {url}")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        print(f"File saved to: {dest_path}")
        return dest_path
    except RequestException as e:
        print(f"CRITICAL ERROR: Failed to download asset from {url}. Error: {e}", file=sys.stderr)
        sys.exit(1)

# --- Main Logic (Modified for robust error handling) ---

def process_stac_url(start_url):
    print(f"Fetching metadata from: {start_url}")

    item_data = None

    # 1. Fetch the initial URL and handle potential connection/parsing errors
    try:
        resp = requests.get(start_url)
        resp.raise_for_status() # Raise for 4xx/5xx responses
        data = resp.json()
    except RequestException as e:
        print(f"ERROR: Failed to connect or retrieve data from STAC URL: {start_url}. Error: {e}", file=sys.stderr)
        sys.exit(1)
    except JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON response from STAC URL: {start_url}. Is the URL a valid STAC endpoint? Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Case 1: Input is a Feature (Item)
    if data.get('type') == 'Feature':
        print("Input recognized as a STAC Item.")
        item_data = data

    # Case 2: Input is a Collection (Requires fetching items)
    elif data.get('type') == 'Collection':
        print("Input recognized as a STAC Collection. Looking for the first item...")

        # Strategy A: Check for static links with rel="item" (less common in APIs)
        links = data.get('links', [])
        item_link = next((l for l in links if l.get('rel') == 'item'), None)

        if item_link:
            item_url = item_link['href']
            # Resolve relative URLs if necessary (a full robust implementation would use a STAC client, but this handles simple cases)
            if not item_url.startswith('http'):
                base = start_url.rsplit('/', 1)[0]
                item_url = f"{base}/{item_url}"

            print(f"Found static item link: {item_url}")
            try:
                item_resp = requests.get(item_url)
                item_resp.raise_for_status()
                item_data = item_resp.json()
            except RequestException as e:
                print(f"ERROR: Failed to fetch static item link: {item_url}. Error: {e}", file=sys.stderr)
                sys.exit(1)
            except JSONDecodeError as e:
                print(f"ERROR: Failed to parse JSON from static item link: {item_url}. Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            # Strategy B: If it's a STAC API, try appending '/items'
            print("No static item links found. Trying STAC API '/items' endpoint...")
            items_url = start_url.rstrip('/') + "/items"
            try:
                items_resp = requests.get(items_url)
                items_resp.raise_for_status()
                features = items_resp.json().get('features', [])
                if features:
                    item_data = features[0]
                else:
                    print("ERROR: Collection contains no features when querying the /items endpoint.", file=sys.stderr)
                    sys.exit(1)
            except RequestException as e:
                print(f"ERROR: Could not retrieve items from API endpoint {items_url}. Error: {e}", file=sys.stderr)
                sys.exit(1)
            except JSONDecodeError as e:
                print(f"ERROR: Failed to parse JSON from items endpoint {items_url}. Error: {e}", file=sys.stderr)
                sys.exit(1)

    else:
        print(f"ERROR: Unknown STAC object type '{data.get('type')}'. Expected 'Feature' or 'Collection'.", file=sys.stderr)
        sys.exit(1)

    # 3. Asset Download Logic
    assets = item_data.get('assets', {})
    if not assets:
        print("ERROR: Selected Item has no assets to download.", file=sys.stderr)
        sys.exit(1)

    # Get the first asset
    first_asset_key = next(iter(assets))
    first_asset = assets[first_asset_key]

    asset_href = first_asset.get('href')
    print(f"Selected asset key: {first_asset_key}")

    download_file(asset_href)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stac_downloader.py <stac_url>", file=sys.stderr)
        sys.exit(1)

    stac_url = sys.argv[1]
    process_stac_url(stac_url)