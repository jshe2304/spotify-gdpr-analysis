from __future__ import annotations

from collections.abc import Iterable
from html import escape
from pathlib import Path

from spotify_gdpr_analysis.analysis.temporal import (
    hourly_average_streams,
    monthly_average_streams,
    monthly_new_artists,
    monthly_unique_artists,
    weekday_average_streams,
)
from spotify_gdpr_analysis.analysis.top import top_albums, top_artists, top_songs
from spotify_gdpr_analysis.visualize.templates import render_page


def render_html_report(
    records: Iterable[dict],
    report_title: str = "Spotify GDPR Listening Report",
) -> str:
    """
    Return a complete HTML report for all available analyses.
    """
    records_list = list(records)

    songs = top_songs(records_list)
    albums = top_albums(records_list)
    artists = top_artists(records_list)
    weekday_averages = weekday_average_streams(records_list)
    monthly_averages = monthly_average_streams(records_list)
    hourly_averages = hourly_average_streams(records_list)
    monthly_artist_counts = monthly_unique_artists(records_list)
    monthly_new_artist_counts = monthly_new_artists(records_list)
    monthly_artist_labels = _year_only_labels(
        [label for label, _ in monthly_artist_counts]
    )
    monthly_new_artist_labels = _year_only_labels(
        [label for label, _ in monthly_new_artist_counts]
    )

    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    month_labels = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    hour_labels = [f"{hour:02d}" for hour in range(24)]

    html_sections = [
        _render_table_section(
            "Top songs",
            ["Track", "Artist", "Plays"],
            [[track, artist, _format_count(count)] for track, artist, count in songs],
        ),
        _render_table_section(
            "Top albums",
            ["Album", "Artist", "Plays"],
            [[album, artist, _format_count(count)] for album, artist, count in albums],
        ),
        _render_table_section(
            "Top artists",
            ["Artist", "Plays"],
            [[artist, _format_count(count)] for artist, count in artists],
        ),
        _render_chart_section(
            "Average listens by weekday",
            _render_bar_chart(
                weekday_labels,
                weekday_averages,
                "Average listens per weekday",
            ),
        ),
        _render_chart_section(
            "Average listens by month",
            _render_bar_chart(
                month_labels,
                monthly_averages,
                "Average listens per month",
            ),
        ),
        _render_chart_section(
            "Average listens by hour",
            _render_bar_chart(
                hour_labels,
                hourly_averages,
                "Average listens per hour",
            ),
        ),
        _render_chart_section(
            "Unique artists by month",
            _render_bar_chart(
                monthly_artist_labels,
                [count for _, count in monthly_artist_counts],
                "Unique artists per month",
            ),
        ),
        _render_chart_section(
            "New artists discovered by month",
            _render_bar_chart(
                monthly_new_artist_labels,
                [count for _, count in monthly_new_artist_counts],
                "New artists discovered per month",
            ),
        ),
    ]

    html_body = "\n".join(section for section in html_sections if section)
    return render_page(report_title, html_body)


def write_html_report(
    records: Iterable[dict],
    output_path: str | Path,
    report_title: str = "Spotify GDPR Listening Report",
) -> Path:
    """
    Write an HTML report to disk and return the written path.
    """
    file_path = Path(output_path)
    file_path.write_text(
        render_html_report(records, report_title),
        encoding="utf-8",
    )
    return file_path


def _render_table_section(title: str, headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header_cells = "".join(f"<th>{escape(header)}</th>" for header in headers)
    row_cells = []
    for row in rows:
        cells = "".join(f"<td>{escape(cell)}</td>" for cell in row)
        row_cells.append(f"<tr>{cells}</tr>")
    table_html = (
        f"<table><thead><tr>{header_cells}</tr></thead><tbody>{''.join(row_cells)}</tbody></table>"
    )
    safe_title = escape(title)
    return (
        "<section>"
        f"<details open><summary><h2>{safe_title}</h2></summary>{table_html}</details>"
        "</section>"
    )


def _render_chart_section(title: str, chart_html: str) -> str:
    return f"<section><h2>{escape(title)}</h2><div class='chart'>{chart_html}</div></section>"


def _year_only_labels(labels: list[str]) -> list[str]:
    return [label.split("-")[0] if label.endswith("-01") else "" for label in labels]


def _render_bar_chart(labels: list[str], values: list[float], chart_title: str) -> str:
    if not labels or not values or len(labels) != len(values):
        return ""

    chart_width = 760
    chart_height = 260
    padding = 32
    label_height = 36
    bar_gap = 2
    usable_height = chart_height - padding - label_height - 8
    bar_count = len(values)
    bar_width = (chart_width - padding * 2 - bar_gap * (bar_count - 1)) / bar_count
    maximum_value = max(values) if values else 0

    gridlines = []
    for idx in range(1, 4):
        y = padding + (usable_height * idx / 4)
        gridlines.append(f"<line class='gridline' x1='{padding}' x2='{chart_width - padding}' y1='{y}' y2='{y}' />")

    bars = []
    labels_html = []
    for index, (label, value) in enumerate(zip(labels, values)):
        height = 0 if maximum_value == 0 else (value / maximum_value) * usable_height
        x = padding + index * (bar_width + bar_gap)
        y = padding + usable_height - height
        safe_label = escape(label)
        formatted_value = _format_float(value)
        bars.append(
            "<rect class='bar' "
            f"x='{x:.2f}' y='{y:.2f}' "
            f"width='{bar_width:.2f}' height='{height:.2f}'>"
            f"<title>{safe_label}: {formatted_value}</title>"
            "</rect>"
        )
        label_x = x + bar_width / 2
        label_y = chart_height - 10
        labels_html.append(
            "<text class='label' "
            f"x='{label_x:.2f}' y='{label_y:.2f}' "
            f"text-anchor='end' transform='rotate(45 {label_x:.2f} {label_y:.2f})'>"
            f"{safe_label}</text>"
        )

    safe_title = escape(chart_title)
    return (
        f"<svg viewBox='0 0 {chart_width} {chart_height}' role='img' aria-label='{safe_title}'>"
        f"<title>{safe_title}</title>"
        f"{''.join(gridlines)}{''.join(bars)}{''.join(labels_html)}</svg>"
    )


def _format_count(count: int) -> str:
    return f"{count:,}"


def _format_float(value: float) -> str:
    return f"{value:,.1f}"
