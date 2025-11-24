# app.py
"""Flask API for the Shazam prototype.

Endpoints:
- POST /identify: Accepts an audio file, fingerprints it, and returns the best match.
- POST /ingest: Accepts an audio file and metadata, fingerprints it, and adds it to the DB.
"""

import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import fingerprint
import utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/identify', methods=['POST'])
def identify_song():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # 1. Generate fingerprints
            hashes = fingerprint.fingerprint_file(filepath)
            
            # 2. Load DB and find match
            db = utils.load_database()
            match, score = utils.find_matches(hashes, db)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            if match and score > 5: # Threshold for a valid match
                return jsonify({
                    "status": "success",
                    "match": {
                        "title": match["title"],
                        "artist": match["artist"],
                        "album": match["album"],
                        "score": score
                    }
                })
            else:
                return jsonify({"status": "no_match", "score": score})
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/ingest', methods=['POST'])
def ingest_song():
    """Add a new song to the database."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    metadata = request.form
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            hashes = fingerprint.fingerprint_file(filepath)
            
            new_song = {
                "id": f"song_{len(utils.load_database()) + 1}",
                "title": metadata.get("title", "Unknown"),
                "artist": metadata.get("artist", "Unknown"),
                "album": metadata.get("album", "Unknown"),
                "year": metadata.get("year", ""),
                "fingerprints": list(hashes)
            }
            
            db = utils.load_database()
            db.append(new_song)
            utils.save_database(db)
            
            os.remove(filepath)
            
            return jsonify({"status": "success", "message": f"Added {new_song['title']}"})
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
