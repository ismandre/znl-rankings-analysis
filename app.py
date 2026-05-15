"""NK Hajduk 1932 Dashboard - Početna stranica"""

import streamlit as st
from src.config import CLUB_NAME, FIRST_DIVISION_SEASONS, SECOND_DIVISION_SEASONS, COLORS
from src.data_processor import prepare_first_division_summary, prepare_second_division_summary

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="NK Hajduk 1932 Analiza",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .hero-section {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 3rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
    }
    .kpi-card {
        background: #F3F4F6;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1E3A8A;
    }
    .fact-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #E5E7EB;
        margin: 0.5rem 0;
    }
    .navigation-button {
        background: #3B82F6;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">⚽ {CLUB_NAME}</div>
        <div class="hero-subtitle">Desetljeće nogometnih rezultata u ŽNL-u</div>
        <div style="margin-top: 1rem; font-size: 1.1rem;">
            2016/17 - 2025/26 | Dubrovačko-neretvanska županijska liga
        </div>
    </div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_overview_data():
    first_div = prepare_first_division_summary()
    return first_div

try:
    first_div_df = load_overview_data()

    # Check if data was loaded successfully
    if first_div_df.empty:
        st.error("Podaci nisu učitani. Molimo provjerite da li CSV datoteke postoje u 'data/' direktoriju.")
        st.stop()

    # Verify required columns exist
    required_cols = ['season', 'position', 'goals_for', 'goals_against', 'points', 'played']
    missing_cols = [col for col in required_cols if col not in first_div_df.columns]
    if missing_cols:
        st.error(f"Nedostaju kolone u podacima: {', '.join(missing_cols)}")
        st.info(f"Dostupne kolone: {', '.join(first_div_df.columns.tolist())}")
        st.stop()

except Exception as e:
    st.error(f"Greška pri učitavanju podataka: {str(e)}")
    st.info("Molimo provjerite da li su svi CSV fajlovi prisutni u 'data/' direktoriju.")
    st.stop()

# Overview KPIs
st.markdown("## 📊 Brzi pregled")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_seasons = len(first_div_df)
    st.metric("Sezona u 1. ŽNL-u", total_seasons, "8 sezona")

with col2:
    if len(first_div_df) > 0:
        best_position = first_div_df['position'].min()
        st.metric("Najbolja pozicija", f"{int(best_position)}.", "u 1. ŽNL-u")

with col3:
    if len(first_div_df) > 0:
        current_position = first_div_df[first_div_df['season'] == '2025/26']['position'].values
        if len(current_position) > 0:
            st.metric("Trenutna pozicija", f"{int(current_position[0])}.", "sezona 2025/26")
        else:
            latest = first_div_df.iloc[-1]
            st.metric("Zadnja pozicija", f"{int(latest['position'])}.", latest['season'])

with col4:
    total_goals = first_div_df['goals_for'].sum()
    st.metric("Ukupno golova", int(total_goals), "u 1. ŽNL-u")

st.markdown("---")

# Quick Facts
st.markdown("## ⚡ Brze činjenice")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Povijest lige")
    st.markdown(f"""
    - **2016/17 - 2020/21**: 5 sezona u 1. ŽNL-u
    - **2021/22**: Natjecanje u 2. ŽNL-u (ispali iz 1. ŽNL-a)
    - **2022/23**: Povratak u 1. ŽNL
    - **2023/24**: Natjecanje u 2. ŽNL-u (ispali iz 1. ŽNL-a)
    - **2024/25 - 2025/26**: Natrag u 1. ŽNL-u
    """)

with col2:
    st.markdown("### 🎯 Ključna dostignuća (1. ŽNL)")

    if len(first_div_df) > 0:
        complete_seasons = first_div_df[~first_div_df['is_incomplete']]
        best_season = complete_seasons.loc[complete_seasons['points'].idxmax()]
        st.markdown(f"""
        - **Najbolja sezona**: {best_season['season']} - {int(best_season['points'])} bodova
        - **Najbolja pozicija**: {int(first_div_df['position'].min())}. mjesto
        - **Najviše golova u sezoni**: {int(first_div_df['goals_for'].max())} golova
        - **Ukupno utakmica**: {int(first_div_df['played'].sum())} odigranih u 1. ŽNL-u
        """)

st.markdown("---")

# Navigation Guide
st.markdown("## 🧭 Istraži nadzornu ploču")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🏆 Put kroz 1. ŽNL
    Zaronite u 8 sezona prvog ranga s:
    - Analizom sezona po sezonama
    - Trendovima i vizualizacijama
    - Ključnim statistikama i uvidima
    - Napomenama o sezonama u 2. ŽNL-u
    """)

with col2:
    st.markdown("""
    ### 📊 Napredna analiza
    Istražite dublje uvide:
    - Prilagođena pretraživanja
    - Potpune ligaške tablice
    - Detaljnu statistiku po sezonama
    - Buduće mogućnosti analize
    """)

st.markdown("---")

# Footer
st.markdown("### 📝 O nadzornoj ploči")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    Ova nadzorna ploča analizira nastupe **{CLUB_NAME}** u 1. ŽNL-u
    Dubrovačko-neretvanske županijske lige, od 2016/17 do 2025/26.

    Analiza obuhvaća:
    - **8 sezona** natjecanja u 1. ŽNL-u (prvi rang)
    - Detaljne metrike učinka, trendove i uvide
    - Napomene o sezonama provedenim u 2. ŽNL-u
    """)

with col2:
    st.info(f"""
    **Izvor podataka**: Službene ŽNL ljestvice

    **Analizirano sezona**: {total_seasons} u 1. ŽNL-u

    **Zadnje ažuriranje**: sezona 2025/26 (u tijeku)
    """)

# Sidebar
with st.sidebar:
    st.markdown(f"## ⚽ {CLUB_NAME}")
    st.markdown("---")
    st.markdown("### 📊 Navigacija")
    st.markdown("""
    Koristite gornje stranice za istraživanje:
    - **Početna**: Pregled i brze činjenice
    - **Put kroz 1. ŽNL**: Analiza prvog ranga
    - **Napredna analiza**: Detaljni alati
    """)
    st.markdown("---")
    st.markdown("### 📈 Brza statistika (1. ŽNL)")
    st.markdown(f"""
    - **Ukupno utakmica**: {int(first_div_df['played'].sum())}
    - **Ukupno golova**: {int(total_goals)}
    - **Ukupno bodova**: {int(first_div_df['points'].sum())}
    """)
