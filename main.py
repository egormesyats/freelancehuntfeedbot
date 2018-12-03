import telebot
import requests
import json
from db import launch, User, Skill
from log import log, log_incoming_command
from sign import sign
from api.req_skills import req_skills
from api.req_projects import req_projects, req_projects_by_skill_for_user
from secured.constants import BOT_TOKEN
from constants import API_URL, API_PROJECTS_UPDATE_RATE, START_MESSAGE, HELP_MESSAGE
from helpers import regex_skill
from apscheduler.schedulers.background import BackgroundScheduler

# db
launch()

# bot
bot = telebot.TeleBot(BOT_TOKEN)
log(bot.get_me())

# requests
req_skills()

def req():
  req_projects()

# background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(req, 'interval', seconds=API_PROJECTS_UPDATE_RATE)
scheduler.start()

@bot.message_handler(commands=['start'])
def handle_start(message):
  log_incoming_command(message)
  chat_id = message.chat.id
  bot.send_chat_action(chat_id, 'typing')
  bot.send_message(chat_id, START_MESSAGE)
  user, created = User.get_or_create(id=chat_id)
  if (created != False):
    req()

@bot.message_handler(commands=['help'])
def handle_help(message):
  log_incoming_command(message)
  chat_id = message.chat.id
  bot.send_chat_action(chat_id, 'typing')
  bot.send_message(chat_id, HELP_MESSAGE)

@bot.message_handler(commands=['skills'])
def handle_skills(message):
  log_incoming_command(message)
  chat_id = message.chat.id
  bot.send_chat_action(chat_id, 'typing')
  msg = 'Available skills list:\n\n'
  for skill in Skill.select():
    msg = msg + '/skill' + str(skill.id) + ' - ' + skill.name + '\n'
  bot.send_message(chat_id, msg)

@bot.message_handler(func=lambda message: regex_skill(message.text))
def handle_skills_regex(message):
  log_incoming_command(message)
  chat_id = message.chat.id
  skill_id = message.text.replace('/skill', '')
  req_projects_by_skill_for_user(chat_id, skill_id)

bot.polling(none_stop=True)