from pathlib import Path

from spotify_gdpr_analysis.io.streaming_history import streaming_history


def _data_dir() -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / "data" / "01-11-2026"


def test_streaming_history_has_thousands_of_entries() -> None:
    data_dir = _data_dir()
    assert data_dir.exists(), f"Missing expected data directory: {data_dir}"

    record_count = sum(1 for _ in streaming_history(data_dir))

    assert (
        record_count >= 2000
    ), f"Expected at least 2000 streaming history entries, got {record_count}"


def test_streaming_history_sample_record_schema() -> None:
    data_dir = _data_dir()

    record = next(streaming_history(data_dir))

    expected_keys = {
        "ts",
        "platform",
        "ms_played",
        "conn_country",
        "ip_addr",
        "master_metadata_track_name",
        "master_metadata_album_artist_name",
        "master_metadata_album_album_name",
        "spotify_track_uri",
        "episode_name",
        "episode_show_name",
        "spotify_episode_uri",
        "audiobook_title",
        "audiobook_uri",
        "audiobook_chapter_uri",
        "audiobook_chapter_title",
        "reason_start",
        "reason_end",
        "shuffle",
        "skipped",
        "offline",
        "offline_timestamp",
        "incognito_mode",
    }

    assert expected_keys.issubset(record.keys())
    assert isinstance(record["ts"], str)
    assert isinstance(record["platform"], str)
    assert isinstance(record["ms_played"], int)
    assert isinstance(record["conn_country"], str)
    assert record["ip_addr"] is None or isinstance(record["ip_addr"], str), (
        f"Unexpected type for ip_addr: {type(record['ip_addr']).__name__}"
    )
    assert isinstance(record["reason_start"], str)
    assert isinstance(record["reason_end"], str)
    assert isinstance(record["shuffle"], bool)
    assert isinstance(record["offline"], bool)
    assert record["offline_timestamp"] is None or isinstance(
        record["offline_timestamp"], int
    ), f"Unexpected type for offline_timestamp: {type(record['offline_timestamp']).__name__}"
    assert isinstance(record["incognito_mode"], bool)

    for key in (
        "master_metadata_track_name",
        "master_metadata_album_artist_name",
        "master_metadata_album_album_name",
        "spotify_track_uri",
        "episode_name",
        "episode_show_name",
        "spotify_episode_uri",
        "audiobook_title",
        "audiobook_uri",
        "audiobook_chapter_uri",
        "audiobook_chapter_title",
    ):
        assert record[key] is None or isinstance(record[key], str), (
            f"Unexpected type for {key}: {type(record[key]).__name__}"
        )

    assert record["skipped"] is None or isinstance(record["skipped"], bool), (
        f"Unexpected type for skipped: {type(record['skipped']).__name__}"
    )
