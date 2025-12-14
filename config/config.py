from dotenv import load_dotenv
import os

# Load env files
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_ROUTES_API = os.getenv("GOOGLE_ROUTES_API")
GOOGLE_STATIC_MAPS_API = os.getenv("GOOGLE_STATIC_MAPS_API")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LAT_HOME = float(os.getenv("LAT_HOME"))
LNG_HOME = float(os.getenv("LNG_HOME"))
LAT_JEG = float(os.getenv("LAT_DEST"))
LNG_JEG = float(os.getenv("LNG_DEST"))

# Coordinates (Home to JEG Tower)
ORIGIN = {"lat": LAT_HOME, "lng": LNG_HOME}
DESTINATION = {"lat": LAT_JEG, "lng": LNG_JEG}

# Colors for Traffic Indicators (Green = No Traffic, Red = Traffic)
COLOR_RED = 16711680
COLOR_GREEN = 65280

# Threshold for detour if more than stated mins
DETOUR_SAVINGS_THRESHOLD_MIN = 5

# Google Maps Zoom Level
ZOOM_LEVEL = 12