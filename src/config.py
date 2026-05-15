"""Configuration constants for NK Hajduk 1932 dashboard."""
import os

# Get the project root directory (parent of src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLUB_NAME = "NK Hajduk 1932"
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

# Season classifications
FIRST_DIVISION_SEASONS = [
    "2016/17", "2017/18", "2018/19", "2019/20",
    "2020/21", "2022/23", "2024/25", "2025/26"
]

SECOND_DIVISION_SEASONS = ["2021/22", "2023/24"]

CLUB_CONFIGS = {
    "NK Župa dubrovačka": {"logo": "assets/nk_zupa_dubrovacka.png", "primary_color": "#1E40AF"},
    "NK Croatia Gabrili": {"logo": "assets/nk_croatia_gabrili.png", "primary_color": "#DC2626"},
    "NK Gusar": {"logo": "assets/nk_gusar_komin.png", "primary_color": "#0891B2"},
    "NK Orebić": {"logo": "assets/nk_orebic.png", "primary_color": "#16A34A"},
    "ONK Metković": {"logo": "assets/onk_metkovic.png", "primary_color": "#EA580C"},
    "NK Hajduk 1932": {"logo": "assets/nk_hajduk_1932.png", "primary_color": "#1E3A8A"},
    "NK Maestral": {"logo": "assets/nk_maestral.png", "primary_color": "#0D9488"},
    "HNK Slaven Gruda": {"logo": "assets/hnk_slaven_gruda.png", "primary_color": "#7C3AED"},
    "NK Grk": {"logo": "assets/nk_grk.png", "primary_color": "#DB2777"},
    "NK Jadran Smokvica": {"logo": "assets/nk_jadran_smkovica.png", "primary_color": "#2563EB"},
    "HNK Konavljanin": {"logo": "assets/hnk_konavljanin.png", "primary_color": "#CA8A04"},
    "NK Omladinac Lastovo": {"logo": "assets/nk_omladinac_lastovo.png", "primary_color": "#059669"},
    "NK Žrnovo": {"logo": "assets/nk_zrnovo.png", "primary_color": "#B91C1C"},
    "NK Neretva": {"logo": "assets/nk_neretva.png", "primary_color": "#0284C7"},
    "NK Sokol (D)": {"logo": "assets/nk_sokol_dubravka.png", "primary_color": "#65A30D"},
    "BŠK Zmaj": {"logo": "assets/bsk_zmaj.png", "primary_color": "#DC2626"},
    "NK Jadran LP": {"logo": "assets/nk_jadran_lp.png", "primary_color": "#0369A1"},
}

# Special season markers
INCOMPLETE_SEASONS = ["2025/26"]
SHORTENED_SEASONS = ["2019/20"]

# Color scheme
COLORS = {
    "primary": "#1E3A8A",      # Deep blue
    "secondary": "#3B82F6",    # Bright blue
    "success": "#10B981",      # Green
    "warning": "#F59E0B",      # Orange
    "danger": "#EF4444",       # Red
    "goals_for": "#10B981",    # Green for goals scored
    "goals_against": "#EF4444", # Red for goals conceded
    "championship": "#F59E0B",  # Gold for championships
    "text_dark": "#111827",
    "text_light": "#6B7280",
    "background": "#F3F4F6"
}

# Chart styling
CHART_CONFIG = {
    "displayModeBar": False,
    "displaylogo": False
}

CHART_LAYOUT = {
    "font": {"family": "sans-serif", "size": 12},
    "plot_bgcolor": "white",
    "paper_bgcolor": "white",
    "margin": {"l": 50, "r": 50, "t": 50, "b": 50}
}
