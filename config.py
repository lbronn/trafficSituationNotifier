from dotenv import load_dotenv
import os

# Load env files
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
print(GOOGLE_API_KEY, DISCORD_WEBHOOK_URL)

# Coordinates (Home to JEG Tower)
ORIGIN = {"lat": 10.439675051459568, "lng": 124.00733686849964}
DESTINATION = {"lat": 10.317158007945627, "lng": 123.9019046097545}

# Threshold for detour if more than stated mins
DETOUR_SAVINGS_THRESHOLD_MIN = 5
