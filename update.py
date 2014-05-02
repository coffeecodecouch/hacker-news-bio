# command -> python update.py -u <user cookie>

import argparse
import requests
from bs4 import BeautifulSoup
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-u', required=True)
cookie = {'user': parser.parse_args().u}

def update_bio(about):
    url = 'https://news.ycombinator.com/user?id=coffeecodecouch'
    r = requests.get(url, cookies=cookie)
    dom = BeautifulSoup(r.text)

    payload = {
        'fnid': dom.find('input', {'name': 'fnid'})['value'],
        'about': about,
        'email': dom.find('input', {'name': 'email'})['value'],
        'showdead': 'yes',
        'noprocrast': 'no',
        'maxvisit': '20',
        'minaway': '180',
        'topcolor': dom.find('input', {'name': 'topcolor'})['value'],
        'delay': '0',
    }

    url = 'https://news.ycombinator.com/x'
    r = requests.post(url, data=payload, cookies=cookie)

    print('Success: ' + str(r.ok))

template = open('bio.txt', 'r').read()
update_bio(template)
pprint(template)
