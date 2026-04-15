"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# ─── User Profiles ───────────────────────────────────────────────────────────

PROFILES = {
    # ── Standard profiles ─────────────────────────────────────────────────────
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
    "Late-Night R&B": {
        "genre": "r&b",
        "mood": "romantic",
        "energy": 0.55,
        "likes_acoustic": False,
    },
    "Acoustic Folk Wanderer": {
        "genre": "folk",
        "mood": "melancholic",
        "energy": 0.30,
        "likes_acoustic": True,
    },

    # ── Adversarial / edge-case profiles ─────────────────────────────────────
    # Tests whether the scorer handles contradictory signals gracefully.
    # High energy is strongly correlated with upbeat moods in most catalogs;
    # pairing it with "sad" reveals whether genre/mood/energy weights fight
    # each other or one silently dominates.
    "Energetic Sadness": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.90,
        "likes_acoustic": False,
    },

    # Acoustic guitars and stadium-level energy almost never coexist.
    # Exposes whether likes_acoustic is ever penalised for high-energy songs
    # or simply ignored when no acoustic+high-energy songs exist.
    "Acoustic Maximalist": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": True,
    },

    # Energy at the absolute floor — tests boundary handling (no division by
    # zero, no negative scores) and whether very quiet songs float to the top.
    "Absolute Silence": {
        "genre": "ambient",
        "mood": "chill",
        "energy": 0.0,
        "likes_acoustic": True,
    },

    # A genre almost certainly absent from the catalog. Reveals whether an
    # unmatched genre collapses to zero score for every song (making the
    # ranking arbitrary) or if energy/mood still meaningfully separate songs.
    "Phantom Genre": {
        "genre": "bossa_nova",
        "mood": "happy",
        "energy": 0.60,
        "likes_acoustic": True,
    },

    # All signals at 0.5 with no strong preference — tests whether the scorer
    # still produces a meaningful, non-tied ranking or returns everything at
    # the same score, making the top-k selection arbitrary.
    "Perfectly Neutral": {
        "genre": "pop",
        "mood": "chill",
        "energy": 0.50,
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
