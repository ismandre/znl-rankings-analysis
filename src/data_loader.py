"""Data loading utilities with caching."""

import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Dict, Optional
from .config import DATA_DIR, CLUB_NAME, FIRST_DIVISION_SEASONS, SECOND_DIVISION_SEASONS


@st.cache_data
def load_season_data(season: str, division: str) -> pd.DataFrame:
    """
    Load a single season's rankings CSV file.

    Args:
        season: Season identifier (e.g., "2024/25")
        division: Division number ("1" or "2")

    Returns:
        DataFrame with rankings data
    """
    # Convert season format: "2024/25" -> "24_25"
    # Handle different year formats properly
    parts = season.split("/")
    if len(parts) == 2:
        year1 = parts[0][-2:]  # Last 2 digits of first year
        year2 = parts[1][-2:]  # Last 2 digits of second year
        season_filename = f"{year1}_{year2}"
    else:
        season_filename = season

    filepath = Path(DATA_DIR) / f"{division}. ŽNL {season_filename} - rankings.csv"

    if not filepath.exists():
        raise FileNotFoundError(f"CSV file not found: {filepath}")

    df = pd.read_csv(filepath)

    if not validate_csv_structure(df):
        raise ValueError(f"Invalid CSV structure in {filepath}")

    return df


def validate_csv_structure(df: pd.DataFrame) -> bool:
    """
    Validate that CSV has required columns.

    Args:
        df: DataFrame to validate

    Returns:
        True if valid, False otherwise
    """
    required_columns = [
        'season', 'position', 'club', 'played',
        'wins', 'draws', 'losses',
        'goals_for', 'goals_against', 'goal_difference', 'points'
    ]
    return all(col in df.columns for col in required_columns)


def get_club_data(df: pd.DataFrame, club_name: str = CLUB_NAME) -> Optional[pd.Series]:
    """
    Extract a specific club's row from rankings DataFrame.

    Args:
        df: Rankings DataFrame
        club_name: Name of club to extract

    Returns:
        Series with club data, or None if not found
    """
    club_rows = df[df['club'] == club_name]
    if len(club_rows) == 0:
        return None
    return club_rows.iloc[0]


@st.cache_data
def load_all_seasons() -> Dict[str, pd.DataFrame]:
    """
    Load all seasons' data into a dictionary.

    Returns:
        Dictionary with season keys and DataFrame values
    """
    all_data = {}

    # Load first division seasons
    for season in FIRST_DIVISION_SEASONS:
        try:
            all_data[f"1-{season}"] = load_season_data(season, "1")
        except FileNotFoundError:
            st.warning(f"File not found for 1. ŽNL {season}")

    # Load second division seasons
    for season in SECOND_DIVISION_SEASONS:
        try:
            all_data[f"2-{season}"] = load_season_data(season, "2")
        except FileNotFoundError:
            st.warning(f"File not found for 2. ŽNL {season}")

    return all_data
