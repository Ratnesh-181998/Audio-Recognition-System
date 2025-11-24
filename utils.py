# utils.py
"""Utility functions for the Shazam prototype."""

import json
import os

DATABASE_FILE = "database.json"

def load_database():
    """Load the song database from the JSON file."""
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(data):
    """Save the song database to the JSON file."""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def find_matches(query_hashes, database):
    """Find the best matching song in the database.
    
    Returns a tuple (best_match_song, match_score).
    Score is simply the number of matching hashes.
    """
    best_match = None
    max_score = 0
    
    # Convert query hashes to a set for O(1) lookups
    query_set = set(query_hashes)
    
    for song in database:
        song_hashes = set(song.get("fingerprints", []))
        # Count intersection
        score = len(query_set.intersection(song_hashes))
        
        if score > max_score:
            max_score = score
            best_match = song
            
    return best_match, max_score
