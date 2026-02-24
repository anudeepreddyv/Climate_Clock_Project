import json
import requests

def get_info():
    url = "https://api.climateclock.world/v1/clock"
    response = requests.get(url)
    parsed = json.loads(response.text)

    carbon_deadline_1 = parsed["data"]["modules"]["carbon_deadline_1"]
    renewables_1 = parsed["data"]["modules"]["renewables_1"]
    indigenous_land_1 = parsed["data"]["modules"]["indigenous_land_1"]
    initiative_30x30 = parsed["data"]["modules"]["initiative_30x30"]
    newsfeed_1 = parsed["data"]["modules"]["newsfeed_1"]

    return {
        "carbon_deadline_1": carbon_deadline_1,
        "renewables_1": renewables_1,
        "green_climate_fund_1": initiative_30x30,
        "indigenous_land_1": indigenous_land_1,
        "newsfeed_1": newsfeed_1
    }