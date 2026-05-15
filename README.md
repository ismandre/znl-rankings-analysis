# NK Hajduk 1932 Dashboard

An interactive Streamlit dashboard analyzing NK Hajduk 1932's performance across 10 seasons (2016/17-2025/26) of ŽNL football.

## Overview

This dashboard provides comprehensive analysis of NK Hajduk 1932's journey through the Dubrovačko-neretvanska County League (ŽNL), covering:
- **8 seasons** in 1. ŽNL (first division)
- **2 championship seasons** in 2. ŽNL (second division)

## Features

### Home Page
- Quick overview with key statistics
- Division history timeline
- Key achievements and milestones
- Navigation guide

### 1. ŽNL Journey
- Season-by-season detailed analysis
- Interactive performance trend charts
- Statistical highlights (best/worst seasons)
- League context for each season
- Overall statistics across 8 seasons

### 2. ŽNL Championships
- Detailed analysis of both championship seasons (2021/22 and 2023/24)
- Side-by-side comparison
- Match result breakdowns
- Promotion timeline story

### Advanced Analysis
- Custom query tool with filters
- Full league table explorer
- Future analysis ideas

## Installation

1. Ensure you're in the project directory:
```bash
cd /Users/andreism/me/znl-rankings-analysis
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

## Usage

Launch the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at http://localhost:8501

## Project Structure

```
.
├── app.py                      # Home page / entry point
├── pages/
│   ├── 1_🏆_1_ZNL_Journey.py    # First division analysis
│   ├── 2_🥇_2_ZNL_Championships.py  # Championship seasons
│   └── 3_📊_Advanced_Analysis.py    # Advanced tools
├── src/
│   ├── config.py              # Configuration constants
│   ├── data_loader.py         # CSV loading with caching
│   ├── data_processor.py      # Data transformation
│   └── visualizations.py      # Plotly charts
├── .streamlit/
│   └── config.toml            # Custom theme
├── data/                       # CSV rankings files
└── requirements.txt            # Python dependencies
```

## Key Metrics

For each season, the dashboard displays:
- Final league position
- Total points and points per game (PPG)
- Goals scored and conceded
- Win-Draw-Loss record
- League context (champion, points gaps)

## Data Sources

- Official ŽNL rankings CSV files
- Seasons: 2016/17 through 2025/26
- 2025/26 season marked as ongoing (incomplete)

## Special Cases

- **2019/20**: Shortened season (12 matches, likely COVID-19 impact)
- **2025/26**: Ongoing season (20/22 matches played)
- **2021/22 & 2023/24**: Championship seasons in 2. ŽNL

## Technologies

- **Streamlit**: Dashboard framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **Python 3.9**: Core language

## Key Highlights

- 🏆 **Two Championships**: 2021/22 (50 pts) and 2023/24 (45 pts)
- ⚽ **Total Goals**: 156+ goals scored across all seasons
- 📊 **Consistency**: Regular presence in 1. ŽNL
- 🎯 **Best Record**: 2021/22 - 16 wins, 2 draws, 0 losses

## Future Enhancements

Potential additions include:
- Home vs away performance analysis
- Monthly/seasonal trend analysis
- Head-to-head records against specific opponents
- Goal timing analysis
- Historical comparisons across decades

## License

This is a personal data analysis project for NK Hajduk 1932 performance tracking.
