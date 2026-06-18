# Food Waste Management System

An executive-level data analytics project for a local food wastage management platform. Connects food providers (supermarkets, restaurants, grocery stores, catering services) with receivers (NGOs, charities, shelters, individuals) to reduce food waste and improve rescue rates.

## Project Structure

```
food/
├── README.md                 # Project documentation (this file)
├── SCHEMA.md                 # Data dictionary & ER diagram
├── requirements.txt          # Python dependencies
├── raw/                      # Source CSV datasets (immutable)
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   └── claims_data.csv
├── sql/                      # Database schema & analytics queries
│   ├── 01_create_schema.sql
│   ├── 02_load_data.sql
│   └── 03_analytics_queries.sql
├── src/                      # Application & analysis scripts
│   ├── application.py        # Streamlit executive dashboard
│   ├── config.py             # Shared paths & configuration
│   ├── eda.py                # EDA pipeline
│   └── generate_ppt.py       # Executive PowerPoint generator
└── final/                    # Generated deliverables
    ├── eda/
    │   ├── EDA_Report.md     # Exploratory data analysis report
    │   └── figures/          # EDA charts (PNG)
    └── Food_Waste_Executive_Summary.pptx
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the interactive dashboard

```bash
streamlit run src/application.py
```

### 3. Generate EDA report & charts

```bash
python src/eda.py
```

Output: `final/eda/EDA_Report.md` and charts in `final/eda/figures/`

### 4. Generate executive presentation

```bash
python src/generate_ppt.py
```

Output: `final/Food_Waste_Executive_Summary.pptx`

### 5. Load data into SQL database

```bash
# PostgreSQL example
psql -d food_waste -f sql/01_create_schema.sql
# Then follow load instructions in sql/02_load_data.sql
```

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Food Units | 25,794 |
| Food Rescue Rate | 28.4% |
| Claim Success Rate | 33.9% |
| Cancellation Rate | 33.6% |
| Providers | 1,000 |
| Receivers | 1,000 |
| Claims | 1,000 |

## Dashboard Pages

| Page | Description |
|------|-------------|
| Overview | Executive KPIs, status distribution, business metrics |
| Providers | Donor analytics, type breakdown, top contributors |
| Receivers | Demand patterns, segmentation, success rates |
| Food Analysis | Type/meal analysis, quantity distribution |
| Geographic | City-level supply vs demand |
| Operations | Claim funnel, time series, efficiency gauges |

## Data Model

Four relational tables linked by foreign keys:

- **providers** → donates via **food_listings**
- **receivers** → requests via **claims**
- **claims** → references **food_listings**

See [SCHEMA.md](SCHEMA.md) for the full data dictionary and ER diagram.

## Deliverables

| Deliverable | Location |
|-------------|----------|
| EDA Report | `final/eda/EDA_Report.md` |
| EDA Charts | `final/eda/figures/` |
| Executive PPT | `final/Food_Waste_Executive_Summary.pptx` |
| SQL Schema | `sql/01_create_schema.sql` |
| Analytics Queries | `sql/03_analytics_queries.sql` |
| Live Dashboard | `src/application.py` |

## Tech Stack

- **Python** — pandas, matplotlib, seaborn
- **Streamlit + Plotly** — interactive dashboard
- **python-pptx** — executive presentation
- **SQL** — PostgreSQL / SQLite compatible schema

## Author

Shubham Diwakar — Portfolio Project
