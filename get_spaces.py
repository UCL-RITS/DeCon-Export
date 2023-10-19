import requests
import json
import time
import os

hostname="wiki.ucl.ac.uk"

url = f"https://{hostname}/rest/api/space"

token = os.getenv("CONFLUENCE_PAC", "")
if token == "":
    with open("bearer.token") as f:
        token = f.read().rstrip()

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {token}"
}

def get_one_spaces_page(start, limit):
    response = requests.request(
       "GET",
       url,
       headers=headers,
       params={'start': start, 'limit': limit}
    )

    rj = response.json()

    return rj

all_results = list()

start = 0
page_size = 50

keep_going = True

print("Collecting index of spaces (paginated)...")

while keep_going == True:
    rj = get_one_spaces_page(start,page_size)
    
    start = start + page_size

    if "next" not in rj["_links"]:
        print("Got final page.")
        keep_going = False
    else:
        print(f"Getting next page: start={start}")

    all_results.extend(rj["results"])
    time.sleep(0.5)


num_spaces = len(all_results)

print(f"Dumping info of {num_spaces} spaces to spaces.json")
with open('spaces.json', 'w') as f:
    json.dump(obj=all_results, fp=f, indent=3)

print("Done.")


