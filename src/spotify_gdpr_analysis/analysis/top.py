from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterable

_TRACK_KEYS = ("master_metadata_track_name",)
_ARTIST_KEYS = ("master_metadata_album_artist_name",)
_ALBUM_KEYS = ("master_metadata_album_album_name",)


def _first_nonempty(record: dict, keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = record.get(key)
        if value:
            return value
    return None

def _top_by_key(
    records: Iterable[dict],
    key_fn: Callable[[dict], tuple | str | None],
    limit: int,
) -> list[tuple]:
    counter: Counter = Counter()
    for record in records:
        key = key_fn(record)
        if key is None:
            continue
        counter[key] += 1
    return counter.most_common(limit)


def top_songs(records: Iterable[dict], limit: int = 100) -> list[tuple[str, str, int]]:
    """
    Return the most-played songs as (track_name, artist_name, play_count).
    """
    def key_fn(record: dict) -> tuple | None:
        track = _first_nonempty(record, _TRACK_KEYS)
        artist = _first_nonempty(record, _ARTIST_KEYS)
        if not track or not artist:
            return None
        return (track, artist)

    counts = _top_by_key(records, key_fn, limit)
    return [(track, artist, count) for (track, artist), count in counts]


def top_albums(records: Iterable[dict], limit: int = 100) -> list[tuple[str, str, int]]:
    """
    Return the most-played albums as (album_name, artist_name, play_count).
    """
    def key_fn(record: dict) -> tuple | None:
        album = _first_nonempty(record, _ALBUM_KEYS)
        artist = _first_nonempty(record, _ARTIST_KEYS)
        if not album or not artist:
            return None
        return (album, artist)

    counts = _top_by_key(records, key_fn, limit)
    return [(album, artist, count) for (album, artist), count in counts]


def top_artists(records: Iterable[dict], limit: int = 100) -> list[tuple[str, int]]:
    """
    Return the most-played artists as (artist_name, play_count).
    """
    def key_fn(record: dict) -> str | None:
        return _first_nonempty(record, _ARTIST_KEYS)

    counts = _top_by_key(records, key_fn, limit)
    return [(artist, count) for artist, count in counts]
