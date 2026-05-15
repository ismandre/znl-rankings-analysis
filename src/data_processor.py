"""Data processing and transformation utilities."""

import pandas as pd
from typing import Dict
from .config import CLUB_NAME, FIRST_DIVISION_SEASONS, SECOND_DIVISION_SEASONS, INCOMPLETE_SEASONS
from .data_loader import load_season_data, get_club_data


def calculate_points_per_game(points: int, played: int) -> float:
    """Calculate points per game."""
    if played == 0:
        return 0.0
    return round(points / played, 2)


def prepare_first_division_summary() -> pd.DataFrame:
    """
    Aggregate all 1. ŽNL seasons data for NK Hajduk 1932.

    Returns:
        DataFrame with columns: season, position, total_teams, points,
        goals_for, goals_against, played, ppg, is_incomplete
    """
    summary_data = []

    for season in FIRST_DIVISION_SEASONS:
        try:
            df = load_season_data(season, "1")
            club_data = get_club_data(df, CLUB_NAME)

            if club_data is None:
                continue

            summary_data.append({
                'season': season,
                'position': int(club_data['position']),
                'total_teams': len(df),
                'points': int(club_data['points']),
                'goals_for': int(club_data['goals_for']),
                'goals_against': int(club_data['goals_against']),
                'played': int(club_data['played']),
                'wins': int(club_data['wins']),
                'draws': int(club_data['draws']),
                'losses': int(club_data['losses']),
                'ppg': calculate_points_per_game(club_data['points'], club_data['played']),
                'is_incomplete': season in INCOMPLETE_SEASONS
            })
        except Exception as e:
            print(f"Error loading {season}: {e}")
            continue

    return pd.DataFrame(summary_data)


def prepare_second_division_summary() -> pd.DataFrame:
    """
    Aggregate all 2. ŽNL championship seasons data.

    Returns:
        DataFrame with same structure as first division summary
    """
    summary_data = []

    for season in SECOND_DIVISION_SEASONS:
        try:
            df = load_season_data(season, "2")
            club_data = get_club_data(df, CLUB_NAME)

            if club_data is None:
                continue

            summary_data.append({
                'season': season,
                'position': int(club_data['position']),
                'total_teams': len(df),
                'points': int(club_data['points']),
                'goals_for': int(club_data['goals_for']),
                'goals_against': int(club_data['goals_against']),
                'played': int(club_data['played']),
                'wins': int(club_data['wins']),
                'draws': int(club_data['draws']),
                'losses': int(club_data['losses']),
                'ppg': calculate_points_per_game(club_data['points'], club_data['played']),
                'is_incomplete': False
            })
        except Exception as e:
            print(f"Error loading {season}: {e}")
            continue

    return pd.DataFrame(summary_data)


def get_league_context(season_df: pd.DataFrame, club_position: int) -> Dict:
    """
    Get league context information (champion, relegation zone, etc.).

    Args:
        season_df: Full league table DataFrame
        club_position: NK Hajduk 1932's position

    Returns:
        Dictionary with context information
    """
    champion = season_df[season_df['position'] == 1].iloc[0]
    club_row = season_df[season_df['position'] == club_position].iloc[0]
    total_teams = len(season_df)

    context = {
        'champion': champion['club'],
        'champion_points': int(champion['points']),
        'champion_played': int(champion['played']),
        'champion_ppg': round(champion['points'] / champion['played'], 2),
        'club_points': int(club_row['points']),
        'club_played': int(club_row['played']),
        'club_ppg': round(club_row['points'] / club_row['played'], 2),
        'points_from_top': int(champion['points'] - club_row['points']),
        'total_teams': total_teams
    }

    # Relegation zone - typically last 2 positions for leagues with 10+ teams, last 1 for smaller leagues
    relegation_positions = 2 if total_teams >= 10 else 1
    safe_position = total_teams - relegation_positions

    # Get the team in the last safe position (just above relegation)
    if safe_position > 0 and safe_position <= total_teams:
        safe_team = season_df[season_df['position'] == safe_position].iloc[0]
        context['safe_points'] = int(safe_team['points'])
        context['safe_played'] = int(safe_team['played'])
        context['safe_ppg'] = round(safe_team['points'] / safe_team['played'], 2)
        context['relegation_positions'] = relegation_positions

    return context


def calculate_season_trends(summary_df: pd.DataFrame) -> Dict:
    """
    Calculate trends and statistics across seasons.

    Args:
        summary_df: Aggregated season data

    Returns:
        Dictionary with trend statistics
    """
    # Filter out incomplete seasons for some calculations
    complete_df = summary_df[~summary_df['is_incomplete']]

    trends = {
        'best_position': int(summary_df['position'].min()),
        'best_position_season': summary_df.loc[summary_df['position'].idxmin(), 'season'],
        'worst_position': int(summary_df['position'].max()),
        'worst_position_season': summary_df.loc[summary_df['position'].idxmax(), 'season'],
        'highest_points': int(complete_df['points'].max()) if len(complete_df) > 0 else 0,
        'highest_points_season': complete_df.loc[complete_df['points'].idxmax(), 'season'] if len(complete_df) > 0 else 'N/A',
        'total_goals_scored': int(summary_df['goals_for'].sum()),
        'total_goals_conceded': int(summary_df['goals_against'].sum()),
        'average_ppg': round(complete_df['ppg'].mean(), 2) if len(complete_df) > 0 else 0,
        'total_matches': int(summary_df['played'].sum()),
        'total_wins': int(summary_df['wins'].sum()),
        'total_draws': int(summary_df['draws'].sum()),
        'total_losses': int(summary_df['losses'].sum())
    }

    return trends
