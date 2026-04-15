from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import csv

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


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Algorithm recipe:
      +2.0  genre match       (song["genre"] == user_prefs["genre"])
      +1.0  mood match        (song["mood"]  == user_prefs["mood"])
      +0.0–1.0  energy proximity  1 - abs(song["energy"] - user_prefs["energy"])

    Returns:
        score   — total numeric score (max 4.0)
        reasons — list of strings, one per signal, showing the label and
                  points awarded, e.g. ["genre match: pop (+2.0)",
                                        "energy proximity: 0.82 vs 0.80 (+0.98)"]
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Mood match: +1.0
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Energy proximity: 1 - abs(difference), result is between 0.0 and 1.0
    target_energy = float(user_prefs.get("energy", 0.5))
    energy_points = round(1.0 - abs(float(song["energy"]) - target_energy), 2)
    score += energy_points
    reasons.append(
        f"energy proximity: {float(song['energy']):.2f} vs target {target_energy:.2f} (+{energy_points:.2f})"
    )

    return round(score, 2), reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores the song catalog that will be scored on every recommend call."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song against the user profile and returns the top k sorted by score."""
        prefs = {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}
        scored = [
            (song, score_song(prefs, asdict(song))[0])
            for song in self.songs
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable sentence describing why a song was recommended."""
        prefs = {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}
        _, reasons = score_song(prefs, asdict(song))
        return "Recommended because: " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":               int(row["id"]),
                "title":            row["title"],
                "artist":           row["artist"],
                "genre":            row["genre"],
                "mood":             row["mood"],
                "energy":           float(row["energy"]),
                "tempo_bpm":        float(row["tempo_bpm"]),
                "valence":          float(row["valence"]),
                "danceability":     float(row["danceability"]),
                "acousticness":     float(row["acousticness"]),
                "speechiness":      float(row["speechiness"]),
                "instrumentalness": float(row["instrumentalness"]),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Recommending is ranking: score_song judges every song in the catalog,
    then we sort the full scored list to surface the top k results.

    Returns a list of (song, score, reasons) tuples where reasons is a list
    of strings — one per scoring signal that contributed points.
    The caller decides how to display them.
    """
    # Step 1: Judge every song in the catalog.
    # The inner `for score, reasons in [score_song(...)]` calls the function
    # once per song and unpacks both return values into the same expression.
    results = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # Step 2 & 3: Sort the full scored list high-to-low, then return the top k.
    return sorted(results, key=lambda x: x[1], reverse=True)[:k]
