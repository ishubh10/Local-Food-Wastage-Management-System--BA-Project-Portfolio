"""Project paths and shared configuration."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "raw"
FINAL_DIR = PROJECT_ROOT / "final"
EDA_DIR = FINAL_DIR / "eda"
FIGURES_DIR = EDA_DIR / "figures"
SQL_DIR = PROJECT_ROOT / "sql"

DATA_FILES = {
    "providers": RAW_DIR / "providers_data.csv",
    "receivers": RAW_DIR / "receivers_data.csv",
    "food": RAW_DIR / "food_listings_data.csv",
    "claims": RAW_DIR / "claims_data.csv",
}
