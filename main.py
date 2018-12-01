import telebot 
import log
from secured import constants

bot = telebot.TeleBot(constants.botToken)
#bot.send_message(364451458, 'test3')
print(bot.get_me())

@bot.message_handler(content_types=['text'])
def handle_text(message):
  print(message)
  if message.text == 'a':
    bot.send_message(message.chat.id, 'b')
  elif message.text == 'b':
    bot.send_message(message.chat.id, 'c')
  else:
    bot.send_message(message.chat.id, 'd')

bot.polling(none_stop=True)