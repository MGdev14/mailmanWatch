# This is a sample Python script.
import json
import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def read_secrets() -> dict:
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        print("ERROR: secrets.json missing")
        exit(1)


def readMailman(URL):
    page = requests.get(URL)
    #print(page.content)
    return page.content


def parsePage(page):
    bs = BeautifulSoup(page, 'html.parser')
    em = bs.find_all('em')
    #print(em[1])
    count = em[1]
    count = count.getText()
    count = count.split(' ')
    # count = count.split(' ')
    print("Aktuell " + count[0] + " Empfänger.")
    return int(count[0])


def write_db(timestamp, count, apiURL):
    ts = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    myobj = {'date': ts, 'word_count': count}
    print(myobj)
    x = requests.post(apiURL, data=myobj)
    print(x.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    secrets = read_secrets()
    URL = secrets['adminURL'] + "?adminpw=" + secrets['adminPW']
    page = readMailman(URL)
    count = parsePage(page)
    timestamp = int(time.time())
    write_db(timestamp, count, secrets['apiURL'])

# secrets.json required:
#
# {
#     "adminURL": "",
#     "adminPW": "",
#     "apiURL": ""
#
# }
