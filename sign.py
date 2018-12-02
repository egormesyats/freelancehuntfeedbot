import base64
import hmac,hashlib

def sign(api_secret, url, method, post_params = ''):
  return base64.b64encode(
    hmac.new(
      b''.join([str.encode(api_secret)]),
      b''.join([str.encode(url), str.encode(method), str.encode(post_params)]),
      hashlib.sha256
    ).digest()
  ).decode("utf-8")