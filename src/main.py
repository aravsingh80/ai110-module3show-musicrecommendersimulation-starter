"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles through the recommender:
  - Three standard profiles (high-energy pop, chill lofi, intense rock)
  - Three adversarial/edge-case profiles to stress-test scoring logic
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "name": "High-Energy Pop",
    "genre": "pop",
    "mood": "happy",
    "energy": 0.85,
    "valence": 0.80,
}

CHILL_LOFI = {
    "name": "Chill Lofi",
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.38,
    "valence": 0.58,
}

DEEP_INTENSE_ROCK = {
    "name": "Deep Intense Rock",
    "genre": "rock",
    "mood": "intense",
    "energy": 0.91,
    "valence": 0.45,
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# ---------------------------------------------------------------------------

# Conflicting: high-energy target in a genre that only has low-energy songs
HIGH_ENERGY_FOLK = {
    "name": "EDGE: High-Energy Folk (conflicting energy vs genre)",
    "genre": "folk",
    "mood": "sad",
    "energy": 0.90,
    "valence": 0.35,
}

# Non-existent genre — should never earn genre points, reveals valence/energy fallback ranking
UNKNOWN_GENRE = {
    "name": "EDGE: Unknown Genre (k-pop not in catalog)",
    "genre": "k-pop",
    "mood": "happy",
    "energy": 0.75,
    "valence": 0.80,
}

# All numeric targets at dead-center 0.5 with a rare genre — exposes tie-breaking behaviour
PERFECTLY_NEUTRAL = {
    "name": "EDGE: Perfectly Neutral Ambient (ties on numerics)",
    "genre": "ambient",
    "mood": "relaxed",
    "energy": 0.50,
    "valence": 0.50,
}


ALL_PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    HIGH_ENERGY_FOLK,
    UNKNOWN_GENRE,
    PERFECTLY_NEUTRAL,
]


def run_profile(songs, profile, k=5):
    """Print top-k recommendations for a single user profile."""
    user_prefs = {k: v for k, v in profile.items() if k != "name"}
    label = profile["name"]

    print("=" * 60)
    print(f"  Profile : {label}")
    print(f"  Genre   : {user_prefs.get('genre')}  |  Mood: {user_prefs.get('mood')}")
    print(f"  Energy  : {user_prefs.get('energy')}  |  Valence: {user_prefs.get('valence')}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=k)

    if not recommendations:
        print("  No recommendations returned.\n")
        return

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}  |  Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"     Why   : {explanation}")
    print()


def main():
    songs = load_songs("data/songs.csv")

    print("\n" + "#" * 60)
    print("#   MUSIC RECOMMENDER — STRESS TEST (6 profiles)       #")
    print("#" * 60 + "\n")

    for profile in ALL_PROFILES:
        run_profile(songs, profile, k=5)


if __name__ == "__main__":
    main()
