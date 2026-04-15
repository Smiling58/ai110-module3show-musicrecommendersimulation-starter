"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ─── User Profiles ───────────────────────────────────────────────────────────

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
}


# ─── Runner ──────────────────────────────────────────────────────────────────

def print_recommendations(label: str, recommendations: list) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {label}")
    print(f"{'─' * 50}")
    if not recommendations:
        print("  (no recommendations returned yet)")
        return
    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score: {score:.2f}  |  {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, recommendations)

    print()


if __name__ == "__main__":
    main()
