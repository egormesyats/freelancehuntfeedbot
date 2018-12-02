import datetime

def get_timestamp():
  ts = datetime.datetime.now().timestamp()
  return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')