"""
Shared path configuration. Every script imports this so the package runs
identically regardless of the current working directory it is launched from.

Tables and other numerical outputs are written to ../output/ (as .csv/.xlsx).
Figures (.png) are written to ../figures/ at 600 DPI.
"""
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CODE_DIR.parent
DATA_DIR = ROOT_DIR / "data" / "raw"
SAT_DIR = ROOT_DIR / "data" / "satellite_images"
GEE_DIR = ROOT_DIR / "data" / "gee_outputs"
ASSETS_DIR = ROOT_DIR / "data" / "design_assets"
OUTPUT_DIR = ROOT_DIR / "output"
FIG_DIR = ROOT_DIR / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

FIGURE_DPI = 600
