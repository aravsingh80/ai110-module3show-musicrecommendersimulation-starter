# Reflection — Music Recommender Simulation

## Profile Pair 1: High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile (energy 0.85, valence 0.80) and the Chill Lofi
profile (energy 0.38, valence 0.58) produced completely non-overlapping top-5
lists — not a single song appeared in both. This makes sense: the energy
targets are on opposite ends of the 0–1 scale, and genre locks each list into
a different corner of the catalog. What was interesting is that the Chill Lofi
list showed catalog skew visibly: 3 of its 5 results were lofi songs, while the
Pop list could only fill 2 pop slots (the catalog has 2 pop songs). Both lists
backfilled with mood-matching songs once genre options were exhausted.

## Profile Pair 2: Deep Intense Rock vs. High-Energy Folk (edge case)

Both profiles asked for high energy (~0.91 vs. 0.90) and negative valence
(0.45 vs. 0.35), but pointed at very different genres. The Rock profile found
a near-perfect match (Storm Runner, 4.97) because the catalog contains exactly
one rock song that matches every signal. The Folk profile also put its only
genre match (Autumn Letters) at rank 1 — but with a score of only 4.38,
because that song's actual energy (0.31) is far from the user's target (0.90).
The key insight: the scoring system does not "know" that folk and high-energy
are contradictory. It just adds up points. A user who wanted intense folk would
get a quiet, sad song as their top result because the categorical signals (+3.0)
outweigh the energy mismatch penalty (−0.59). This is a real weakness.

## Profile Pair 3: Unknown Genre (k-pop) vs. Perfectly Neutral Ambient

These two edge cases expose different failure modes. The k-pop profile never
earns genre points, so its best possible score is 3.0 — the system silently
degrades without any indication to the user that their preferred genre is
missing. The Ambient profile does earn genre points, but only one ambient song
exists, so rank 1 is guaranteed by default regardless of whether the song
actually matches the numeric preferences well. Running the weight-shift
experiment (halving genre weight) caused the Ambient profile's rank-1 to flip
to a country song — proving that the ambient song's top position was held by
the genre weight alone, not because it was numerically close to the target.
Together, these two profiles show that catalog coverage and weight design are
inseparable: a weight that works well on a large catalog can produce misleading
results on a small one.
