import requests
from config.config import GOOGLE_API_KEY, GOOGLE_ROUTES_API, GOOGLE_STATIC_MAPS_API, ORIGIN, DESTINATION, ZOOM_LEVEL

# Gets route data from Routes API
def get_route_data(travel_mode, alternatives=False):
    base_url = GOOGLE_ROUTES_API
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }
    
    body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": ORIGIN["lat"],
                    "longitude": ORIGIN["lng"]
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": DESTINATION["lat"],
                    "longitude": DESTINATION["lng"]
                }
            }
        },
        "travelMode": travel_mode,
        "routingPreference": "TRAFFIC_AWARE" if travel_mode in ["DRIVE", "TWO_WHEELER"] else None,
        "computeAlternativeRoutes": alternatives,
        "units": "METRIC"
    }

    if travel_mode == "TRANSIT":
        body.pop("routingPreference", None)

    response = requests.post(base_url, json=body, headers=headers)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    return response.json()

# Generates static map image of the route from Static Maps API
def generate_static_map_url(polyline, origin_lat, origin_lng, dest_lat, dest_lng):
    base_url = GOOGLE_STATIC_MAPS_API
    
    origin_marker = f"markers=color:blue%7Clabel:H%7C{origin_lat},{origin_lng}"
    dest_marker = f"markers=color:red%7Clabel:O%7C{dest_lat},{dest_lng}"
    
    params = [
        "size=1600x1600",
        f"zoom={ZOOM_LEVEL}",
        "maptype=roadmap",
        f"path=enc:{polyline}",
        origin_marker,
        dest_marker,
        f"key={GOOGLE_API_KEY}"
    ]
    return base_url + "&".join(params)