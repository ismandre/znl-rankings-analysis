# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis project for ŽNL (1. and 2. ŽNL Dubrovačko-neretvanska) rankings data spanning multiple seasons from 2016/17 to 2025/26.

## Data Structure

The `data/` directory contains CSV files with the following naming pattern:
- `1. ŽNL [season] - rankings.csv` for first division
- `2. ŽNL [season] - rankings.csv` for second division

Each CSV file has these columns:
- `season`: Season identifier (e.g., "2016/17")
- `position`: Final league position
- `club`: Club name
- `played`: Matches played
- `wins`, `draws`, `losses`: Match results
- `goals_for`, `goals_against`: Goals scored/conceded
- `goal_difference`: Net goal difference
- `points`: Total points

## Environment Setup

The project uses Python 3.9 with a virtual environment in `venv/`.

To activate the virtual environment:
```bash
source venv/bin/activate
```

To install new dependencies (when needed):
```bash
pip install <package>
pip freeze > requirements.txt  # Update requirements file after installing packages
```

Common packages for data analysis projects like this typically include:
- pandas (for data manipulation)
- matplotlib/seaborn (for visualization)
- jupyter/jupyterlab (for notebook-based analysis)

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard for visualizing NK Hajduk 1932's performance:

### Dashboard Structure
- `app.py`: Home page with overview and quick stats
- `pages/1_🏆_1_ZNL_Journey.py`: Analysis of 8 seasons in 1. ŽNL
- `pages/2_🥇_2_ZNL_Championships.py`: Celebration of 2 championship seasons in 2. ŽNL
- `pages/3_📊_Advanced_Analysis.py`: Custom queries and data explorer

### Core Modules
- `src/config.py`: Configuration constants (seasons, colors, club name)
- `src/data_loader.py`: CSV loading with Streamlit caching
- `src/data_processor.py`: Data transformation and aggregation
- `src/visualizations.py`: Reusable Plotly chart functions

### Running the Dashboard
```bash
source venv/bin/activate
streamlit run app.py
```

Dashboard opens at http://localhost:8501

### Key Features
- Season-by-season analysis with league context
- Interactive Plotly visualizations (position timeline, goals comparison, PPG trends)
- Championship season deep dives
- Custom query tool with filters
- Full league table explorer
- Responsive design with custom theming

## Development Workflow

Since this is a data analysis project:
1. Activate the virtual environment before working
2. Use the Streamlit dashboard for interactive analysis
3. CSV files in `data/` should be treated as read-only source data
4. Any analysis outputs, plots, or processed data should be saved to separate output directories
5. When adding new analyses, extend the dashboard pages or create new pages
