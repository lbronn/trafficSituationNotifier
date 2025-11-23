import requests
import json
from datetime import datetime
import sys
from config import GOOGLE_API_KEY, DISCORD_WEBHOOK_URL, ORIGIN, DESTINATION, DETOUR_SAVINGS_THRESHOLD_MIN

def get_route_data(travel_mode, alternatives=False):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }
    
    body = {
        "origin": {"location": {"latLng": {"latitude": ORIGIN["lat"], "longitude": ORIGIN["lng"]}}},
        "destination": {"location": {"latLng": {"latitude": DESTINATION["lat"], "longitude": DESTINATION["lng"]}}},
        "travelMode": travel_mode,
        "routingPreference": "TRAFFIC_AWARE" if travel_mode in ["DRIVE", "TWO_WHEELER"] else None,
        "computeAlternativeRoutes": alternatives,
        "units": "METRIC"
    }

    # Transit requires different handling (no traffic_aware preference)
    if travel_mode == "TRANSIT":
        body.pop("routingPreference", None)

    response = requests.post(url, json=body, headers=headers)
    return response.json()

def parse_duration(duration_str):
    """Converts '3600s' string to minutes (int)."""
    if not duration_str: return 0
    return int(duration_str.replace("s", "")) // 60

def generate_static_map_url(polyline):
    """Creates a URL for a static map image showing the route."""
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = [
        "size=600x300",
        "maptype=roadmap",
        f"path=enc:{polyline}",
        f"key={GOOGLE_API_KEY}"
    ]
    return base_url + "&".join(params)

def main():
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
        static_time_min = parse_duration(main_route.get('staticDuration')) # Time without traffic
        
        # Calculate Traffic Impact
        traffic_delay = drive_time_min - static_time_min
        is_heavy_traffic = traffic_delay > 10 # Flag if delay is > 10 mins

        # 3. Process Other Modes
        moto_time_min = parse_duration(moto_data['routes'][0].get('duration')) if moto_data.get('routes') else "N/A"
        transit_time_min = parse_duration(transit_data['routes'][0].get('duration')) if transit_data.get('routes') else "N/A"

        # 4. Check for Better Routes (Detours)
        better_route_msg = ""
        map_image_url = generate_static_map_url(main_route['polyline']['encodedPolyline'])
        
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
                    map_image_url = generate_static_map_url(alt_route['polyline']['encodedPolyline'])
                    break 

        # 5. Construct Discord Message
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        traffic_status = ""
        if is_heavy_traffic:
            traffic_status = f"\n⚠️ **HEAVY TRAFFIC DETECTED**\nCurrent conditions are adding ~{traffic_delay} minutes of delay compared to free-flow traffic."

        message_content = f"""
**Traffic Situation Advisory**
*From Location X to Location Y*
*As of {current_time}*

🏍️ **Motorcycle:** {moto_time_min} mins
🚗 **Car:** {drive_time_min} mins
🚌 **Commute:** {transit_time_min} mins

{traffic_status}
{better_route_msg}
"""

        payload = {
            "content": message_content,
            "embeds": [{
                "title": "Route Visual",
                "image": {"url": map_image_url},
                "color": 16711680 if is_heavy_traffic else 65280 # Red if traffic, Green if clear
            }]
        }

        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("Notification sent successfully.")

    except Exception as e:
        print(f"Error running script: {e}")

if __name__ == "__main__":
    main()