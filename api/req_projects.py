import __main__
import requests
import json
from collections import OrderedDict
from db import User, Skill
from log import log
from sign import sign
from secured.constants import API_SECRET, API_TOKEN
from constants import API_URL, API_PROJECTS_LOAD_NUMBER, START_MESSAGE, HELP_MESSAGE

DIVIDER = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

def format_project(project):
  title = project['name']
  link = project['url']
  skills = str(project['skills'])
  skills_more = ''
  for skill in project['skills']:
    s = Skill.select().where(Skill.name == skill)
    skills_more = skills_more + skill + ': /skill' + str(s[0].id) + '\n'
  budget = 'n/a'
  if 'budget_amount' in project:
    budget = str(project['budget_amount']) + ' ' + project['budget_currency_code']

  fstr = """*{title}*
    \n_Budget_: {budget}
    \n_Skills_: {skills}
    \n_Link_: {link}
    \n_Explore more projects for a specific skill_:\n{skills_more}""".format(
      title=title,
      link=link,
      budget=budget,
      skills=skills,
      skills_more=skills_more
    )
  return fstr

def req_projects(): 
  log('API Request: /projects')
  url = API_URL + '/projects?per_page=' + str(API_PROJECTS_LOAD_NUMBER)
  method = 'GET'
  signature = sign(API_SECRET, url, method)
  r = requests.get(url, auth=(API_TOKEN, signature))
  print('X-Ratelimit-Remaining: ' + r.headers['X-Ratelimit-Remaining'] + '\n')
  projects = json.loads(r.text)
  for project in reversed(projects):
    for user in User.select():
      if (user.latest_project_id < int(project['project_id'])):
        __main__.bot.send_chat_action(user.id, 'typing')
        __main__.bot.send_message(
          user.id, 
          '🆕 🆕 🆕\n\n' + str(format_project(project)), 
          parse_mode='Markdown')
        query = User.update(latest_project_id=project['project_id']).where(User.id == user.id)
        query.execute()
        print('\nlatest_project_id updated to: ' + str(project['project_id']))
        print('\nand sent for user.id: ' + str(user.id))
  print('\nAPI Request: /projects END\n')

def req_projects_by_skill_for_user(user_id, skill_id):
  log('API Request: /projects/skills=')
  url = API_URL + '/projects?per_page=' + str(API_PROJECTS_LOAD_NUMBER) + '&skills=' + str(skill_id)
  method = 'GET'
  signature = sign(API_SECRET, url, method)
  r = requests.get(url, auth=(API_TOKEN, signature))
  print('X-Ratelimit-Remaining: ' + r.headers['X-Ratelimit-Remaining'] + '\n')
  projects = json.loads(r.text)
  
  __main__.bot.send_chat_action(user_id, 'typing')
  __main__.bot.send_message(
    user_id, 
    DIVIDER + '\nProjects by skill ' + str(skill_id) + '\n' + DIVIDER, 
    parse_mode='Markdown')
  for project in reversed(projects):
    __main__.bot.send_chat_action(user_id, 'typing')
    __main__.bot.send_message(user_id, format_project(project), parse_mode='Markdown')
    print('\nproject_id: ' + str(project['project_id']))
    print('\nsent for user_id: ' + str(user_id))
  __main__.bot.send_chat_action(user_id, 'typing')
  __main__.bot.send_message(
    user_id, 
    DIVIDER + '\n// END of projects by skill ' + str(skill_id) + '\n' + DIVIDER, 
    parse_mode='Markdown')
  print('\nAPI Request: /projects END\n')
