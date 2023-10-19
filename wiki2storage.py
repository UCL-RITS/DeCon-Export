"""
A quick script for running text through Confluence's conversion API end-point.
"""

import requests
import json
import time
import os
import sys
import argparse

hostname="wiki.ucl.ac.uk"

url = f"https://{hostname}/rest/api/contentbody/convert/"

with open("bearer.token") as f:
    token = f.read()

headers = {
  "Accept": "application/json",
  "Authorization": 'Bearer '+ os.getenv("CONFLUENCE_PAC"),
  #"Authorization": f"Bearer {token}",
  "Accept": "application/json",
  "Content-Type": "application/json"
}


def convert_format(page_text, f_from, f_to):
    response = requests.request(
       "POST",
       url + f_to,
       headers=headers,
       json={"value": page_text, "representation": f_from}   #{"value": page_text, "representation": "wiki"}
    )

    response.raise_for_status()

    rj = response.json()

    return rj

def w2s(page_text):
    return convert_format(page_text, "wiki", "storage")["value"]

def s2v(page_text):
    return convert_format(page_text, "storage", "view")["value"]

def w2v(page_text):
    return s2v(w2s(page_text))

# Valid conversions:
# Source Representation	Destination Representation Supported
# wiki	storage
# storage	view,export_view,styled_view,editor
# editor	storage
# view	None
# export_view	None
# styled_view	None
def main():
    parser = argparse.ArgumentParser(
                        prog='wiki2storage',
                        description='Converts Confluence wiki format to storage format',
                        epilog='-')
    parser.add_argument('filename', nargs="+") 
    args = parser.parse_args()

    for filename in args.filename:
        with open(filename, 'r') as f:
            s = str(f.read())
            print(w2v(s))

if __name__ == "__main__":
    main()
