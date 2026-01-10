# Shazam‑like Audio Recognition Prototype

This repository contains a **minimal prototype** of the Shazam audio‑recognition system.

## 📖 Overview
- Record a short audio snippet (≈ 5 seconds) from a microphone.
- Convert the audio into a **spectrogram**, extract **spectral peaks**, and generate **hashes** (fingerprint).
- Look up the fingerprint in a **simple JSON database** of pre‑computed song fingerprints.
- Return the matching song's metadata (title, artist, album, year).

The implementation is deliberately lightweight and intended for **educational / demo** purposes – it is **not** a production‑grade Shazam clone.

## 📂 Project Structure
```
shazam_project/
├─ README.md                # This file
├─ requirements.txt         # Python dependencies
├─ fingerprint.py           # Core fingerprint generation
├─ database.json            # Simple fingerprint‑to‑metadata store
├─ database.example.json    # Example database structure
├─ app.py                   # Flask API exposing /identify and /ingest endpoints
├─ record_and_identify.py   # CLI tool to record audio and call the API
├─ ingest_youtube.py        # Script to download and ingest songs from YouTube
├─ test_with_file.py        # Test identification with an audio file
├─ reingest_all.py          # Reingest all downloaded songs
└─ utils.py                 # Helper utilities (audio loading, database operations)
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
cd shazam_project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

**Note:** You'll also need **FFmpeg** installed for audio processing:
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt-get install ffmpeg`

You'll also need **yt-dlp** for YouTube downloads:
```bash
pip install yt-dlp
```

### 3. Initialize the database
```bash
# Copy the example database structure
cp database.example.json database.json
```

### 4. Run the Flask server
```bash
python app.py
```
The server will listen on `http://127.0.0.1:5000`.

### 5. Ingest songs from YouTube
```bash
python ingest_youtube.py <youtube_url>
```
Example:
```bash
python ingest_youtube.py https://www.youtube.com/watch?v=jCVjudmnByk
```

### 6. Record and identify a song
```bash
python record_and_identify.py
```
Play a song for ~5 seconds; the script will send the audio to the server and print the result.

## 🎯 API Endpoints

### POST /identify
Identify a song from an audio file.

**Request:**
- `file`: Audio file (WAV, MP3, etc.)

**Response:**
```json
{
  "status": "success",
  "match": {
    "title": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name",
    "score": 139
  }
}
```

### POST /ingest
Add a new song to the database.

**Request:**
- `file`: Audio file (WAV, MP3, etc.)
- `title`: Song title (optional)
- `artist`: Artist name (optional)
- `album`: Album name (optional)
- `year`: Release year (optional)

**Response:**
```json
{
  "status": "success",
  "message": "Added Song Title"
}
```

## 📚 How It Works

### Audio Fingerprinting
1. **Spectrogram Generation:** Convert audio to a time-frequency representation using STFT
2. **Peak Detection:** Identify local maxima in the spectrogram
3. **Hash Generation:** Create unique hashes from pairs of peaks (anchor + target)
4. **Database Lookup:** Match hashes against the fingerprint database
5. **Scoring:** Count matching hashes and return the best match

### Architecture
```
Client (Microphone) → Flask API → Fingerprint Generator → Database Lookup → Match Result
```

## 🔧 Scripts

- **`app.py`**: Flask server with `/identify` and `/ingest` endpoints
- **`record_and_identify.py`**: Record audio from microphone and identify
- **`ingest_youtube.py`**: Download and ingest songs from YouTube
- **`test_with_file.py`**: Test identification with a local audio file
- **`reingest_all.py`**: Reingest all songs in the downloads folder
- **`fingerprint.py`**: Core fingerprinting logic
- **`utils.py`**: Database and audio utilities

## 📘 System Design Reference

This prototype implements a simplified version of the Shazam audio recognition system:

### Functional Requirements
1. Capture ~5–10 seconds of audio through the client microphone
2. Generate fingerprints from spectrogram peaks and search against the catalog
3. Return matching song metadata (title, artist, album, year)

### Non-Functional Requirements
- **Accuracy:** Fingerprinting tolerates moderate noise/distortion
- **Speed:** Near real-time identification (< 5 seconds)
- **Scalability:** In production, would use distributed hash stores (Cassandra/HBase)

### Main Flow
1. Client records audio snippet and uploads to server
2. Backend converts to mono 22.05 kHz, computes spectrogram, extracts peaks
3. Creates hash triples `(f1, f2, Δt)` from anchor–target peak pairs
4. Queries hashes against fingerprint database
5. Returns top matching song or "no match"

### Production Considerations
For a production system, you would need:
- Distributed fingerprint storage (Cassandra, HBase, DynamoDB)
- CDN for audio/metadata delivery
- Caching layer (Redis)
- Load balancing and horizontal scaling
- Robust noise handling and preprocessing
- Monitoring and analytics

---

**License:** MIT

*This prototype is built for demonstration and educational purposes only. Real-world deployment would require a massive, distributed fingerprint database, robust noise handling, caching, and many other engineering concerns.*


---


<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=24,20,12,6&height=3" width="100%">


## 📜 **License**

![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

**Licensed under the MIT License** - Feel free to fork and build upon this innovation! 🚀

---

# 📞 **CONTACT & NETWORKING** 📞


### 💼 Professional Networks

[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ratneshkumar1998/)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ratnesh-181998)
[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/RatneshS16497)
[![Portfolio](https://img.shields.io/badge/🌐_Portfolio-FF6B6B?style=for-the-badge&logo=google-chrome&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![Email](https://img.shields.io/badge/✉️_Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rattudacsit2021gate@gmail.com)
[![Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@rattudacsit2021gate)
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-F58025?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/32068937/ratnesh-kumar)

### 🚀 AI/ML & Data Science
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/user/ratnesh-181998)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/RattuDa98)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/rattuda)

### 💻 Competitive Programming
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/Ratnesh_1998/)
[![HackerRank](https://img.shields.io/badge/HackerRank-00EA64?style=for-the-badge&logo=hackerrank&logoColor=black)](https://www.hackerrank.com/profile/rattudacsit20211)
[![CodeChef](https://img.shields.io/badge/CodeChef-5B4638?style=for-the-badge&logo=codechef&logoColor=white)](https://www.codechef.com/users/ratnesh_181998)
[![Codeforces](https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/Ratnesh_181998)
[![GeeksforGeeks](https://img.shields.io/badge/GeeksforGeeks-2F8D46?style=for-the-badge&logo=geeksforgeeks&logoColor=white)](https://www.geeksforgeeks.org/profile/ratnesh1998)
[![HackerEarth](https://img.shields.io/badge/HackerEarth-323754?style=for-the-badge&logo=hackerearth&logoColor=white)](https://www.hackerearth.com/@ratnesh138/)
[![InterviewBit](https://img.shields.io/badge/InterviewBit-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://www.interviewbit.com/profile/rattudacsit2021gate_d9a25bc44230/)


---

## 📊 **GitHub Stats & Metrics** 📊



![Profile Views](https://komarev.com/ghpvc/?username=Ratnesh-181998&color=blueviolet&style=for-the-badge&label=PROFILE+VIEWS)





<img src="https://github-readme-streak-stats.herokuapp.com/?user=Ratnesh-181998&theme=radical&hide_border=true&background=0D1117&stroke=4ECDC4&ring=F38181&fire=FF6B6B&currStreakLabel=4ECDC4" width="48%" />




<img src="https://github-readme-activity-graph.vercel.app/graph?username=Ratnesh-181998&theme=react-dark&hide_border=true&bg_color=0D1117&color=4ECDC4&line=F38181&point=FF6B6B" width="48%" />

---

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&duration=3000&pause=1000&color=4ECDC4&center=true&vCenter=true&width=600&lines=Ratnesh+Kumar+Singh;Data+Scientist+%7C+AI%2FML+Engineer;4%2B+Years+Building+Production+AI+Systems" alt="Typing SVG" />

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=1000&color=F38181&center=true&vCenter=true&width=600&lines=Built+with+passion+for+the+AI+Community+🚀;Innovating+the+Future+of+AI+%26+ML;MLOps+%7C+LLMOps+%7C+AIOps+%7C+GenAI+%7C+AgenticAI+Excellence" alt="Footer Typing SVG" />


<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%">


