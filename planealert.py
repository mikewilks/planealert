""" Plane Alert """
import json
import time
import math
import requests
import apprise


def fetch_json_from_url(url):
    """ Load json from the url"""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def on_aircraft_found(apprise_object, aircraft, distance):
    """ Called when an aircraft is found, notifies with apprise"""
    # Format the data to display
    formatted_altitude = f"{aircraft['alt_baro']:,}"
    formatted_distance = round(distance, 2)

    # Notify using apprise
    apprise_object.notify(title="Aircraft Seen",
                          body=f"Hex ID {aircraft['hex']}, "
                               f"{formatted_distance} miles away at {formatted_altitude} feet")


def haversine_distance(lat1, lon1, lat2, lon2):
    """ Haversine formula to calculate distance between two latitude-longitude points"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    distance_lat = lat2 - lat1
    distance_lon = lon2 - lon1
    a = (math.sin(distance_lat / 2) ** 2 + math.cos(lat1) *
         math.cos(lat2) * math.sin(distance_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius = 3956  # Radius of Earth in miles
    return radius * c


def main():
    """Main function to periodically check the URL for specified aircraft"""
    with open("params.json", "r") as file:
        print('loading params')
        params = json.load(file)

    url = params["url"]
    hex_ids = params["hex_ids"]
    interval = params["interval"]
    target_lat = params["location"]["latitude"]
    target_lon = params["location"]["longitude"]
    max_distance = params["distance"]
    found_aircraft = []

    # Set up the apprise object ready for notifications
    apprise_object = apprise.Apprise()
    apprise_object.add(params['notify_url'])

    # Main loop
    while True:
        data_dict = fetch_json_from_url(url)
        aircraft_list = data_dict.get("aircraft", [])

        for hex_id in hex_ids:
            if hex_id not in found_aircraft:
                aircraft = next((a for a in aircraft_list if a["hex"] == hex_id), None)
                if aircraft:
                    aircraft_lat = aircraft["lat"]
                    aircraft_lon = aircraft["lon"]
                    distance = haversine_distance(target_lat, target_lon,
                                                  aircraft_lat, aircraft_lon)
                    if distance <= max_distance:
                        on_aircraft_found(apprise_object, aircraft, distance)
                        found_aircraft.append(hex_id)

        if set(hex_ids) == set(found_aircraft):
            break

        time.sleep(interval)


# To run the script, call the main function:
main()
