# 🎧 Model Card: Music Recommender Simulation

## Model Name

**VibeFinder 1.0**

---

## Goal / Task

VibeFinder suggests songs that match a user's mood, genre, and energy level.
It ranks a catalog of songs from most to least compatible with a given user profile.
It does not learn from feedback — it scores each song using fixed rules.

---

## Data Used

- 20 songs in the catalog
- 10+ genres: pop, lofi, rock, ambient, jazz, hip-hop, folk, metal, EDM, and more
- 10+ moods: happy, chill, intense, melancholic, euphoric, romantic, and more
- Each song has 9 features: genre, mood, energy, tempo, valence, danceability, acousticness, speechiness, instrumentalness
- Genre coverage is uneven — lofi has 3 songs, most genres have only 1
- No world music, K-pop, or Latin genres are represented

---

## Algorithm Summary

The scorer checks four things for each song and adds up points:

| Signal | Max Points | How it works |
|---|---|---|
| Genre match | 20 | +20 if genre label matches exactly |
| Mood match | 30 | +30 if mood label matches exactly |
| Energy proximity | 40 | Closer energy = more points (continuous, not binary) |
| Acoustic bonus | 10 | +10 if user likes acoustic and song is 60%+ acoustic |

Max possible score: **100 points.**
Songs are sorted highest to lowest. The top 5 are returned.

Genre was originally worth 40 points. After testing, it was reduced to 20 and energy raised to 40 — genre was overriding mood and energy results in a way that felt wrong.

---

## Observed Behavior / Biases

**Genre acts like a filter, not a preference.**
With only 1–2 songs per genre, the genre match sends those songs straight to the top regardless of mood.

**Low-energy users are penalized by the catalog.**
The quietest song has energy 0.22. A user targeting 0.0 always has a gap — the score reflects the catalog's limit, not the user's fit.

**Acoustic preference only rewards, never penalizes.**
There is no deduction when a non-acoustic user gets an acoustic song recommended. The signal only works in one direction.

**Exact matching creates a cliff.**
`"indie pop" ≠ "pop"` scores zero. `"relaxed" ≠ "chill"` scores zero. Adjacent genres and moods are treated the same as opposites.

**The system never subtracts points.**
Even a completely wrong song earns partial energy-proximity credit and can appear in the top 5.

---

## Evaluation Process

Ten profiles were tested — 5 standard, 5 adversarial:

| Profile | Purpose |
|---|---|
| High-Energy Pop | Baseline — clear preferences, well-represented genre |
| Chill Lofi | Low energy, acoustic — multiple lofi songs available |
| Deep Intense Rock | Single-genre test — only one rock song exists |
| Late-Night R&B | Mid-energy, romantic mood |
| Acoustic Folk Wanderer | Low energy + acoustic bonus combined |
| Energetic Sadness | Conflicting signals — high energy but sad mood |
| Acoustic Maximalist | Impossible combo — high energy and acoustic |
| Absolute Silence | Boundary test — energy target of 0.0 |
| Phantom Genre | Unknown genre — "bossa_nova" matches nothing |
| Perfectly Neutral | Weak signal — mid energy, common genre |

**Biggest surprise:** The Perfectly Neutral profile (pop, chill, 0.50 energy) returned two happy/intense pop songs at the top. The mood was completely wrong. Genre match alone pushed them there.

**Phantom Genre worked better than expected.** With no genre matches, the list ranked entirely by mood and energy — which was actually more honest than some standard profiles.

**The Gym Hero problem:** Gym Hero (mood: intense) kept appearing for happy pop users. Genre matched, energy was close — the system had no way to penalize the mood mismatch.

---

## Intended Use and Non-Intended Use

**Intended for:**
- Learning how content-based recommenders work
- Classroom experiments with scoring weights and user profiles
- Exploring bias and tradeoffs in simple ranking systems

**Not intended for:**
- Real music discovery or production deployment
- Users with tastes outside the 20-song catalog
- Any context where fairness across user types is required

---

## Ideas for Improvement

1. **Fuzzy genre and mood matching.** "Indie pop" should earn partial credit toward "pop." "Relaxed" and "chill" should be near-synonyms. A small lookup table would fix the cliff-edge problem.

2. **Normalize energy against the catalog range.** Score energy relative to the actual min and max in the catalog, not the full 0–1 scale. This removes the structural penalty for low-energy users.

3. **Add a mismatch penalty.** Subtract small points for a clearly wrong mood or an acoustic song shown to a non-acoustic user. This pushes bad matches to the bottom instead of letting them coast on energy proximity.

---

## Personal Reflection

**Biggest learning moment**

Changing two numbers — genre weight from 0.40 to 0.20, energy from 0.20 to 0.40 — completely changed whose preferences the system respected.
No logic changed. No new features. Just two values.
That was the moment I understood that weights are not neutral. They encode priorities, and users have no idea those priorities exist.

**How AI tools helped — and where I had to push back**

The AI helped me move fast. It implemented `load_songs` and `recommend_songs`, set up all ten user profiles, and filled out sections of this card based on what we had already discussed together.

But I had to catch it more than once.
When it tried to add a whole new section header to reorganize my screenshot images, I stopped it — I just wanted the caption text changed, nothing else.
When it wrote the first draft of this model card, the sentences were too long and academic. I rejected it and asked for plain language.
When the scoring logic was first implemented in an earlier version of the project, it was reverted because the approach was wrong.

The pattern was consistent: the AI moved confidently but not always correctly. Reading the output critically and knowing when something "felt off" was just as important as letting it generate.

**What surprised me about simple algorithms**

I expected something this basic to feel broken — like it would just return random songs.
It did not. The results actually felt personalized, at least for the standard profiles.
That was surprising. Add up four signals, sort the list, and suddenly it seems like the system "knows" something about you.
What I now understand is that it does not know anything. It is just arithmetic. The "feeling" comes from the user reading their own preferences back through song titles they already recognize.

**What I would extend next**

I would add fuzzy mood matching first. The fact that "chill" and "relaxed" score zero overlap is the most obviously wrong thing in the system.
After that I would grow the catalog significantly — at least five songs per genre — so genre stops acting like a filter and starts acting like a signal.
If I kept going, I would try adding a basic collaborative component: group users by similar profiles and see if their combined history surfaces songs that a single user's static preferences would never reach on their own.
