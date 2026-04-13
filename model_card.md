# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests up to 5 songs from an 18-song catalog based on a user's
preferred genre, mood, target energy level, and target valence (positivity).
It is designed for classroom exploration of how content-based recommenders work.
It is not intended for real users or production deployment.

---

## 3. How the Model Works

Every song in the catalog gets a score based on how well it matches what the
user said they want. The score has four parts:

- **Genre match** adds 2 points — the biggest reward in the system, because
  genre is the broadest signal of musical style.
- **Mood match** adds 1 point — refines within a genre (e.g., "chill" vs
  "focused" within lofi).
- **Energy proximity** adds up to 1 point — a song earns full credit if its
  energy exactly matches the user's target, and less credit the further away it
  is.
- **Valence proximity** adds up to 1 point — same idea, but for how
  positive/melancholy the music sounds.

The maximum possible score is 5.0. All 18 songs are scored and the top 5 are
returned in order from highest to lowest.

---

## 4. Data

The catalog has 18 songs spanning 15 genres: pop, lofi, rock, jazz, ambient,
synthwave, indie pop, hip-hop, r&b, metal, country, classical, reggae,
electronic, and folk. Moods include happy, chill, intense, relaxed, focused,
moody, romantic, angry, energetic, and sad.

The data is small and hand-crafted, so it does not represent the full range of
musical taste. Lofi has 3 songs (the most of any genre); most genres have only
1 song. No songs were removed from the starter dataset.

---

## 5. Strengths

- Works well for users whose preferred genre is **lofi** — three matching songs
  give the catalog enough variety to fill a ranked list meaningfully.
- The scoring is fully transparent: every recommendation comes with a plain-text
  explanation of exactly which signals fired and how many points each added.
- Perfect-match profiles (e.g., "Deep Intense Rock" targeting Storm Runner's
  exact values) produce near-perfect scores (4.97/5.0), confirming the math is
  correct.
- Handles graceful degradation — if a genre does not exist in the catalog (e.g.,
  k-pop), the system still returns reasonable results ranked by mood and numeric
  proximity instead of crashing.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** Genre is worth 2× any other
signal, so a song with the perfect energy and valence but a different genre will
almost always rank below an on-genre song with mediocre numerics. In the
High-Energy Folk edge case, "Autumn Letters" ranked first even though its
energy (0.31) was far from the user's target (0.90) — the +3.0 from genre and
mood alone overwhelmed the energy penalty.

**Catalog skew amplifies popular genres.** Lofi listeners consistently receive
more on-genre options (3 songs) than fans of metal, jazz, country, or classical
(1 song each). A lofi user has more variety in their top-5 than a metal user
who exhausts their genre in one slot.

**Categorical rigidity prevents cross-genre discovery.** Genre and mood are
matched as exact strings. A "hip-hop" user will never match an "r&b" song even
if the two are acoustically similar. There is no concept of genre closeness.

**No diversity enforcement.** The system can return 5 nearly identical songs
(e.g., three lofi/chill songs with energy ≈ 0.38) with no mechanism to spread
results across different artists or moods.

**Unknown genres silently degrade quality.** When a user's preferred genre does
not appear in the catalog, the maximum achievable score drops from 5.0 to 3.0
with no warning to the user.

---

## 7. Evaluation

Six user profiles were tested — three standard and three adversarial:

| Profile | Rank-1 Score | Key Finding |
|---|---|---|
| High-Energy Pop | 4.93 | Near-perfect match; genre dominance clear in rank 2 |
| Chill Lofi | 4.95 | Catalog skew: 3 of top 5 are lofi |
| Deep Intense Rock | 4.97 | Only 1 rock song; huge gap to rank 2 (2.88) |
| High-Energy Folk (edge) | 4.38 | Genre weight overrides energy mismatch |
| Unknown Genre k-pop (edge) | 2.98 | Max score capped at 3.0; no genre points possible |
| Perfectly Neutral Ambient (edge) | 3.63 | Genre beats mood; rank 1 flipped in weight experiment |

**Weight-shift experiment:** Halving the genre weight (2.0 → 1.0) and doubling
the energy weight (1.0 → 2.0) caused the Perfectly Neutral Ambient profile's
rank-1 result to flip from the ambient song (genre match) to a country song
(mood match + strong energy proximity). This confirmed that the genre weight is
load-bearing — it controls which signal "wins" in close races.

---

## 8. Future Work

- Add a **diversity penalty** so the same artist or genre cannot dominate all
  5 slots.
- Replace exact-string genre matching with a **genre similarity table** (e.g.,
  hip-hop and r&b score partial credit for each other).
- Expand the catalog to at least 5 songs per genre so every user type gets
  meaningful variety.
- Support **multi-preference profiles** (e.g., "I like both lofi and jazz") by
  scoring against multiple genre targets and taking the maximum.
- Add **tempo range matching** as a fifth numeric signal.

---

## 9. Personal Reflection

Building VibeFinder 1.0 showed how a handful of weights can quietly encode
strong assumptions. Giving genre twice the value of any other signal was an
intuitive design choice — but running the adversarial profiles revealed that
this single decision lets a "folk + sad" song beat every high-energy song in
the catalog for a user who asked for energy 0.9. Real recommenders face the
same trade-off at much larger scale: every weight is a value judgment about
what matters most to a listener. The experiment also highlighted how catalog
size shapes perceived quality — a lofi listener experiences a richer, more
varied recommender than a metal listener using the exact same code, purely
because of how many songs were added to songs.csv.
