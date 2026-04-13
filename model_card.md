# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder tries to answer the question: *"Given what a user says they like,
which songs in the catalog match them best?"*

It suggests up to 5 songs ranked from best match to worst. It does not learn
from listening history — it only uses what the user explicitly says they want
(genre, mood, energy, and positivity level).

---

## 3. Data Used

- **Size:** 18 songs, hand-crafted for classroom use.
- **Features per song:** genre, mood, energy (0–1), tempo (BPM), valence (0–1),
  danceability (0–1), acousticness (0–1).
- **Genres covered:** pop, lofi, rock, jazz, ambient, synthwave, indie pop,
  hip-hop, r&b, metal, country, classical, reggae, electronic, folk (15 total).
- **Moods covered:** happy, chill, intense, relaxed, focused, moody, romantic,
  angry, energetic, sad.
- **Limits:** The dataset is tiny. Lofi has 3 songs; most genres have only 1.
  There are no rap, classical sub-genres, international styles, or spoken word
  songs. The catalog reflects a narrow slice of musical taste.

---

## 4. Algorithm Summary

Every song gets a score out of 5.0. The score has four parts:

1. **Genre match (+2.0)** — If the song's genre matches what the user asked
   for, add 2 points. Genre is the biggest signal because it's the clearest
   "vibe gate."
2. **Mood match (+1.0)** — If the mood label matches, add 1 point. Mood
   fine-tunes within a genre.
3. **Energy closeness (up to +1.0)** — The closer the song's energy is to the
   user's target, the more points it earns. An exact match gives 1.0; a song
   that is completely opposite gives 0.
4. **Valence closeness (up to +1.0)** — Same idea but for positivity/mood tone.

All 18 songs are scored, then sorted from highest to lowest. The top 5 are
returned with a plain-English explanation of why each song scored what it did.

---

## 5. Observed Behavior / Biases

**Genre dominance is the biggest pattern.** Because genre is worth 2×
everything else, a song can win rank 1 even if its numeric features are a poor
match. In testing, a folk/sad song (energy 0.31) ranked first for a user
asking for energy 0.90 — just because the genre and mood labels matched.

**Catalog skew favors lofi listeners.** Lofi has 3 songs; a lofi user gets a
full, varied top-5. A metal or classical user exhausts their genre in one slot
and gets genre-mismatched songs filling ranks 2–5.

**No cross-genre discovery.** Genre is matched as an exact string. A hip-hop
fan will never see an r&b song, even if the two songs are sonically similar.

**Missing genres silently degrade results.** If a user's favorite genre is not
in the catalog (e.g., k-pop), the system never awards genre points. The best
possible score drops from 5.0 to 3.0, but nothing tells the user this happened.

---

## 6. Evaluation Process

Six user profiles were run through the system — three standard and three
adversarial (designed to find edge cases):

| Profile | Rank-1 Score | Key Finding |
|---|---|---|
| High-Energy Pop | 4.93 / 5.0 | Near-perfect match; genre dominance visible at rank 2 |
| Chill Lofi | 4.95 / 5.0 | Catalog skew: 3 of 5 results were lofi songs |
| Deep Intense Rock | 4.97 / 5.0 | Only 1 rock song; rank 2 scored only 2.88 |
| High-Energy Folk (edge) | 4.38 / 5.0 | Genre+mood weight rescued a low-energy song to rank 1 |
| Unknown Genre k-pop (edge) | 2.98 / 3.0 | No genre points possible; max score silently capped |
| Perfectly Neutral Ambient (edge) | 3.63 / 5.0 | Rank 1 held by genre weight alone |

**Weight-shift experiment:** Genre weight was halved (2.0 → 1.0) and energy
weight was doubled (1.0 → 2.0). The Ambient profile's rank-1 flipped from the
ambient song to a country song, confirming that the genre weight — not numeric
fit — was keeping it at the top under the original settings.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Classroom exploration of how content-based recommenders score and rank items.
- Understanding how weights encode design decisions and trade-offs.
- Learning how catalog size and categorical features affect output quality.

**Not intended for:**
- Real music recommendations for actual listeners.
- Any production or consumer-facing product.
- Representing any musical community or cultural taste fairly — the 18-song
  catalog is too small and too narrow for that.
- Making decisions about what music "people like you" enjoy, which could
  reinforce stereotypes if the genre/mood labels were tied to identity.

---

## 8. Ideas for Improvement

1. **Diversity penalty:** Prevent the same artist or genre from taking more
   than 2 of the 5 slots. This would force the system to surface variety even
   when one genre dominates the numeric rankings.

2. **Genre similarity table:** Instead of exact-string matching, assign partial
   credit for related genres (e.g., hip-hop and r&b share 0.5 genre points).
   This would help users whose favorite genre has few catalog entries.

3. **Warn when genre is missing:** If the user's preferred genre does not exist
   in the catalog, print a message like "Genre 'k-pop' not found — showing best
   matches by mood and energy instead."

---

## 9. Personal Reflection

**Biggest learning moment:** The weight-shift experiment was the clearest "aha"
moment. I expected halving the genre weight to cause minor reshuffling. Instead,
for the Perfectly Neutral Ambient profile, rank 1 flipped entirely to a
different song from a different genre. That showed me that weights are not just
tuning knobs — they decide *which kind of match wins*, not just *by how much*.

**How AI tools helped, and when I needed to double-check:** AI-generated
suggestions for adversarial profiles (like "high-energy + sad mood" or "genre
not in catalog") were genuinely useful — they pointed at failure modes I would
not have thought to test first. But I had to verify every suggestion against the
actual songs.csv to confirm the edge case was real. When the tool suggested
testing "conflicting preferences," I had to check whether any song in the
catalog actually had that combination before knowing the test would produce an
interesting result.

**What surprised me about simple algorithms:** The system is just addition and
absolute value, but the output still *feels* like a recommendation. When
"Sunrise City" scores 4.93 for the High-Energy Pop profile, it reads as
intentional curation even though it is just arithmetic. That gap — between what
the algorithm is doing and what a user would experience — is where a lot of AI
risk lives. Users trust the output without seeing the math.

**What I would try next:** I would add a second scoring pass that penalizes
repetitive results and forces at least one "surprise" song — a song that scores
moderately on genre but unusually well on energy or valence. Real recommenders
call this a serendipity or discovery layer, and it would make VibeFinder feel
less like a filter and more like a DJ.
