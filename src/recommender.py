from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["energy"]           = float(row["energy"])
            row["tempo_bpm"]        = float(row["tempo_bpm"])
            row["valence"]          = float(row["valence"])
            row["danceability"]     = float(row["danceability"])
            row["acousticness"]     = float(row["acousticness"])
            row["speechiness"]      = float(row["speechiness"])
            row["instrumentalness"] = float(row["instrumentalness"])
            songs.append(row)
    return songs


def _score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Returns (score, explanation) for a single song against a user profile."""
    score = 0.0
    reasons = []

    # Genre match — worth 20 % of the total (halved from 40 %)
    if song["genre"] == user_prefs["genre"]:
        score += 0.20
        reasons.append("genre match")

    # Mood match — worth 30 %
    if song["mood"] == user_prefs["mood"]:
        score += 0.30
        reasons.append("mood match")

    # Energy proximity — worth up to 40 % (doubled from 20 %)
    energy_similarity = 1.0 - abs(song["energy"] - user_prefs["energy"])
    score += energy_similarity * 0.40
    reasons.append(f"energy ~{song['energy']:.2f}")

    # Acoustic bonus — worth 10 % when the user likes acoustic songs
    if user_prefs.get("likes_acoustic") and song["acousticness"] >= 0.60:
        score += 0.10
        reasons.append("acoustic")

    explanation = ", ".join(reasons)
    return round(score, 4), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(_score_song(user_prefs, song), song) for song in songs]
    scored.sort(key=lambda x: x[0][0], reverse=True)
    return [(song, score, explanation) for (score, explanation), song in scored[:k]]
