"""Reusable Plotly visualization components."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from .config import COLORS, CHART_CONFIG, CHART_LAYOUT


def apply_chart_styling(fig: go.Figure, title: str) -> go.Figure:
    """
    Apply consistent styling to Plotly charts.

    Args:
        fig: Plotly figure object
        title: Chart title

    Returns:
        Styled figure
    """
    fig.update_layout(
        title=title,
        **CHART_LAYOUT,
        hovermode='x unified'
    )
    return fig


def create_position_timeline(summary_df: pd.DataFrame) -> go.Figure:
    """
    Create line chart showing position over seasons (inverted Y-axis).

    Args:
        summary_df: Season summary DataFrame

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=summary_df['season'],
        y=summary_df['position'],
        mode='lines+markers',
        marker=dict(size=10, color=COLORS['primary']),
        line=dict(color=COLORS['primary'], width=3),
        hovertemplate='<b>%{x}</b><br>Position: %{y}<extra></extra>'
    ))

    fig.update_yaxes(
        autorange='reversed',
        title='Pozicija na ljestvici',
        dtick=1
    )
    fig.update_xaxes(title='Sezona')

    return apply_chart_styling(fig, 'Pozicija na ljestvici kroz vrijeme')


def create_points_bar_chart(summary_df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart of points earned per season.

    Args:
        summary_df: Season summary DataFrame

    Returns:
        Plotly figure
    """
    # Color bars differently for incomplete seasons
    colors = [COLORS['warning'] if incomplete else COLORS['secondary']
              for incomplete in summary_df['is_incomplete']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=summary_df['season'],
        y=summary_df['points'],
        marker=dict(color=colors),
        hovertemplate='<b>%{x}</b><br>Points: %{y}<extra></extra>'
    ))

    fig.update_yaxes(title='Bodovi')
    fig.update_xaxes(title='Sezona')

    return apply_chart_styling(fig, 'Osvojeni bodovi po sezoni')


def create_goals_comparison(summary_df: pd.DataFrame) -> go.Figure:
    """
    Create grouped bar chart comparing goals for vs against.

    Args:
        summary_df: Season summary DataFrame

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Postignuti golovi',
        x=summary_df['season'],
        y=summary_df['goals_for'],
        marker=dict(color=COLORS['goals_for']),
        hovertemplate='<b>%{x}</b><br>Postignuto: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Primljeni golovi',
        x=summary_df['season'],
        y=summary_df['goals_against'],
        marker=dict(color=COLORS['goals_against']),
        hovertemplate='<b>%{x}</b><br>Primljeno: %{y}<extra></extra>'
    ))

    fig.update_layout(barmode='group')
    fig.update_yaxes(title='Golovi')
    fig.update_xaxes(title='Sezona')

    return apply_chart_styling(fig, 'Postignuti vs Primljeni golovi')


def create_ppg_line_chart(summary_df: pd.DataFrame) -> go.Figure:
    """
    Create line chart showing points per game trend.

    Args:
        summary_df: Season summary DataFrame

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    # Split into complete and incomplete for different styling
    complete = summary_df[~summary_df['is_incomplete']]
    incomplete = summary_df[summary_df['is_incomplete']]

    if len(complete) > 0:
        fig.add_trace(go.Scatter(
            x=complete['season'],
            y=complete['ppg'],
            mode='lines+markers',
            name='Završene sezone',
            marker=dict(size=10, color=COLORS['primary']),
            line=dict(color=COLORS['primary'], width=3),
            hovertemplate='<b>%{x}</b><br>Bod. po utakmici: %{y:.2f}<extra></extra>'
        ))

    if len(incomplete) > 0:
        fig.add_trace(go.Scatter(
            x=incomplete['season'],
            y=incomplete['ppg'],
            mode='markers',
            name='Sezona u tijeku',
            marker=dict(size=12, color=COLORS['warning'], symbol='diamond'),
            hovertemplate='<b>%{x}</b><br>Bod. po utakmici: %{y:.2f} (u tijeku)<extra></extra>'
        ))

    fig.update_yaxes(title='Bodova po utakmici')
    fig.update_xaxes(title='Sezona')

    return apply_chart_styling(fig, 'Trend bodova po utakmici')


def create_championship_comparison_radar(champ_df: pd.DataFrame) -> go.Figure:
    """
    Create radar chart comparing two championship seasons.

    Args:
        champ_df: Championship seasons DataFrame (2 rows)

    Returns:
        Plotly figure
    """
    if len(champ_df) != 2:
        return go.Figure()

    # Normalize metrics to 0-100 scale for radar chart
    metrics = ['points', 'goals_for', 'wins', 'ppg']
    labels = ['Bodovi', 'Postignuti golovi', 'Pobjede', 'Bod/ut (×10)']

    fig = go.Figure()

    for idx, row in champ_df.iterrows():
        values = [
            row['points'],
            row['goals_for'],
            row['wins'],
            row['ppg'] * 10  # Scale PPG to be visible
        ]
        values.append(values[0])  # Close the radar

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels + [labels[0]],
            fill='toself',
            name=row['season']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(champ_df['goals_for'].max(), champ_df['points'].max())])
        ),
        showlegend=True,
        **CHART_LAYOUT
    )

    return apply_chart_styling(fig, 'Usporedba prvačkih sezona')


def create_league_positions_trajectory(all_seasons: list, data_seasons: list, division: str = "1", selected_clubs: list = None) -> go.Figure:
    """
    Create interactive trajectory graph showing all clubs' positions across seasons.

    Args:
        all_seasons: List of ALL season identifiers to show on x-axis
        data_seasons: List of seasons to actually load data from
        division: Division number ("1" or "2")
        selected_clubs: List of club names to display (None = show only NK Hajduk 1932)

    Returns:
        Plotly figure with interactive club trajectories
    """
    from .data_loader import load_season_data
    from .config import DATA_DIR, CLUB_CONFIGS, ASSETS_DIR
    from PIL import Image
    import base64
    from io import BytesIO
    import os

    # Collect all club position data (only from data_seasons)
    club_data = {}  # {club_name: {season: position}}
    max_teams = 0  # Track maximum number of teams across all seasons

    for season in data_seasons:
        try:
            df = load_season_data(season, division)
            # Update max teams count
            max_teams = max(max_teams, len(df))

            for _, row in df.iterrows():
                club = row['club']
                position = int(row['position'])

                if club not in club_data:
                    club_data[club] = {}
                club_data[club][season] = position
        except:
            continue

    # Create figure
    fig = go.Figure()

    # Default color for clubs not in config
    default_color = '#6B7280'

    # Sort clubs by total appearances (more appearances = more prominent)
    club_appearances = {club: len(positions) for club, positions in club_data.items()}
    sorted_clubs = sorted(club_appearances.items(), key=lambda x: x[1], reverse=True)

    # Function to convert image to base64
    def image_to_base64(image_path):
        try:
            with Image.open(image_path) as img:
                # Resize logo
                img = img.resize((30, 30), Image.Resampling.LANCZOS)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                return f"data:image/png;base64,{img_str}"
        except Exception as e:
            return None

    # Default to showing only NK Hajduk 1932 if no selection provided
    if selected_clubs is None:
        selected_clubs = ["NK Hajduk 1932"]

    # Store all logo images that will be added to layout
    layout_images = []

    # Map season to x-coordinate index (for image positioning)
    season_to_x = {season: idx for idx, season in enumerate(all_seasons)}

    # Add trace for each club
    for idx, (club, _) in enumerate(sorted_clubs):
        positions = club_data[club]

        # Skip clubs that appear in less than 2 seasons
        if len([s for s in all_seasons if s in positions]) < 2:
            continue

        # Check if this club should be displayed
        should_display = club in selected_clubs

        # Get club config (color and logo)
        club_config = CLUB_CONFIGS.get(club, {"primary_color": default_color, "logo": ""})
        club_color = club_config.get("primary_color", default_color)
        club_logo_path = club_config.get("logo", "")

        # Convert logo to base64
        logo_base64 = None
        if club_logo_path and should_display:
            # Construct absolute path to logo
            # Logo path in config is like "assets/nk_gusar_komin.png"
            # Extract just the filename and construct full path
            if club_logo_path.startswith("assets/"):
                logo_filename = club_logo_path.replace("assets/", "")
                absolute_logo_path = os.path.join(ASSETS_DIR, logo_filename)
            else:
                absolute_logo_path = club_logo_path

            logo_base64 = image_to_base64(absolute_logo_path)

        # Create lists for x (seasons) and y (positions)
        x_values = []
        y_values = []
        hover_text = []

        for season in all_seasons:
            if season in positions:
                x_values.append(season)
                y_values.append(positions[season])
                hover_text.append(f"<b>{club}</b><br>Sezona: {season}<br>Pozicija: {positions[season]}")

                # Add logo image at this data point if available and club is selected
                if logo_base64:
                    layout_images.append(dict(
                        source=logo_base64,
                        xref="x",
                        yref="y",
                        x=season,
                        y=positions[season],
                        sizex=0.4,  # Size in x-axis units
                        sizey=0.8,  # Size in y-axis units
                        xanchor="center",
                        yanchor="middle",
                        layer="above",
                        visible=True  # Only add logos for selected clubs
                    ))

        # Determine if this is NK Hajduk 1932 (make it more prominent)
        is_hajduk = "NK Hajduk 1932" in club or "Hajduk 1932" in club
        line_width = 4 if is_hajduk else 2.5

        # Add trace - only lines, no markers (logos will be the markers)
        # Set visibility based on selection
        trace_visible = True if should_display else 'legendonly'

        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values,
            mode='lines',
            name=club,
            line=dict(width=line_width, color=club_color),
            connectgaps=False,
            hovertemplate='%{text}<extra></extra>',
            text=hover_text,
            visible=trace_visible,
            customdata=[club] * len(x_values)  # Store club name for later reference
        ))

    # Update layout with logo images
    fig.update_layout(
        title='Kretanje klubova kroz pozicije po sezonama',
        xaxis_title='Sezona',
        yaxis_title='Pozicija',
        yaxis=dict(
            autorange=False,
            range=[max_teams + 0.5, 0.5],
            dtick=1,
            gridcolor='#E5E7EB',
            tickmode='linear',
            tick0=1
        ),
        xaxis=dict(
            gridcolor='#E5E7EB',
            categoryorder='array',
            categoryarray=all_seasons
        ),
        hovermode='closest',
        showlegend=False,  # Legend removed - use dropdown menu instead
        images=layout_images,  # Add logo images
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='sans-serif', size=12),
        margin=dict(l=80, r=80, t=80, b=50),  # Extra horizontal margin for logos
        height=600
    )

    # Add update mechanism to show/hide logos when traces are toggled
    # This is handled by Plotly's built-in legend interaction

    return fig


def create_win_loss_pie(season_data: pd.Series) -> go.Figure:
    """
    Create pie chart of wins/draws/losses for a season.

    Args:
        season_data: Single season row with wins, draws, losses

    Returns:
        Plotly figure
    """
    labels = ['Pobjede', 'Neriješeno', 'Porazi']
    values = [season_data['wins'], season_data['draws'], season_data['losses']]
    colors = [COLORS['success'], COLORS['text_light'], COLORS['danger']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>%{value} utakmica<br>%{percent}<extra></extra>'
    )])

    fig.update_layout(**CHART_LAYOUT)

    return fig
