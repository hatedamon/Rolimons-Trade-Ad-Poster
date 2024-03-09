# author @swedish.psycho, @hatedamon
import requests
import json
import time
from multiprocessing import Process

def fetch_cookies():
    url = "https://www.rolimons.com" # fetching ur rolidata and roliverification cookies to post in payload
    session = requests.Session()
    response = session.get(url)
    cookies = session.cookies.get_dict()
    return cookies

def post_trade_ad(): # use EditThisCookie extension to extract the RoliData and RoliVerification cookies from https://rolimons.com
    # EditThisCookie -> https://chromewebstore.google.com/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
    cookies = {
        '_RoliData': 'value here', # replace with ur RoliData cookie
        '_RoliVerification': 'value here' # replace with ur RoliVerification cookie
    }
    url = "https://www.rolimons.com/tradeapi/create"
    headers = {"Content-Type": "application/json"}
    payload = {
        "player_id": 879828802, # replace with ur player id, find in the url when u click ur roblox profile -> https://www.roblox.com/users/<userid>/profile
        "offer_item_ids": [439945661, 494291269, 628771505], # replace with ur offering item ids, find these at their catalog urls aswell -> https://www.roblox.com/catalog/<itemid>/Dominus-Empyreus example
        "request_item_ids": [], # do the same here but for the itemids ur requesting (max 4)
        "request_tags": ["any", "demand", "upgrade"] # u can use any, demand, rap, projecteds and whatever else rolimons offers. Max 4
    }
    with requests.Session() as session:
        response = session.post(url, headers=headers, cookies=cookies, data=json.dumps(payload)) # this is just posting it with the authorization cookies
        if response.status_code == 200:
            print("Failed") # it doesnt really respond or idk how to check so we're gonna assume it failed
            return True
        else:
            print("Posted ad") # same here
            return False 

if __name__ == "__main__": # function to create a countdown
    trade_ad_counter = 0
    while True:
        start_time = time.time()
        trade_ad_counter += 1
        p = Process(target=post_trade_ad)
        p.start()
        p.join()  
        elapsed_time = time.time() - start_time
        remaining_time = 1000 - elapsed_time
        while remaining_time > 0:
            print(f"\rNext trade ad in {int(remaining_time)} seconds | Total trade ads created: {trade_ad_counter}", end="", flush=True)
            time.sleep(1)
            elapsed_time += 1
            remaining_time = 1000 - elapsed_time # wait around 15 minutes to post another trade ad

