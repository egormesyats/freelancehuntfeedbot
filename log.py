from timestamp import get_timestamp

LOG_DIVIDER = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

def log(message):
  print(LOG_DIVIDER)
  print(get_timestamp())
  print(message)
  print('')

def log_incoming_command(message):
  print(LOG_DIVIDER)
  print(get_timestamp())
  print('incoming command: ' + message.text)
  print('message_id: ' + str(message.message_id))
  print('from_user: ')
  print('-> id: ' + str(message.from_user.id))
  print('-> is_bot: ' + str(message.from_user.is_bot))
  print('-> username: ' + str(message.from_user.username))
  print('-> first_name: ' + str(message.from_user.first_name))
  print('-> last_name: ' + str(message.from_user.last_name))
  print('')