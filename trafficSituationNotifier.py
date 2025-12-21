import os
import requests
from datetime import datetime
from config.config import DETOUR_SAVINGS_THRESHOLD_MIN, ORIGIN, DESTINATION, COLOR_GREEN, COLOR_RED
from config.googleData import get_route_data, generate_static_map_url
from helpers.parseDuration import parse_duration
from helpers.formatTravelTime import format_travel_time

def main():
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not DISCORD_WEBHOOK_URL:
        print("❌ ERROR: Discord Webhook URL is missing or None.")
        print("Double check your GitHub Secret name is 'DISCORD_WEBHOOK_URL'")
        return
    
    try:
        # 1. Fetch Data for all modes
        drive_data = get_route_data("DRIVE", alternatives=True)
        moto_data = get_route_data("TWO_WHEELER")
        transit_data = get_route_data("TRANSIT")

        # 2. Process Driving Data (Main Route)
        if not drive_data.get('routes'):
            print("Error: No routes found.")
            return

        main_route = drive_data['routes'][0]
        drive_time_min = parse_duration(main_route.get('duration'))
        static_time_min = parse_duration(main_route.get('staticDuration'))
        
        traffic_delay = drive_time_min - static_time_min
        is_heavy_traffic = traffic_delay > 10

        # 3. Process Other Modes
        moto_time_min = parse_duration(moto_data['routes'][0].get('duration')) if moto_data.get('routes') else "N/A"
        transit_time_min = parse_duration(transit_data['routes'][0].get('duration')) if transit_data.get('routes') else "N/A"
            
        # 4. Format Times
        formatted_drive = format_travel_time(drive_time_min)
        formatted_moto = format_travel_time(moto_time_min)
        formatted_transit = format_travel_time(transit_time_min)

        # 5. Check for Better Routes (Detours)
        better_route_msg = ""
        map_image_url = generate_static_map_url(
            main_route['polyline']['encodedPolyline'],
            ORIGIN["lat"], ORIGIN["lng"],
            DESTINATION["lat"], DESTINATION["lng"]
        )
        
        if len(drive_data['routes']) > 1:
            for alt_route in drive_data['routes'][1:]:
                alt_time = parse_duration(alt_route.get('duration'))
                time_saved = drive_time_min - alt_time
                
                if time_saved >= DETOUR_SAVINGS_THRESHOLD_MIN:
                    better_route_msg = (
                        f"\n**ALTERNATIVE ROUTE FOUND!**\n"
                        f"Please be advised to take an alternate route that saves **{time_saved} minutes**.\n"
                        f"(Travel time: {alt_time} mins)"
                    )
                    # Update map to show the better route instead
                    map_image_url = generate_static_map_url(
                        main_route['polyline']['encodedPolyline'],
                        ORIGIN["lat"], ORIGIN["lng"],
                        DESTINATION["lat"], DESTINATION["lng"]
                    )
                    break

        # 6. Construct Discord Message
        CURRENT_TIME = datetime.now().strftime("%B %d, %Y %I:%M %p")
        
        traffic_status_msg = ""
        header_emoji = "🔴" if is_heavy_traffic else "🟢"
        if is_heavy_traffic:
            traffic_status_msg = f"⚠️ **HEAVY TRAFFIC DETECTED**\nCurrent traffic conditions are adding around {traffic_delay} minutes of delay compared to free-flow traffic."

        message_content = f"""
>>> ## {header_emoji} Traffic Situation Advisory
**Date:** *{CURRENT_TIME}*
**Route:** Home (H) ➡️ Office (O)

**Estimated Travel Times:**
- 🏍️ **Motorcycle:** `{formatted_moto}`
- 🚗 **Car:** `{formatted_drive}`
- 🚌 **Commute:** `{formatted_transit}`

{traffic_status_msg}
{better_route_msg}
"""

        payload = {
            "content": message_content,
            "embeds": [{
                "title": "Home to JEG Tower Route",
                "image": {"url": map_image_url},
                "color": COLOR_RED if is_heavy_traffic else COLOR_GREEN
            }]
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Traffic update sent successfully.")
        else:
            print(f"Failed to send traffic update. Status code: {response.status_code}")
            print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error running script: {e}")

if __name__ == "__main__":
    main()