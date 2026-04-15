"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

WIDTH = 57


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Header
    print()
    print("=" * WIDTH)
    print(f"  Top {len(recommendations)} Recommendations")
    print(
        f"  Profile: genre={user_prefs['genre']}"
        f"  |  mood={user_prefs['mood']}"
        f"  |  energy={float(user_prefs['energy']):.1f}"
    )
    print("=" * WIDTH)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  by  {song['artist']}")
        print(f"       Score : {score:.2f} / 4.00")
        for reason in reasons:
            print(f"         * {reason}")
        print("  " + "-" * (WIDTH - 2))

    print()


if __name__ == "__main__":
    main()
