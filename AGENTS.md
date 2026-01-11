# Repository Guidelines

## Project Structure & Module Organization
- `src/spotify_gdpr_analysis/io/` contains ingestion helpers for Spotify GDPR exports (e.g., streaming history loaders).
- `data/` contains local Spotify export data (JSON/PDF). Treat as private, do not commit new personal exports.
- `README.md` is a brief project overview. 

# Coding Style & Naming Conventions
- Prefer descriptive, domain-focused names. 
- Keep modules small and composable; use iterators for large datasets.
- Keep the dependency tree shallow. This applies to modules, helper functions, etc. 

# Data Notes
- The project targets `endsong_*.json` files exclusively.
- Relevant keys are `ts`, `ms_played`, `master_metadata_track_name`, `master_metadata_album_artist_name`, `master_metadata_album_album_name`.
- Podcast entries use `episode_name` and `episode_show_name` instead of track metadata.
