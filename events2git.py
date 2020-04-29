#! /usr/bin/env python3
 
from sseclient import SSEClient
import json
import os
import requests
import time
import git
import logging
import sys

 
logging.basicConfig(stream=sys.stdout)
 
 
event_type = os.getenv('event_type')
marathon_api_url = os.getenv('marathon_api_url')
repo_path = os.getenv('repo_path')

# print(event_type)
# if event_type is None:
#     exit(1)
 
#event_type = 'api_post_event'
#marathon_api_url = '0.0.0.0:8080'
#repo_path = 'repo'
 
 
def save_json(id, app_definition):
    id = id.split('/')
    filename = id.pop()
    path = '/'.join(id)

    if os.path.isfile(repo_path):
       git.Repo(repo_path)
    else:
       git.Repo.init(repo_path)

    repo = git.Repo(repo_path)

    os.makedirs(repo_path + '/' + path, exist_ok=True)
    with open(repo_path + '/' + path + '/%s.json' % filename, 'w+', encoding='utf-8') as f:
        json.dump(app_definition, f, ensure_ascii=False, indent=4)
    print('File saved: ' + repo_path + '/' + path + '/%s.json' % filename)
    full_path = repo_path + path + '/%s.json' % filename
    try:
        repo.git.add(A=True)
        repo.index.commit('Added new config for ' + full_path)
        print("Success save config")
        return True
    except:
        print("Error git automation")
        return False
 
 
def get_server():
    leader = None
    time.sleep(1)
    try:
        data = requests.get('http://%s/v2/leader' % marathon_api_url)
    except:
        return leader
    leader = data.content.decode()
    leader = json.loads(leader)['leader']
    print('Leader: %s' % leader)
 
    return leader
 
def connector():
    time.sleep(1)
    messages = None
    try:
        leader = get_server()
        messages = SSEClient('http://%s/v2/events?event_type=%s' % (leader, event_type))
    except Exception as e:
        print(e)
        connector()
    print('connected')
    return messages
 
 
 
while True:
    try:
        messages = connector()
        for msg in messages:
            event = str(msg.event)
            if event == event_type:
                print('Event: %s' % event)
                print('Data: %s' % str(msg.data))
                data = json.loads(msg.data)
                id = data['appDefinition']['id'][1:]
                app_definition = data['appDefinition']
                save_json(id, app_definition)
    except Exception as e:
        print(e)
        connector()
        pass