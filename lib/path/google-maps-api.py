import requests

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#')
    )

def get_dist_dur(api_key, start, end):
    # For lat/lon: https://maps.googleapis.com/maps/api/geocode/json
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": start,
        "destinations": end,
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            distance = data["rows"][0]["elements"][0]["distance"]["text"]
            duration = data["rows"][0]["elements"][0]["duration"]["text"]
            return distance, duration
        else:
            print("Request failed.")
            return None, None
    else:
        print("Failed to make the request.")
        return None, None

api_key = vars_dict["MAPS_KEY"]


start = "Palace Lucerna, Nové Město"
end = "Project FOX, Praha 3-Žižkov"
distance, duration = get_dist_dur(api_key, start, end)

if distance and duration:

    print(f"Driving Distance: {distance}")

    print(f"Driving Duration: {duration}")