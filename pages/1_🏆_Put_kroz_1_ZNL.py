"""Put kroz 1. ŽNL - Analiza 8 sezona u prvom rangu"""

import streamlit as st
import pandas as pd
import os
from src.config import (
    CLUB_NAME, INCOMPLETE_SEASONS, SHORTENED_SEASONS, COLORS,
    FIRST_DIVISION_SEASONS, SECOND_DIVISION_SEASONS, ASSETS_DIR
)
from src.data_loader import load_season_data, get_club_data
from src.data_processor import (
    prepare_first_division_summary,
    get_league_context,
    calculate_season_trends
)
from src.visualizations import (
    create_position_timeline,
    create_points_bar_chart,
    create_goals_comparison,
    create_ppg_line_chart,
    create_league_positions_trajectory
)

st.set_page_config(layout="wide", page_title="Put kroz 1. ŽNL", page_icon="🏆")

# Custom CSS
st.markdown("""
    <style>
    .ongoing-badge {
        background: #EF4444;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
    }
    .season-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .context-box {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .highlight-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .lowlight-box {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    logo_path = os.path.join(ASSETS_DIR, "nk_hajduk_1932.png")
    st.image(logo_path, width=120)
with col2:
    st.markdown("# Put kroz 1. ŽNL")
    st.markdown(f"""
    U proteklih deset godina, **{CLUB_NAME}** proveo je osam sezona natječući se u prvom rangu Dubrovačko-neretvanske županijske lige.
    Kakav rezultat je ostvaren tijekom tog razdoblja?
    """)

st.info("""
📋 **Napomena**: Ova analiza obuhvaća samo sezone u 1. ŽNL-u.
Klub je također nastupao u 2. ŽNL-u tijekom sezona **2021/22** i **2023/24** nakon ispadanja iz prvog ranga.
""")

st.markdown("---")

# Load data
summary_df = prepare_first_division_summary()
trends = calculate_season_trends(summary_df)

# Add missing seasons info
st.markdown("## 📅 Statistika po sezonama")

# Show timeline with missing seasons
st.markdown("""
**Kronologija nastupa:**
- 2016/17 - 2020/21: Pet uzastopnih sezona u 1. ŽNL-u
- **2021/22**: 📉 Ispadanje - Natjecanje u 2. ŽNL-u
- 2022/23: Povratak u 1. ŽNL
- **2023/24**: 📉 Ispadanje - Natjecanje u 2. ŽNL-u
- 2024/25 - 2025/26: Povratak i nastavak u 1. ŽNL-u
""")

for idx, row in summary_df.iterrows():
    season = row['season']
    is_incomplete = row['is_incomplete']
    is_shortened = season in SHORTENED_SEASONS

    # Load full league data for context
    try:
        league_df = load_season_data(season, "1")
        context = get_league_context(league_df, row['position'])
    except:
        context = None

    # Season header with badge if ongoing
    header_text = f"### {season}"
    if is_incomplete:
        header_text += " <span class='ongoing-badge'>U TIJEKU</span>"

    with st.expander(f"{season} - Pozicija {int(row['position'])}/{int(row['total_teams'])}", expanded=False):
        st.markdown(header_text, unsafe_allow_html=True)

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Pozicija na ljestvici",
                f"{int(row['position'])} / {int(row['total_teams'])}",
                delta=None
            )

        with col2:
            st.metric(
                "Bodovi",
                f"{int(row['points'])} bod.",
                delta=f"{row['ppg']:.2f} po utakmici"
            )

        with col3:
            st.metric(
                "Postignuti golovi",
                int(row['goals_for']),
                delta=None
            )

        with col4:
            goal_diff = int(row['goals_for'] - row['goals_against'])
            diff_color = "#10B981" if goal_diff > 0 else "#EF4444" if goal_diff < 0 else "#6B7280"
            diff_sign = "+" if goal_diff > 0 else ""
            st.metric(
                "Primljeni golovi",
                int(row['goals_against'])
            )
            st.markdown(f"""
            <div style="margin-top: -10px; font-size: 0.875rem;">
                <span style="color: {diff_color}; font-weight: 600;">{diff_sign}{goal_diff}</span>
                <span style="color: #6B7280;"> razlika</span>
            </div>
            """, unsafe_allow_html=True)

        # Record details with colored wins/draws/losses
        st.markdown(f"""
        **Učinak**: <span style="color: #10B981; font-weight: 600;">{int(row['wins'])}</span> -
        <span style="color: #F59E0B; font-weight: 600;">{int(row['draws'])}</span> -
        <span style="color: #EF4444; font-weight: 600;">{int(row['losses'])}</span>
        ({int(row['played'])} odigrano utakmica)
        """, unsafe_allow_html=True)

        if is_shortened:
            st.warning("⚠️ Ovo je bila skraćena sezona (zbog COVID-19)")

        if is_incomplete:
            remaining = 22 - row['played']
            st.info(f"🔄 Sezona u tijeku: {int(row['played'])}/22 odigrane utakmice (preostalo {remaining})")

        # League context
        if context:
            st.markdown("---")
            st.markdown("**Kontekst lige:**")
            st.markdown(f"""
            - 🏆 **Prvak**: {context['champion']} ({context['champion_points']} bod., {context['champion_ppg']:.2f} bod/ut)
            """)

            # Championship requirements vs club performance
            champ_diff = context['club_points'] - context['champion_points']
            champ_ppg_diff = context['club_ppg'] - context['champion_ppg']
            champ_color = "#10B981" if champ_diff >= 0 else "#EF4444"

            st.markdown(f"""
            - 📊 **Za osvajanje**: Potrebno {context['champion_points']} bod. ({context['champion_ppg']:.2f} bod/ut)
              → NK Hajduk 1932: {context['club_points']} bod. ({context['club_ppg']:.2f} bod/ut)
              <span style="color: {champ_color}; font-weight: 600;">({champ_diff:+d} bod., {champ_ppg_diff:+.2f} bod/ut razlike)</span>
            """, unsafe_allow_html=True)

            # Relegation safety requirements vs club performance
            if 'safe_points' in context:
                safe_diff = context['club_points'] - context['safe_points']
                safe_ppg_diff = context['club_ppg'] - context['safe_ppg']
                safe_color = "#10B981" if safe_diff >= 0 else "#EF4444"

                st.markdown(f"""
                - 🛡️ **Za ostanak**: Potrebno {context['safe_points']} bod. ({context['safe_ppg']:.2f} bod/ut)
                  → NK Hajduk 1932: {context['club_points']} bod. ({context['club_ppg']:.2f} bod/ut)
                  <span style="color: {safe_color}; font-weight: 600;">({safe_diff:+d} bod., {safe_ppg_diff:+.2f} bod/ut razlike)</span>
                """, unsafe_allow_html=True)

st.markdown("---")

# Performance Trends
st.markdown("## 📈 Trendovi učinka")

# League-wide position trajectories
st.markdown("### 🎯 Kretanje svih klubova kroz sezone")
st.info("""
💡 **Interaktivni graf**: Odaberite klubove koje želite prikazati na grafu.
Graf će prikazati njihove pozicije kroz sezone s njihovim logotipima.

**Napomena**: Graf prikazuje sve sezone (2016/17-2025/26), ali samo podatke iz 1. ŽNL-a.
Klubovi "nestaju" u sezonama kada su igrali u 2. ŽNL-u (npr. 2021/22, 2023/24).
""")

# Get all clubs that participated in 1. ŽNL
all_clubs = set()
for season in FIRST_DIVISION_SEASONS:
    try:
        df = load_season_data(season, "1")
        all_clubs.update(df['club'].tolist())
    except:
        continue

# Sort clubs alphabetically, but put NK Hajduk 1932 first
sorted_all_clubs = sorted(list(all_clubs))
if "NK Hajduk 1932" in sorted_all_clubs:
    sorted_all_clubs.remove("NK Hajduk 1932")
    sorted_all_clubs.insert(0, "NK Hajduk 1932")

# Multiselect for choosing which clubs to display
selected_clubs = st.multiselect(
    "Odaberite klubove za prikaz:",
    options=sorted_all_clubs,
    default=["NK Hajduk 1932"],
    help="Odaberite jedan ili više klubova da vidite njihove trajektorije i logotipe na grafu"
)

# Only show graph if at least one club is selected
if selected_clubs:
    # Combine all seasons chronologically for x-axis
    all_seasons_combined = sorted(list(set(FIRST_DIVISION_SEASONS + SECOND_DIVISION_SEASONS)))
    fig_trajectory = create_league_positions_trajectory(all_seasons_combined, FIRST_DIVISION_SEASONS, "1", selected_clubs)
    st.plotly_chart(fig_trajectory, use_container_width=True)
else:
    st.info("Molimo odaberite barem jedan klub za prikaz grafa.")

st.markdown("---")

# Individual team stats
st.markdown("### 📊 NK Hajduk 1932 - Detaljni trendovi")

col1, col2 = st.columns(2)

with col1:
    fig = create_position_timeline(summary_df)
    st.plotly_chart(fig, use_container_width=True)

    fig = create_goals_comparison(summary_df)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = create_points_bar_chart(summary_df)
    st.plotly_chart(fig, use_container_width=True)

    fig = create_ppg_line_chart(summary_df)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Statistical Highlights
st.markdown("## 🌟 Statistički vrhunci")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="highlight-box">
        <h3>🏅 Najbolja sezona</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {trends['best_position_season']}
        </p>
        <p style="font-size: 1.2rem;">
            Pozicija: {trends['best_position']}. | Bodova: {trends['highest_points']}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="lowlight-box">
        <h3>📉 Najslabija sezona</h3>
        <p style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">
            {trends['worst_position_season']}
        </p>
        <p style="font-size: 1.2rem;">
            Pozicija: {trends['worst_position']}.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Overall statistics
st.markdown("### 📊 Ukupna statistika (8 sezona)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ukupno utakmica", trends['total_matches'])
    st.metric("Ukupno bodova", int(summary_df['points'].sum()))

with col2:
    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <div style="font-size: 0.875rem; color: #6B7280;">Ukupan učinak</div>
        <div style="font-size: 1.875rem; font-weight: 600; margin-top: 0.5rem;">
            <span style="color: #10B981;">{trends['total_wins']}</span>
            <span style="color: #6B7280;"> - </span>
            <span style="color: #F59E0B;">{trends['total_draws']}</span>
            <span style="color: #6B7280;"> - </span>
            <span style="color: #EF4444;">{trends['total_losses']}</span>
        </div>
        <div style="font-size: 0.75rem; color: #9CA3AF; margin-top: 0.25rem;">
            Pobjede - Neriješeno - Porazi
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Ukupno pobjeda", trends['total_wins'])
    st.metric("Ukupno poraza", trends['total_losses'])

with col3:
    st.metric("Postignuto golova", trends['total_goals_scored'])
    st.metric("Primljeno golova", trends['total_goals_conceded'])

with col4:
    goal_diff = trends['total_goals_scored'] - trends['total_goals_conceded']
    diff_color = "#10B981" if goal_diff > 0 else "#EF4444" if goal_diff < 0 else "#6B7280"

    st.metric("Prosjek bodova", f"{trends['average_ppg']:.2f}")
    st.markdown(f"""
    <div style="margin-top: 1rem;">
        <div style="font-size: 0.875rem; color: #6B7280;">Ukupna razlika</div>
        <div style="font-size: 1.875rem; font-weight: 600; color: {diff_color};">
            {goal_diff:+d}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Additional collective statistics
st.markdown("## 📊 Dodatna kolektivna statistika")

# a) Average points per position across all seasons
st.markdown("### a) Prosječan broj bodova po poziciji")
st.markdown("Analiza prosječnog broja bodova potrebnih za svaku poziciju na ljestvici kroz sve sezone:")

# Calculate average points per position
position_stats = {}
for season in FIRST_DIVISION_SEASONS:
    try:
        league_df = load_season_data(season, "1")
        for _, row in league_df.iterrows():
            pos = int(row['position'])
            if pos not in position_stats:
                position_stats[pos] = {'points': [], 'played': []}
            position_stats[pos]['points'].append(row['points'])
            position_stats[pos]['played'].append(row['played'])
    except:
        continue

# Create summary table
position_summary = []
for pos in sorted(position_stats.keys()):
    avg_points = sum(position_stats[pos]['points']) / len(position_stats[pos]['points'])
    avg_played = sum(position_stats[pos]['played']) / len(position_stats[pos]['played'])
    avg_ppg = avg_points / avg_played if avg_played > 0 else 0
    position_summary.append({
        'Pozicija': f"{pos}.",
        'Prosječno bodova': f"{avg_points:.1f}",
        'Prosječno utakmica': f"{avg_played:.1f}",
        'Bodova po utakmici': f"{avg_ppg:.2f}"
    })

# Display in columns
col1, col2 = st.columns([2, 1])

with col1:
    import pandas as pd
    pos_df = pd.DataFrame(position_summary)
    st.dataframe(pos_df, use_container_width=True, hide_index=True)

with col2:
    # Highlight NK Hajduk 1932's positions
    club_positions = summary_df['position'].tolist()
    st.markdown("**NK Hajduk 1932 pozicije:**")
    for season_row in summary_df.itertuples():
        pos = int(season_row.position)
        if pos in position_stats:
            avg_pts = sum(position_stats[pos]['points']) / len(position_stats[pos]['points'])
            club_pts = season_row.points
            diff = club_pts - avg_pts
            color = "#10B981" if diff >= 0 else "#EF4444"
            st.markdown(f"""
            - {season_row.season}: **{pos}.** mjesto
              <span style="color: {color}; font-size: 0.85rem;">
              ({club_pts} bod. vs {avg_pts:.1f} prosjek, {diff:+.1f})
              </span>
            """, unsafe_allow_html=True)

st.markdown("---")

# b) Season-to-season ranking changes
st.markdown("### b) Promjene pozicija kroz sezone")
st.markdown("Praćenje promjena plasmana između uzastopnih sezona u 1. ŽNL-u:")

# Calculate season-to-season changes
changes = []
prev_season = None
prev_position = None

for idx, row in summary_df.iterrows():
    season = row['season']
    position = int(row['position'])

    if prev_season is not None:
        # Check if seasons are consecutive (accounting for 2. ŽNL gaps)
        change = prev_position - position  # Positive = improvement (lower position number)

        change_emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        change_color = "#10B981" if change > 0 else "#EF4444" if change < 0 else "#6B7280"
        change_text = f"+{change}" if change > 0 else str(change) if change < 0 else "0"

        changes.append({
            'season_from': prev_season,
            'season_to': season,
            'position_from': prev_position,
            'position_to': position,
            'change': change,
            'emoji': change_emoji,
            'color': change_color,
            'text': change_text
        })

    prev_season = season
    prev_position = position

# Display changes
if changes:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Sve promjene:**")
        for change in changes:
            st.markdown(f"""
            {change['emoji']} **{change['season_from']} → {change['season_to']}**
            <br>&nbsp;&nbsp;&nbsp;&nbsp;{change['position_from']}. → {change['position_to']}. mjesto
            <span style="color: {change['color']}; font-weight: 600;">({change['text']} mjesta)</span>
            """, unsafe_allow_html=True)

    with col2:
        # Statistics about changes
        improvements = sum(1 for c in changes if c['change'] > 0)
        declines = sum(1 for c in changes if c['change'] < 0)
        same = sum(1 for c in changes if c['change'] == 0)

        st.markdown("**Statistika promjena:**")
        st.markdown(f"""
        - <span style="color: #10B981;">📈 Napredovanja: {improvements}</span>
        - <span style="color: #EF4444;">📉 Nazadovanja: {declines}</span>
        - <span style="color: #6B7280;">➡️ Bez promjene: {same}</span>
        """, unsafe_allow_html=True)

        if len(changes) > 0:
            avg_change = sum(c['change'] for c in changes) / len(changes)
            st.markdown(f"- **Prosječna promjena**: {avg_change:+.1f} mjesta")

    with col3:
        # Biggest changes
        if changes:
            biggest_improvement = max(changes, key=lambda x: x['change'])
            biggest_decline = min(changes, key=lambda x: x['change'])

            st.markdown("**Najveće promjene:**")
            if biggest_improvement['change'] > 0:
                st.markdown(f"""
                📈 **Najbolje napredovanje:**
                <br>{biggest_improvement['season_from']} → {biggest_improvement['season_to']}
                <br><span style="color: #10B981; font-weight: 600;">+{biggest_improvement['change']} mjesta</span>
                """, unsafe_allow_html=True)

            if biggest_decline['change'] < 0:
                st.markdown(f"""
                📉 **Najveći pad:**
                <br>{biggest_decline['season_from']} → {biggest_decline['season_to']}
                <br><span style="color: #EF4444; font-weight: 600;">{biggest_decline['change']} mjesta</span>
                """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown(f"## 🏆 Put kroz 1. ŽNL")
    st.markdown("---")
    st.markdown(f"""
    ### Brza statistika
    - **Sezona**: {len(summary_df)}
    - **Najbolja pozicija**: {trends['best_position']}.
    - **Odigrano utakmica**: {trends['total_matches']}
    - **Ukupno golova**: {trends['total_goals_scored']}
    """)
