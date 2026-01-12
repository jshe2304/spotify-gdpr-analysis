"""
A collection of numerical, temporal analytics. 

By temporal, we mean that, if plotted, the data has time on the x-axis. 
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from datetime import datetime
from zoneinfo import ZoneInfo

_TIMEZONE = ZoneInfo("America/Los_Angeles")
_ARTIST_KEY = "master_metadata_album_artist_name"

def weekday_average_streams(records: Iterable[dict]) -> list[float]:
    """
    Return average listens per weekday across weeks (Mon=0 .. Sun=6).
    """
    counters = defaultdict(Counter)

    for record in records:
        timestamp = record.get('ts').replace("Z", "+00:00")
        dt = datetime.fromisoformat(timestamp).astimezone(_TIMEZONE)
        week = dt.isocalendar()
        counters[(week.year, week.week)][dt.weekday()] += 1

    totals = Counter()
    for week_counter in counters.values():
        totals.update(week_counter)

    weeks_count = len(counters)
    return [totals.get(day, 0) / weeks_count for day in range(7)]

def monthly_average_streams(records: Iterable[dict]) -> list[float]:
    """
    Return average listens per month across years (Jan=1 .. Dec=12).
    """
    counters = defaultdict(Counter)

    for record in records:
        timestamp = record.get('ts').replace("Z", "+00:00")
        dt = datetime.fromisoformat(timestamp).astimezone(_TIMEZONE)
        counters[dt.year][dt.month] += 1

    totals = Counter()
    for year_counter in counters.values():
        totals.update(year_counter)

    years_count = len(counters)
    return [totals.get(month, 0) / years_count for month in range(1, 13)]


def hourly_average_streams(records: Iterable[dict]) -> list[float]:
    """
    Return average listens per hour across days (0 .. 23).
    """
    counters = defaultdict(Counter)

    for record in records:
        timestamp = record.get("ts").replace("Z", "+00:00")
        dt = datetime.fromisoformat(timestamp).astimezone(_TIMEZONE)
        counters[dt.date()][dt.hour] += 1

    totals = Counter()
    for day_counter in counters.values():
        totals.update(day_counter)

    days_count = len(counters)
    return [totals.get(hour, 0) / days_count for hour in range(24)]


def monthly_unique_artists(records: Iterable[dict]) -> list[tuple[str, int]]:
    """
    Return unique artist counts per month as (YYYY-MM, count).
    """
    monthly_artists: dict[tuple[int, int], set[str]] = defaultdict(set)

    for record in records:
        timestamp = record.get("ts").replace("Z", "+00:00")
        dt = datetime.fromisoformat(timestamp).astimezone(_TIMEZONE)
        artist_name = record.get(_ARTIST_KEY)
        if not artist_name:
            continue
        monthly_artists[(dt.year, dt.month)].add(artist_name)

    monthly_counts = []
    for (year, month) in sorted(monthly_artists):
        label = f"{year}-{month:02d}"
        monthly_counts.append((label, len(monthly_artists[(year, month)])))
    return monthly_counts


def monthly_new_artists(records: Iterable[dict]) -> list[tuple[str, int]]:
    """
    Return new artist counts per month as (YYYY-MM, count).
    """
    first_seen: dict[str, tuple[int, int]] = {}

    for record in records:
        timestamp = record.get("ts").replace("Z", "+00:00")
        dt = datetime.fromisoformat(timestamp).astimezone(_TIMEZONE)
        artist_name = record.get(_ARTIST_KEY)
        if not artist_name:
            continue
        month_key = (dt.year, dt.month)
        if artist_name not in first_seen or month_key < first_seen[artist_name]:
            first_seen[artist_name] = month_key

    monthly_counts: Counter = Counter(first_seen.values())
    return [
        (f"{year}-{month:02d}", monthly_counts[(year, month)])
        for (year, month) in sorted(monthly_counts)
    ]
