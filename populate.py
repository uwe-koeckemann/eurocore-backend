#!/bin/bash
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
url = 'http://127.0.0.1:8000'

# Simple script that adds some basic content


def populate_keywords_from_file(name: str):
    with open(name) as file:
        keywords = file.read().splitlines()
        for word in keywords:
            word = word.strip()
            if word.strip() != "" and not word.startswith("#"):
                word = word.replace(" ", "_")
                print(word)
                response = session.post(f"{url}/tag/create", json={'name': word})
                print(response.status_code)


def populate_relations_from_file(name: str):
    with open(name) as file:
        lines = file.read().splitlines()[1:]
        for line in lines:
            parts = line.split(",")
            relation_json = {
                'name': parts[0].strip(),
                'inverse_name': parts[1].strip(),
                'topic': parts[2].strip(),
                'inverse_topic': parts[3].strip(),
                'description': parts[4].strip()
            }
            response = session.post(f"{url}/relation_type/create", json=relation_json)
            print(response.status_code)


# populate_keywords_from_file('./sample-data/keywords/filetype.txt')
# populate_keywords_from_file('./sample-data/keywords/functional.txt')
# populate_keywords_from_file('./sample-data/keywords/RAL.txt')
# populate_keywords_from_file('./sample-data/keywords/type.txt')
#
# populate_relations_from_file('./sample-data/relations.csv')

answer = session.post(f"{url}/entry/create", json={
    'name': 'AIDDL',
    'url': 'aiddl.org',
    'description': 'Awesome Framework',
    'tags': [{'name': 'AIDDL'}, {'name': 'Framework'}]
})
print(answer.status_code)
print(answer.text)

# answer = session.get(f"{url}/relation_type/get-all")
# for e in answer.json():
#     print(e)


#answer = session.get(f"{url}/relation_type/1")
#print(answer.status_code)
#print(answer.text)

