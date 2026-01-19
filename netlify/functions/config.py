"""
Configuration file for Travel Itinerary Optimizer
"""

# Top 10 travel websites to scrape
TRAVEL_WEBSITES = [
    "expedia",
    "booking",
    "kayak",
    "skyscanner",
    "tripadvisor",
    "agoda",
    "hotels",
    "priceline",
    "orbitz",
    "travelocity"
]

# Optimization weights (0.0 to 1.0)
COST_WEIGHT = 0.6  # How much to prioritize cost
TIME_WEIGHT = 0.4  # How much to prioritize time

# Default search parameters
DEFAULT_DEPARTURE_CITY = "New York"
DEFAULT_DESTINATION_CITY = "Paris"
DEFAULT_DEPARTURE_DATE = None  # Will use current date + 30 days
DEFAULT_RETURN_DATE = None  # Will use departure date + 7 days
DEFAULT_TRAVELERS = 2  # For couple

# Scraping settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 1  # seconds

# Output settings
CURRENCY = "USD"
DATE_FORMAT = "%Y-%m-%d"
