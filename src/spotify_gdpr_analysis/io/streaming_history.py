from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

def load_streaming_history_json(path: str | Path) -> list[dict]:
    """
    Load a streaming history JSON file and validate contents.
    """

    # Load file
    
    file_path = Path(path)
    with file_path.open("r") as handle:
        data = json.load(handle)

    # Validate json format

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of records in {file_path}, got {type(data).__name__}")
    
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(
                f"Expected dict records in {file_path}, item {idx} is {type(item).__name__}"
            )
    
    return data

def streaming_history(data_dir: str | Path) -> Iterator[dict]:
    """
    Iterate over streaming history JSON files and yield contents.
    """
    base = Path(data_dir)
    streaming_history_paths = sorted(base.glob("Streaming_History_Audio_*.json"))

    for path in streaming_history_paths:
        records = load_streaming_history_json(path)
        yield from records
