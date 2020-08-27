
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from datetime import datetime

def load_episode(episode_url):
    session = HTMLSession()
    page = session.get(episode_url)
    page.html.render()
    soup = BeautifulSoup(page.html.raw_html, 'html.parser')
    episode_text_raw = soup.findAll("div", {"class": "release-content"})[0].text

    episode = dict()

    episode['songs'] = []

    for li in soup.findAll("div", {"class": "contents"})[0].find("ol").find_all("li"):
        episode['songs'].append(li.text)
        episode['text'] = episode_text_raw.replace(li.text, li.text+'\n')

    episode_date_str = soup.findAll("span", {"class": "small gray"})[0].text.split('|')[0].strip()
    episode['date'] = datetime.strptime(episode_date_str, '%d.%m.%Y').date()
    episode['id'] = soup.findAll("span", {"class": "small gray"})[0].text.split('|')[1].strip().replace('Выпуск ','')
    episode['title'] = soup.findAll("h1", {"class": "title"})[0].text

    return episode

def episodes_update(episodes, base_url, new_top_id):
    current_top_id = max(episodes.keys()) if bool(episodes) else 0
    print(current_top_id)

    for episode_id in range(current_top_id+1, new_top_id+1):
        episode = load_episode(base_url + str(episode_id))
        print(str(episode_id) + ' ' + episode['id'])
        episodes[episode_id] = episode
    
    return episodes

def episodes_write(episodes):
    with open(os.path.realpath(sys.argv[0]) + '/episodes.json', 'w') as f:
        json.dump(episodes, f, indent=4, sort_keys=True, default=str)

def episodes_read():
    with open(os.path.realpath(sys.argv[0]) + '/episodes.json') as f:
        return json.load(f)

def episodes_print(episodes):
    for ep in episodes.items():
        print(str(ep[1]['id']) + ' ' + str(ep[1]['date']) + ' ' + ep[1]['title'] + ' ' + str(len(ep[1]['songs']))  + ' ' + str(len(ep[1]['text'])))




base_url = 'https://aerostatbg.ru/release/'
episodes = dict()

print(episodes.keys())

episodes = episodes_update(episodes, base_url, 797)

episodes_print(episodes)

episodes_write(episodes)

eps = episodes_read()

episodes_print(eps)


















