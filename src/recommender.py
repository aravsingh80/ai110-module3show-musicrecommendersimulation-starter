import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio attributes."""
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
    """Represents a user's taste preferences for recommendation matching."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP recommender that scores and ranks Song objects against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, _song_to_dict(song))[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(user_prefs, _song_to_dict(song))
        return "; ".join(reasons) if reasons else "No strong matches"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass to a plain dict for use with score_song."""
    return {
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "valence": song.valence,
        "acousticness": song.acousticness,
    }


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; return (score, reasons)."""
    score = 0.0
    reasons = []

    # Categorical signals
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Numerical proximity: reward closeness rather than absolute value
    if "energy" in user_prefs and "energy" in song:
        pts = round(1.0 - abs(user_prefs["energy"] - song["energy"]), 2)
        score += pts
        reasons.append(f"energy proximity (+{pts:.2f})")

    if "valence" in user_prefs and "valence" in song:
        pts = round(1.0 - abs(user_prefs["valence"] - song["valence"]), 2)
        score += pts
        reasons.append(f"valence proximity (+{pts:.2f})")

    # Acoustic preference bonus
    if user_prefs.get("likes_acoustic") and "acousticness" in song:
        pts = round(song["acousticness"] * 0.5, 2)
        score += pts
        reasons.append(f"acoustic bonus (+{pts:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest-to-lowest, and return the top-k results."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    scored.sort(key=lambda x: x[1], reverse=True)

    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
