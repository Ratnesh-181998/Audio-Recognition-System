# record_and_identify.py
"""Client script to record audio and query the Shazam API."""

import sys
import time
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np

# Configuration
API_URL = "http://127.0.0.1:5000/identify"
DURATION = 5  # Seconds to record
SAMPLE_RATE = 22050
FILENAME = "query_snippet.wav"

def record_audio(duration, fs, filename):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    
    # Save as WAV
    sf.write(filename, recording, fs)
    return filename

def identify_song(filename):
    print("Sending to server for identification...")
    try:
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(API_URL, files=files)
            
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                match = result["match"]
                print("\n🎉 MATCH FOUND! 🎉")
                print(f"Title:  {match['title']}")
                print(f"Artist: {match['artist']}")
                print(f"Album:  {match['album']}")
                print(f"Score:  {match['score']}")
            else:
                print("\n❌ No match found.")
                print(f"Score: {result.get('score')}")
        else:
            print(f"Error: Server returned {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    # Force UTF-8 for stdout to avoid Unicode errors on Windows
    sys.stdout.reconfigure(encoding='utf-8')

    try:
        record_audio(DURATION, SAMPLE_RATE, FILENAME)
        identify_song(FILENAME)
    except KeyboardInterrupt:
        print("\nAborted.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
