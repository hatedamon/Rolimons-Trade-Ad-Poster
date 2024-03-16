# author @swedish.pyscho

USERNAME = "YourUsername"
INCLUDE_ON_HOLD = True # True or False
COOKIES = { # Use EditThisCookie on Rolimons to find these
    '_RoliData': 'Value',
    '_RoliVerification': 'Value'
}

import importlib.util
import sys

def Install(module_name):
    try:
        importlib.util.find_spec(module_name)
    except ImportError:
        print(f"Installing {module_name}...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        except Exception as e:
            print(f"Failed to install {module_name}: {e}")
            sys.exit(1)

required_modules = ["requests", "json", "time", "multiprocessing", "datetime"]
for module in required_modules:
    Install(module)

import requests
import json
import time
from multiprocessing import Process
from datetime import datetime

def ConvertID(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": True}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json().get("data")
        if data:
            return data[0].get("id")
    return None

def Limiteds(user_id, include_on_hold):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100&sortOrder=Asc"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json().get("data", [])
        filtered_items = [item for item in items if include_on_hold or not item.get("isOnHold")]
        sorted_items = sorted(filtered_items, key=lambda x: x.get("recentAveragePrice", 0), reverse=True)
        return [item["assetId"] for item in sorted_items[:4]]
    return []

def Post(trade_ad_counter, player_id, offer_item_ids):
    url = "https://www.rolimons.com/tradeapi/create"
    headers = {"Content-Type": "application/json"}
    payload = {
        "player_id": player_id,
        "offer_item_ids": offer_item_ids,
        "request_item_ids": [],
        "request_tags": ["upgrade", "demand", "any"]
    }
    with requests.Session() as session:
        response = session.post(url, headers=headers, cookies=COOKIES, data=json.dumps(payload))
        if response.status_code == 200:
            print("Trade ad posted successfully")
        else:
            print("Failed to post ad")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Posted at {timestamp} || Total: {trade_ad_counter}/60")

if __name__ == "__main__":
    user_id = ConvertID(USERNAME)
    if not user_id:
        print("Failed to find user ID for the username provided.")
        sys.exit(1)
    offer_item_ids = Limiteds(user_id, INCLUDE_ON_HOLD)
    if not offer_item_ids:
        print("Failed to find collectible items for the user.")
        sys.exit(1)
    
    trade_ad_counter = 0
    while True:
        trade_ad_counter += 1
        p = Process(target=Post, args=(trade_ad_counter, user_id, offer_item_ids))
        p.start()
        p.join()
        remaining_time = 1000
        while remaining_time > 0:
            progress = int((1000 - remaining_time) / 1000 * 20)
            percentage = int((1000 - remaining_time) / 1000 * 100)
            progress_bar = "[" + "#" * progress + " " * (20 - progress) + "]"
            print(f"\rPosting in {int(remaining_time)} || {progress_bar} {percentage}% | Total => {trade_ad_counter}", end="", flush=True)
            time.sleep(1)
            remaining_time -= 1
