from __future__ import annotations

import argparse
from pathlib import Path

from spotify_gdpr_analysis.io.streaming_history import streaming_history
from spotify_gdpr_analysis.visualize.report import write_html_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an HTML report from Spotify GDPR streaming history exports.",
    )
    parser.add_argument(
        "data_dir",
        help="Directory containing Streaming_History_Audio_*.json files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="spotify_report.html",
        help="Output HTML path (default: spotify_report.html).",
    )
    parser.add_argument(
        "--title",
        default="Spotify GDPR Listening Report",
        help="Custom report title.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    output_path = Path(args.output)
    records = streaming_history(args.data_dir)
    write_html_report(records, output_path, args.title)
    print(f"Wrote report to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
