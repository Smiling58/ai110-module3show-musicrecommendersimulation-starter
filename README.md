# Music Recommender Simulation

## Project Summary

This project is a small music recommender system that suggests songs from a catalog based on a user's taste profile. It models how real-world recommender systems (like Spotify or YouTube Music) turn structured data about songs and listeners into ranked suggestions.

The system represents songs as data objects with audio features (genre, mood, energy, tempo, valence, danceability, acousticness, speechiness, instrumentalness), stores a user's preferences in a profile, and applies a scoring function to rank the catalog for that user. The catalog contains 20 songs spanning 10 genres and 10 moods.

---

## How The System Works

### Song Features

Each `Song` in the catalog ([src/recommender.py](src/recommender.py)) stores:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical genre (e.g., pop, lofi, rock, jazz) |
| `mood` | string | Emotional tone (e.g., happy, chill, intense, moody) |
| `energy` | float (0–1) | How energetic or driving the track feels |
| `tempo_bpm` | float | Beats per minute |
| `valence` | float (0–1) | Musical positivity (high = upbeat, low = somber) |
| `danceability` | float (0–1) | How suitable the track is for dancing |
| `acousticness` | float (0–1) | How acoustic (vs. electronic) the track sounds |
| `speechiness` | float (0–1) | Presence of spoken words (high in rap/hip-hop, low in instrumentals) |
| `instrumentalness` | float (0–1) | Likelihood the track has no vocals (near 1.0 = purely instrumental) |

### User Profile

A `UserProfile` captures four preference signals:

- `favorite_genre` — the genre the user most wants to hear
- `favorite_mood` — the mood the user is in
- `target_energy` — their preferred energy level (0–1)
- `likes_acoustic` — whether they lean toward acoustic or electronic tracks

### Scoring Logic

The `Recommender` class and `recommend_songs` function score each song against the user profile. A song earns points for:

1. **Genre match** — does the song's genre match `favorite_genre`
2. **Mood match** — does the song's mood match `favorite_mood`
3. **Energy proximity** — how close `song.energy` is to `target_energy`
4. **Acoustic preference** — bonus if `likes_acoustic` aligns with a high `acousticness` value

The top `k` songs (default 5) with the highest scores are returned as recommendations, each with a short explanation of why it was chosen.

### Algorithm Recipe

The finalized scoring function awards points per song as follows:

| Signal | Condition | Points |
|---|---|---|
| Genre match | `song.genre == user.favorite_genre` | +2.0 |
| Mood match | `song.mood == user.favorite_mood` | +1.0 |
| Energy proximity | `1.0 - abs(song.energy - user.target_energy)` | +0.0 – 1.0 |

**Maximum possible score: 4.0**

Genre is weighted highest (2×) because it represents the user's strongest declared preference. Mood is a secondary signal. Energy is continuous and always contributes something, preventing zero-score ties among songs that miss on both genre and mood.

**Potential biases to watch for:**

- **Genre over-prioritization** — A genre match alone (+2.0) outweighs a perfect mood + perfect energy combination (+2.0 max). A great song in the right mood at the exact right energy level will lose to a mediocre song that simply shares the user's genre.
- **Catalog imbalance** — 15 of 17 genres appear only once in this catalog. If a user's favorite genre is represented by a single song, that song ranks first unconditionally regardless of how well it actually fits the user's mood or energy.
- **Binary categorical matching** — `"indie pop"` and `"pop"` score zero for each other's genre match even though they heavily overlap. Same for moods like `"chill"` vs `"relaxed"`. Exact-string matching penalizes related categories.
- **No exclusion of already-heard songs** — The system has no memory of past recommendations, so the same top-k songs will surface every time for the same user profile.

### Recommendation Flow

```
data/songs.csv
      │
      ▼
 load_songs()  ──►  List[Song]
                         │
               UserProfile (genre, mood, energy, acoustic)
                         │
                         ▼
              recommend_songs() / Recommender.recommend()
                         │
                         ▼
         Top-k (song, score, explanation) tuples
```
![song_recommendation](image.png)
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

_Document the experiments you ran as you built and tuned the system. For example:_

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did results differ for a user who `likes_acoustic = True` vs. `False`
- How did the system handle edge cases like an empty catalog or an unknown genre

---

## Limitations and Risks

- **Small catalog** — the system has 20 songs across 10 genres; recommendations are still heavily constrained by what's available.
- **No collaborative filtering** — it only uses song attributes and a single user profile, not the listening history of similar users.
- **Binary genre/mood matching** — genre and mood are exact-match strings; "indie pop" and "pop" score as completely different even though they overlap.
- **Static user profile** — the system cannot learn or update as a user's taste changes over time.
- **Potential genre bias** — if most songs in the catalog are one genre, that genre will dominate recommendations regardless of user preference.

---

## Reflection

_Write 1–2 paragraphs here about what you learned:_

- How recommenders turn data (features, scores, rankings) into predictions
- Where bias or unfairness could emerge — for example, if the song catalog overrepresents certain genres or moods, or if energy-level weighting systematically disadvantages lower-energy listeners

---

## Model Card

See [model_card.md](model_card.md) for a full evaluation of the system's intended use, strengths, limitations, and ethical considerations.
