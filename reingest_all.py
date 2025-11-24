# reingest_all.py
"""Ingest all WAV files currently in the downloads folder."""

import os
import requests

API_URL = "http://127.0.0.1:5000/ingest"
DOWNLOADS_DIR = "downloads"

def ingest_file(filepath):
    print(f"Ingesting {filepath}...")
    filename = os.path.basename(filepath)
    # Use filename as title for simplicity since we lost the metadata
    metadata = {
        "title": filename,
        "artist": "Unknown",
        "album": "Batch Import",
        "year": "2024"
    }
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(API_URL, files=files, data=metadata)
            
        if response.status_code == 200:
            print(f"[OK] Success: {response.json().get('message')}")
        else:
            print(f"[FAIL] Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not os.path.exists(DOWNLOADS_DIR):
        print("No downloads directory found.")
    else:
        files = [f for f in os.listdir(DOWNLOADS_DIR) if f.endswith('.wav')]
        print(f"Found {len(files)} WAV files.")
        for f in files:
            ingest_file(os.path.join(DOWNLOADS_DIR, f))
