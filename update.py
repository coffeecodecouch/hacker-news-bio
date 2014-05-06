import os
from pymongo import MongoClient
import tweetpony
import github
import json
import requests
from bs4 import BeautifulSoup

fn = os.path.join(os.path.dirname(__file__), 'config.txt')
conf = dict((line.strip().split(' = ') for line in file(fn)))
db = MongoClient('localhost', 27017).hackernewsbio

def parse_twitter(temp):
    twitter = tweetpony.API(
        conf['tw_api_key'],
        conf['tw_api_secret'],
        conf['tw_acc_token'],
        conf['tw_tok_secret']
    )
    followers = json.loads(twitter.followers().json)['users']
    name = str(followers[0]['screen_name'].ljust(15))
    return temp.replace('{{tw_follower}}', name)

def parse_github(temp):
    gh = github.GitHub(username=conf['gh_user'], password=conf['gh_pass'])

    followers = str(gh.users('coffeecodecouch').get()['followers']).ljust(24)
    return temp.replace('{{gh_followers}}', followers)

def update_bio(about):
    url = 'https://news.ycombinator.com/user?id=coffeecodecouch'
    cookie = {'user': conf['cookie']}
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
template = parse_twitter(template)
template = parse_github(template)
update_bio(template)
