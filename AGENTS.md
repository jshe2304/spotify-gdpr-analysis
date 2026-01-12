# Project Structure & Module Organization
- `data/` contains local Spotify export data (JSON)
- `src/spotify_gdpr_analysis/io/` contains data ingestion helpers
- `src/spotify_gdpr_analysis/analysis/` contains functions for computing analytics
- `tests/` contains some unit tests

# Coding style
- Prefer descriptive, unabbreviated variable names
- Only annotate types for function arguments and outputs. 
- Avoid being overly protective; for example, only use try and except when absolutely necessary. 

# Development guidelines
- Adhere to code's existing style except when asked for a complete rewrite. 
- Keep the dependency tree shallow (applies to modules, helper functions, etc. )
- If a script and a __init__.py have a discrepancy, fix the latter

# Data specifics
- The data is organized into json files, each containing a list of dicts
- Each dict contains metadata on one streamed song
- The most relevant keys are `ts`, `ms_played`, `master_metadata_track_name`, `master_metadata_album_artist_name`, `master_metadata_album_album_name`.
