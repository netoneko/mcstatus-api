from flask import Flask, request, jsonify
from minecraft_query import MinecraftQuery
from urlparse import urlparse
from os import getenv
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--redis-url", dest="redis_url", help="Redis URL", metavar="REDIS_URL")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode")
parser.add_option("-s", "--simple", action="store_true", dest="simple", default=False, help="Disable cache")

(options, args) = parser.parse_args()

def init_redis():
  from redis import StrictRedis
  url = urlparse(options.redis_url or 'redis://0@localhost:6379')
  return StrictRedis(host=url.hostname, port=url.port, db=url.username)

app = Flask(__name__)
if not options.simple:
  redis = init_redis()

@app.route('/')
def index():
  return 'Nothing to look at'

@app.route('/api/status', methods=['GET'])
def status():
  host = request.args.get('host')
  port = request.args.get('port', default=25565)
  test = bool(request.args.get('test', default=False))
  result = None

  if not options.simple:
    key = "%s:%s" % (host, str(port))
    result = redis.hgetall(key)

  if not result:
    try:
      result = MinecraftQuery(host, port).get_rules()
    except Exception as e:
      result = {'message': 'Socket error, host is unreacheable'}

    if not options.simple:
      redis.hmset(key, result)
      redis.pexpire(key, 30000) # 30s

  if test:
    result['players'] = ['Wow', 'Such', 'Doge']

  return jsonify(**result)

if __name__ == '__main__':
  app.run(debug=options.verbose)
