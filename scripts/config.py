from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------
# DATA
# --------------------------------------------------
DATA_ROOT = PROJECT_ROOT / "data" / "ds004147"

# --------------------------------------------------
# OUTPUT DIRECTORIES 
# --------------------------------------------------
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

FIGURES_DIR = OUTPUTS_DIR / "figures"
RESULTS_DIR = OUTPUTS_DIR / "results"
SANITY_DIR = OUTPUTS_DIR / "sanity_checks"
LOGS_DIR = OUTPUTS_DIR / "logs"

# --------------------------------------------------
# SUBJECTS
# --------------------------------------------------
SUBJECTS = [f"sub-{i}" for i in range(27, 39)]

# --------------------------------------------------
# ERP SETTINGS
# --------------------------------------------------
TMIN = -0.2
TMAX = 0.8
BASELINE = (None, 0)

FRN_CH = ["FCz"]
P300_CH = ["Pz"]

FRN_WIN = (0.2, 0.3)
P300_WIN = (0.3, 0.5)