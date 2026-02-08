# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A multi-part blog series analyzing NFL Quarterback Rating (QBR) metrics. Each blog installment adds complexity: data collection (Blog 1), statistical analysis (Blog 2), interactive Dash visualization (Blog 3), predictive modeling (Blog 4), and extended scraping via StatHead/Selenium (Blog 5).

Blog posts are published at: http://btc.bashingbitcoin.com

## Running the Dash App (Blog 3)

```bash
cd QBR-Blog-Post/Blog_3
python3 QBR_Blog_3_Dash_App.py
# Open http://localhost:8000/
```

Requires Python 3.10.9 and: pandas, numpy, dash, plotly, dash_bootstrap_components.

## Key Dependencies

- **Web scraping:** requests, BeautifulSoup, selenium (Blog 5 uses Selenium for StatHead, which requires authentication credentials stored in `Blog_5/stathead_credentials/`)
- **Data/analysis:** pandas, numpy, matplotlib, plotly
- **Dashboard:** dash, dash_bootstrap_components

No requirements.txt exists; dependencies are implicit in the notebooks and scripts.

## Architecture

**Data flow:** Web sources (ESPN, pro-football-reference, StatHead) → scraping scripts → CSV files → analysis notebooks → visualizations/models.

- **Blog_1/** - Web scraping ESPN QBR + merging with pro-football-reference data (Jupyter notebooks)
- **Blog_2/** - Exploratory analysis comparing QBR vs Passer Rating (Jupyter notebook)
- **Blog_3/** - Interactive Dash web app with two tabs: individual QB comparison and team-level analysis. Only standalone `.py` script in the project; reads `qbr3_df.csv` from the same directory.
- **Blog_4/** - Predictive modeling to estimate QBR from pro-football-reference features (Jupyter notebook)
- **Blog_5/** - Extended data collection using Selenium for StatHead (requires paid subscription). Separate notebooks for regular season, weekly, and playoff scraping. Generated CSVs live in `Blog_5/data/` (gitignored).

## Notes

- No test framework, linter, or CI/CD pipeline is configured.
- `Blog_5/data/`, `Blog_5/stathead_credentials/`, and `Blog_5/additional_web_scraping_scripts/` are gitignored.
- Notebooks are the primary development medium; run them cell-by-cell in Jupyter.
