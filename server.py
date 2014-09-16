from flask import Flask, request, jsonify
from minecraft_query import MinecraftQuery
from urlparse import urlparse
from os import getenv
from redis import StrictRedis

def init_redis():
  url = urlparse(getenv('REDIS_URL', default='redis://0@localhost:6379'))
  return StrictRedis(host=url.hostname, port=url.port, db=url.username)

app = Flask(__name__)
redis = init_redis()

@app.route('/')
def index():
  return 'Nothing to look at'

@app.route('/api/status', methods=['GET'])
def status():
  host = request.args.get('host')
  port = request.args.get('port', default=25565)
  test = bool(request.args.get('test', default=False))

  key = "%s:%s" % (host, str(port))
  result = redis.hgetall(key)

  if not result:
    try:
      result = MinecraftQuery(host, port).get_rules()
    except Exception as e:
      result = {'message': 'Socket error, host is unreacheable'}

    redis.hmset(key, result)
    redis.pexpire(key, 30000) # 30s

  if test:
    result['players'] = ['Wow', 'Such', 'Doge']

  return jsonify(**result)

if __name__ == '__main__':
  app.run(debug=True)
