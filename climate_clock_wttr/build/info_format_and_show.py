from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

def show_info(list_info):

    CARBON_DEADLINE_1 = {
        "timestamp": datetime.fromisoformat(list_info["carbon_deadline_1"]["timestamp"]),
        "label": list_info["carbon_deadline_1"]["labels"][0]
    }
    RENEWABLES_1 = {
        "initial": list_info["renewables_1"]["initial"],
        "timestamp": datetime.fromisoformat(list_info["renewables_1"]["timestamp"]),
        "rate": list_info["renewables_1"]["rate"],
        "label": list_info["renewables_1"]["labels"][0]
    }
    INITIATIVE_30X30 = {
        "initial": list_info["green_climate_fund_1"]["initial"],
        "label": list_info["green_climate_fund_1"]["labels"][0],
        "unit": list_info["green_climate_fund_1"]["unit_labels"][0]
    }
    INDIGENOUS_LAND_1 = {
        "initial": list_info["indigenous_land_1"]["initial"],
        "label": list_info["indigenous_land_1"]["labels"][0],
        "unit": list_info["indigenous_land_1"]["unit_labels"][0]
    }
    NEWS_FEED_1 = {
        f"feed_{i+1}": list_info["newsfeed_1"]["newsfeed"][i]["headline"]
        for i in range(10)
    }

    # Calculate countdown
    now = datetime.now(timezone.utc)
    deadline_delta = relativedelta(CARBON_DEADLINE_1["timestamp"], now)
    years = deadline_delta.years
    rdays = relativedelta(months=deadline_delta.months, days=deadline_delta.days)
    days = ((rdays + now) - now).days
    hours = deadline_delta.hours
    minutes = deadline_delta.minutes
    seconds = deadline_delta.seconds

    # Calculate renewables percentage
    t = (now - RENEWABLES_1["timestamp"]).total_seconds()
    percent = RENEWABLES_1["rate"] * t + RENEWABLES_1["initial"]

    print("\n" + "="*80)
    print(f"  🌍 CLIMATE CLOCK  |  {datetime.now().strftime('%a %d %b %Y')}")
    print("="*80)
    print(f"  ⏳ {CARBON_DEADLINE_1['label']}")
    print(f"     {years} YRS  {days} DAYS  {str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}")
    print("-"*80)
    print(f"  ⚡ {RENEWABLES_1['label']}: {percent:.4f}%")
    print("-"*80)
    print(f"  🌱 {INITIATIVE_30X30['label']}: {INITIATIVE_30X30['initial']}{INITIATIVE_30X30['unit']}")
    print("-"*80)
    print(f"  🏔️  {INDIGENOUS_LAND_1['label']}: {INDIGENOUS_LAND_1['initial']} {INDIGENOUS_LAND_1['unit']}")
    print("-"*80)
    print("  📰 Climate News:")
    for i in range(1, 11):
        print(f"     {i}. {NEWS_FEED_1[f'feed_{i}']}")
    print("="*80 + "\n")

    return 0