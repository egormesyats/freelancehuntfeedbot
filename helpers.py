import re

def regex_skill(text):
  match = re.match(r'/skill[1-9]\d*', text)
  if match == None:
    return False
  else:
    return True