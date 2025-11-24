# ingest_youtube.py
"""Script to download a YouTube song and ingest it into the Shazam database."""

import sys
import os
import requests
import yt_dlp

# Configuration
INGEST_URL = "http://127.0.0.1:5000/ingest"
DOWNLOAD_FOLDER = "downloads"

def download_youtube_audio(url):
    """Download audio from YouTube URL as a WAV file."""
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        'overwrites': True,
        'concurrent_fragment_downloads': 1, # Disable concurrent downloads to avoid locking
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading {url}...")
        info = ydl.extract_info(url, download=True)
        # yt-dlp with FFmpegExtractAudio postprocessor automatically updates the extension
        filename = ydl.prepare_filename(info)
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        
        return wav_filename, info

def ingest_song(filepath, info):
    """Send the downloaded file to the ingestion API."""
    print(f"Ingesting {filepath}...")
    
    metadata = {
        "title": info.get('title', 'Unknown Title'),
        "artist": info.get('uploader', 'Unknown Artist'),
        "album": "YouTube Import",
        "year": info.get('upload_date', '')[:4]
    }
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(INGEST_URL, files=files, data=metadata)
            
        if response.status_code == 200:
            print("✅ Successfully ingested!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Ingestion failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    # Force UTF-8 for stdout to avoid Unicode errors on Windows
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 2:
        print("Usage: python ingest_youtube.py <youtube_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    wav_path = None
    try:
        wav_path, info = download_youtube_audio(url)
        if wav_path and os.path.exists(wav_path):
            ingest_song(wav_path, info)
        else:
            print("Download failed or file not found.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup
        if wav_path and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except OSError:
                pass
