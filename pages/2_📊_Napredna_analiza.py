"""Napredna analiza - Detaljni alati i istraživač podataka"""

import streamlit as st
import pandas as pd
from src.config import CLUB_NAME, FIRST_DIVISION_SEASONS, SECOND_DIVISION_SEASONS
from src.data_loader import load_season_data, get_club_data, load_all_seasons
from src.data_processor import prepare_first_division_summary, prepare_second_division_summary

st.set_page_config(layout="wide", page_title="Napredna analiza", page_icon="📊")

st.markdown("# 📊 Napredna analiza")
st.markdown("Zaronite u podatke pomoću prilagođenih upita i potpunih ligaških tablica")

st.markdown("---")

# Tab interface
tab1, tab2, tab3 = st.tabs(["🔍 Alat za upite", "📋 Istraživač podataka", "🔮 Buduće analize"])

with tab1:
    st.markdown("## 🔍 Alat za prilagođene upite")
    st.markdown("Filtrirajte i analizirajte određene sezone i metrike iz 1. ŽNL-a")

    st.info("📋 Ova analiza prikazuje samo podatke iz 1. ŽNL-a (8 sezona)")

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        # Only 1. ŽNL seasons
        all_seasons = sorted(FIRST_DIVISION_SEASONS)
        season_filter = st.multiselect(
            "Sezone (1. ŽNL)",
            options=all_seasons,
            default=all_seasons
        )

    with col2:
        metric_view = st.selectbox(
            "Fokus metrike",
            options=["Pregled", "Napad", "Obrana", "Učinkovitost"]
        )

    if st.button("Generiraj analizu"):
        # Prepare filtered data (only 1. ŽNL)
        filtered_data = []

        for season in season_filter:
            if season in FIRST_DIVISION_SEASONS:
                try:
                    df = load_season_data(season, "1")
                    club_data = get_club_data(df, CLUB_NAME)
                    if club_data is not None:
                        row = club_data.to_dict()
                        row['division'] = '1. ŽNL'
                        row['total_teams'] = len(df)
                        filtered_data.append(row)
                except:
                    pass

        if len(filtered_data) > 0:
            result_df = pd.DataFrame(filtered_data)

            # Display based on metric view
            if metric_view == "Pregled":
                display_cols = ['division', 'season', 'position', 'total_teams',
                               'points', 'played', 'wins', 'draws', 'losses']
            elif metric_view == "Napad":
                display_cols = ['division', 'season', 'goals_for', 'played', 'wins']
                result_df['goals_per_game'] = (result_df['goals_for'] / result_df['played']).round(2)
                display_cols.append('goals_per_game')
            elif metric_view == "Obrana":
                display_cols = ['division', 'season', 'goals_against', 'played', 'losses']
                result_df['conceded_per_game'] = (result_df['goals_against'] / result_df['played']).round(2)
                display_cols.append('conceded_per_game')
            else:  # Učinkovitost
                display_cols = ['division', 'season', 'points', 'played']
                result_df['ppg'] = (result_df['points'] / result_df['played']).round(2)
                result_df['win_rate'] = ((result_df['wins'] / result_df['played']) * 100).round(1)
                display_cols.extend(['ppg', 'win_rate'])

            st.dataframe(
                result_df[display_cols],
                use_container_width=True,
                hide_index=True
            )

            # Summary statistics
            st.markdown("### 📈 Zbirna statistika")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Sezona", len(result_df))
                st.metric("Ukupno utakmica", int(result_df['played'].sum()))

            with col2:
                st.metric("Ukupno bodova", int(result_df['points'].sum()))
                st.metric("Ukupno pobjeda", int(result_df['wins'].sum()))

            with col3:
                st.metric("Postignuto golova", int(result_df['goals_for'].sum()))
                st.metric("Primljeno golova", int(result_df['goals_against'].sum()))

            with col4:
                avg_ppg = (result_df['points'].sum() / result_df['played'].sum()).round(2)
                st.metric("Prosjek bod/ut", avg_ppg)
                goal_diff = int(result_df['goals_for'].sum() - result_df['goals_against'].sum())
                st.metric("Gol razlika", f"{goal_diff:+d}")

        else:
            st.warning("Nema dostupnih podataka za odabrane filtere")

with tab2:
    st.markdown("## 📋 Istraživač podataka")
    st.markdown("Pregledajte potpune ligaške tablice za sve sezone 1. ŽNL-a")

    st.info("📋 Prikaz potpunih ljestvica samo za sezone u 1. ŽNL-u")

    # Season selector (only 1. ŽNL)
    available_seasons = FIRST_DIVISION_SEASONS
    division_num = "1"

    explore_season = st.selectbox("Odaberite sezonu (1. ŽNL)", available_seasons)

    if st.button("Učitaj potpunu tablicu"):
        try:
            league_df = load_season_data(explore_season, division_num)

            st.markdown(f"### 1. ŽNL {explore_season} - Potpuna ligaška tablica")

            # Highlight NK Hajduk 1932 row
            def highlight_club(row):
                if row['club'] == CLUB_NAME:
                    return ['background-color: #FEF3C7'] * len(row)
                return [''] * len(row)

            styled_df = league_df.style.apply(highlight_club, axis=1)

            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )

            # League statistics
            st.markdown("### 📊 Statistika lige")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Ukupno momčadi", len(league_df))
                champion = league_df[league_df['position'] == 1].iloc[0]
                st.metric("Prvak", champion['club'])
                st.metric("Bodovi prvaka", int(champion['points']))

            with col2:
                total_goals = league_df['goals_for'].sum()
                st.metric("Ukupno golova (liga)", int(total_goals))
                avg_goals = total_goals / len(league_df)
                st.metric("Prosjek gol./momčad", f"{avg_goals:.1f}")

            with col3:
                club_data = get_club_data(league_df, CLUB_NAME)
                if club_data is not None:
                    st.metric(f"{CLUB_NAME} pozicija", int(club_data['position']))
                    st.metric(f"{CLUB_NAME} bodovi", int(club_data['points']))

        except Exception as e:
            st.error(f"Greška prilikom učitavanja podataka: {e}")

with tab3:
    st.markdown("## 🔮 Ideje za buduće analize")

    st.markdown("""
    Ova nadzorna ploča može biti proširena dodatnim analizama:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📈 Analitika učinka
        - **Domaćin vs gost**: Usporedba učinka kod kuće i u gostima
        - **Mjesečni trendovi**: Analiza učinka po mjesecu/dijelu sezone
        - **Analiza forme**: Praćenje niza pobjeda/poraza
        - **Ključni nastupi**: Važne utakmice i presudni trenuci
        """)

        st.markdown("""
        ### 🆚 Analiza protivnika
        - **Međusobni susreti**: Rezultati protiv specifičnih protivnika
        - **Učinak protiv vodećih**: Rezultati protiv čelnih momčadi
        - **Derbiji**: Analiza rivalskih utakmica
        - **Plasirana/ispala momčad**: Učinak protiv različitih kalibra protivnika
        """)

    with col2:
        st.markdown("""
        ### ⚽ Napredne metrike
        - **Očekivani bodovi**: Statističko modeliranje učinka
        - **Vrijeme golova**: Kada su golovi postignuti/primljeni
        - **Obrasci postizanja**: Analiza distribucije golova
        - **Obrambena čvrstoća**: Utakmice bez primljenog gola i obrambeni učinak
        """)

        st.markdown("""
        ### 🏆 Povijesni kontekst
        - **Sveukupni rekordi**: Najbolji/najgori nastupi u karijeri
        - **Usporedba desetljeća**: Učinak 2010-ih vs 2020-ih
        - **Utjecaj trenera**: Ako su dostupni podaci o trenerima
        - **Doprinosi igrača**: Ako su dostupne statistike igrača
        """)

    st.info("""
    💡 **Prijedlog**: Ove analize mogu biti dodane kako skup podataka raste ili kako
    dodatni izvori podataka postaju dostupni. Trenutni okvir olakšava proširenje s
    novim vizualizacijama i uvidima.
    """)

    # Data quality notes
    st.markdown("---")
    st.markdown("### 📝 Napomene o podacima")

    with st.expander("Pogledajte informacije o kvaliteti podataka"):
        st.markdown("""
        **Trenutni skup podataka:**
        - 8 sezona potpunih podataka iz 1. ŽNL-a (2016/17 - 2025/26)
        - Sezone 2021/22 i 2023/24 nisu uključene (klub je nastupao u 2. ŽNL-u)
        - Sezona 2025/26 trenutno u tijeku

        **Posebni slučajevi:**
        - 2019/20: Skraćena sezona (12 utakmica, vjerojatno utjecaj COVID-19)
        - 2025/26: Nedovršena sezona (u tijeku)
        - 2021/22 i 2023/24: Klub u 2. ŽNL-u (nakon ispadanja iz 1. ŽNL-a)

        **Izvori podataka:**
        - Službene 1. ŽNL ljestvice u CSV formatima
        - Svi podaci validirani za dosljednost
        """)

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Napredni alati")
    st.markdown("---")
    st.markdown("""
    ### Dostupni alati
    - **Prilagođeni upiti**: Filtriraj po sezoni/metrici
    - **Istraživač podataka**: Potpune ligaške tablice
    - **Buduće ideje**: Mogućnosti proširenja

    ### Savjeti
    - Koristite filtre za fokusiranu analizu
    - Izvezite podatke za vanjske alate
    - Provjerite nove funkcionalnosti
    """)
