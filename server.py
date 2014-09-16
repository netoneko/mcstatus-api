#!/usr/bin/env python

from flask import Flask, request, jsonify
from minecraft_query import MinecraftQuery
from urlparse import urlparse
from os import getenv
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--redis-url", dest="redis_url", help="Redis URL", metavar="REDIS_URL")
parser.add_option("-s", "--simple", action="store_true", dest="simple_mode", default=False, help="Disable Redis")
parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Enable Flask debug mode")
parser.add_option("-p", "--port", action="store", type="int", dest="port", default=34500, help="HTTP server listen port")

(options, args) = parser.parse_args()

def init_redis():
  import redis
  url = urlparse(options.redis_url or 'redis://0@localhost:6379')
  return redis.StrictRedis(host=url.hostname, port=url.port, db=url.username)

app = Flask(__name__)
if not options.simple_mode:
  redis = init_redis()
else:
  redis = None

@app.route('/')
def index():
  return 'Nothing to look at'

@app.route('/api/status', methods=['GET'])
def status():
  host = request.args.get('host')
  try:
    port = int(request.args.get('port', default=25565))
  except Exception, e:
    port = 25565

  test = (host == 'test.mc.glassmoon.ru') 
  if test:
    return jsonify(players=['doge', 'such', 'wow', 'diamonds']) 
  
  result = None

  if redis:
    key = "%s:%s" % (host, str(port))
    result = redis.hgetall(key)

  if not result:
    try:
      result = MinecraftQuery(host, port).get_rules()
    except Exception as e:
      result = {'message': 'No response from the Minecraft server'}

    if redis:
      redis.hmset(key, result)
      redis.pexpire(key, 30000) # 30s

  return jsonify(**result)

if __name__ == '__main__':
  app.run(debug=options.debug, port=options.port)

