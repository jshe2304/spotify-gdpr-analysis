import unittest
from pathlib import Path

from spotify_gdpr_analysis.io.streaming_history import streaming_history


class TestStreamingHistory(unittest.TestCase):
    def test_streaming_history_has_thousands_of_entries(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        data_dir = repo_root / "data" / "01-11-2026"

        self.assertTrue(data_dir.exists(), f"Missing expected data directory: {data_dir}")

        record_count = sum(1 for _ in streaming_history(data_dir))

        self.assertGreaterEqual(
            record_count,
            2000,
            f"Expected at least 2000 streaming history entries, got {record_count}",
        )

    def test_streaming_history_sample_record_schema(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        data_dir = repo_root / "data" / "01-11-2026"

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

        self.assertTrue(expected_keys.issubset(record.keys()))
        self.assertIsInstance(record["ts"], str)
        self.assertIsInstance(record["platform"], str)
        self.assertIsInstance(record["ms_played"], int)
        self.assertIsInstance(record["conn_country"], str)
        self.assertTrue(
            record["ip_addr"] is None or isinstance(record["ip_addr"], str),
            f"Unexpected type for ip_addr: {type(record['ip_addr']).__name__}",
        )
        self.assertIsInstance(record["reason_start"], str)
        self.assertIsInstance(record["reason_end"], str)
        self.assertIsInstance(record["shuffle"], bool)
        self.assertIsInstance(record["offline"], bool)
        self.assertTrue(
            record["offline_timestamp"] is None
            or isinstance(record["offline_timestamp"], int),
            f"Unexpected type for offline_timestamp: {type(record['offline_timestamp']).__name__}",
        )
        self.assertIsInstance(record["incognito_mode"], bool)

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
            self.assertTrue(
                record[key] is None or isinstance(record[key], str),
                f"Unexpected type for {key}: {type(record[key]).__name__}",
            )

        self.assertTrue(
            record["skipped"] is None or isinstance(record["skipped"], bool),
            f"Unexpected type for skipped: {type(record['skipped']).__name__}",
        )
