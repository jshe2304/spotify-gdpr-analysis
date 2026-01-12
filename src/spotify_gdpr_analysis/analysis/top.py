from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

_TRACK_KEY = "master_metadata_track_name"
_ARTIST_KEY = "master_metadata_album_artist_name"
_ALBUM_KEY = "master_metadata_album_album_name"


def _top_pair(records: Iterable[dict], left_key: str, right_key: str, limit: int) -> list[tuple]:
    counter: Counter = Counter()
    for record in records:
        left = record.get(left_key)
        right = record.get(right_key)
        if not left or not right:
            continue
        counter[(left, right)] += 1
    return counter.most_common(limit)


def _top_single(records: Iterable[dict], key: str, limit: int) -> list[tuple]:
    counter: Counter = Counter()
    for record in records:
        value = record.get(key)
        if not value:
            continue
        counter[value] += 1
    return counter.most_common(limit)


def top_songs(records: Iterable[dict], limit: int = 25) -> list[tuple[str, str, int]]:
    """
    Return the most-played songs as (track_name, artist_name, play_count).
    """
    counts = _top_pair(records, _TRACK_KEY, _ARTIST_KEY, limit)
    return [(track, artist, count) for (track, artist), count in counts]


def top_albums(records: Iterable[dict], limit: int = 25) -> list[tuple[str, str, int]]:
    """
    Return the most-played albums as (album_name, artist_name, play_count).
    """
    counts = _top_pair(records, _ALBUM_KEY, _ARTIST_KEY, limit)
    return [(album, artist, count) for (album, artist), count in counts]


def top_artists(records: Iterable[dict], limit: int = 25) -> list[tuple[str, int]]:
    """
    Return the most-played artists as (artist_name, play_count).
    """
    counts = _top_single(records, _ARTIST_KEY, limit)
    return [(artist, count) for artist, count in counts]
