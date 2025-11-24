# test_with_file.py
"""Test the Shazam API by sending a snippet of an existing WAV file."""

import os
import sys
import random
import requests
import soundfile as sf
import numpy as np

# Configuration
API_URL = "http://127.0.0.1:5000/identify"
DOWNLOADS_DIR = "downloads"
SNIPPET_DURATION = 5  # seconds

def get_random_wav_file():
    files = [f for f in os.listdir(DOWNLOADS_DIR) if f.endswith('.wav')]
    if not files:
        return None
    return os.path.join(DOWNLOADS_DIR, random.choice(files))

def create_snippet(input_path, output_path):
    print(f"Loading {input_path}...")
    data, fs = sf.read(input_path)
    
    # Pick a random start point (ensure we have enough audio)
    total_samples = len(data)
    needed_samples = int(SNIPPET_DURATION * fs)
    
    if total_samples < needed_samples:
        print("Audio too short, using what we have.")
        start = 0
    else:
        # Avoid the very start/end which might be silence
        start = random.randint(0, total_samples - needed_samples)
        
    snippet = data[start : start + needed_samples]
    
    print(f"Extracting 5s snippet from {start/fs:.2f}s to {(start+needed_samples)/fs:.2f}s")
    sf.write(output_path, snippet, fs)
    return output_path

def identify_snippet(filepath):
    print(f"Sending {filepath} to {API_URL}...")
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(API_URL, files=files)
            
        if response.status_code == 200:
            print("\n--- API RESPONSE ---")
            print(response.json())
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    # 1. Find a WAV
    wav_file = get_random_wav_file()
    if not wav_file:
        print("No WAV files found in downloads/ to test with.")
        sys.exit(1)
        
    # 2. Create a snippet
    snippet_file = "test_snippet.wav"
    create_snippet(wav_file, snippet_file)
    
    # 3. Identify
    identify_snippet(snippet_file)
    
    # Cleanup
    if os.path.exists(snippet_file):
        os.remove(snippet_file)
