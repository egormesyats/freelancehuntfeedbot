import requests
from db import Skill
import json
from log import log
from sign import sign
from secured.constants import API_SECRET, API_TOKEN
from constants import API_URL, START_MESSAGE, HELP_MESSAGE

def req_skills():
  log('API Request: /skills')
  url = API_URL + '/skills'
  method = 'GET'
  signature = sign(API_SECRET, url, method)
  r = requests.get(url, auth=(API_TOKEN, signature))
  print('X-Ratelimit-Remaining: ' + r.headers['X-Ratelimit-Remaining'] + '\n')
  skills = json.loads(r.text)
  for skill in skills:
    Skill.get_or_create(id=skill['skill_id'], name=skill['skill_name'])
  print('successfully added/updated skills on database\n')
  print('API Request: /skills END\n')

