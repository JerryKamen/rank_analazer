"""
Configuration for Ranking Analyzer Agent
"""

# ORIS URLs
ORIS_BASE_URL = "https://oris.ceskyorientak.cz"
STARTOVKA_URL = "https://oris.ceskyorientak.cz/Startovka?id=8950"
RANKING_URL = "https://oris.ceskyorientak.cz/Ranking?sport=1&ranktype=2"

# Target categories for MČR long distance
TARGET_CATEGORIES = ["H21", "D21"]

# Number of top runners to consider for coefficient calculation
TOP_RUNNERS_COUNT = 4

# Output settings
OUTPUT_DIR = "reports"
PDF_FILENAME = "ranking_coefficient_report.pdf"

# Timeout settings
REQUEST_TIMEOUT = 30
SELENIUM_TIMEOUT = 10

# Categories names mapping
CATEGORY_NAMES = {
    "H21": "Muži 21 let",
    "D21": "Ženy 21 let"
}
