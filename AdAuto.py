# author @swedish.psycho

import importlib.util
import sys

# module installation
def install_module(module_name):
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
    install_module(module)

import requests
import json
import time
from multiprocessing import Process
from datetime import datetime

# fetch ur rolimons RoliData and RoliVerification cookies
def fetch_cookies():
    url = "https://www.rolimons.com"
    session = requests.Session()
    response = session.get(url)
    cookies = session.cookies.get_dict()
    return cookies

# replace RoliData and RoliVerification with the respective cookie values. 
# go to https://rolimons.com and use EditThisCookie to retrieve these (or app storage if yk how)
def post_trade_ad(trade_ad_counter): 
    cookies = {
        '_RoliData': 'ValueHere',
        '_RoliVerification': 'ValueHere'
    }
    url = "https://www.rolimons.com/tradeapi/create"
    headers = {"Content-Type": "application/json"}
    payload = {
        "player_id": 879828802, # replace with your UserID, find this after clicking the "Profile" www.roblox.com/users/<UrIDsHere>/profile
        "offer_item_ids": [439945661, 494291269, 628771505, 564449640], # max 4, replace with ur ItemIDs u wanna offer. u can find here -> www.roblox.com/catalog/<ItemID/<name>
        "request_item_ids": [1744060292, 51346471], # same process applys here but with what items ur looking for, max 4 
        "request_tags": ["any", "adds"] # these take up request slots aswell u need under 4 requests.
    }
    with requests.Session() as session: # making the request with ur cookie data to validate it
        response = session.post(url, headers=headers, cookies=cookies, data=json.dumps(payload))
        if response.status_code == 200: # this doesnt work but ok
            print("Failed to post ad")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Posted at {timestamp} || Total: {trade_ad_counter}/60")

# making console look pretty
if __name__ == "__main__":
    trade_ad_counter = 0
    while True:
        trade_ad_counter += 1
        p = Process(target=post_trade_ad, args=(trade_ad_counter,))
        p.start()
        p.join()
        remaining_time = 903  
        while remaining_time > 0:
            progress = int((903 - remaining_time) / 903 * 20) # 903 to counter accidentally posting before countdown ends
            percentage = int((903 - remaining_time) / 903 * 100) 
            progress_bar = "[" + "|" * progress + " " * (70 - progress) + "]"
            print(f"\rPosting in {int(remaining_time)} || {progress_bar} {percentage}% | Total => {trade_ad_counter}", end="", flush=True)
            time.sleep(1)
            remaining_time -= 1
