from flask import Flask, request, jsonify
from minecraft_query import MinecraftQuery

app = Flask(__name__)

@app.route('/')
def index():
  return 'Nothing to look at'

@app.route('/api/status', methods=['GET'])
def status():
  host = request.args.get('host')
  port = request.args.get('port', default=25565)

  try:
    query = MinecraftQuery(host, port).get_rules()
    return jsonify(**query)
  except:
    return jsonify({'message': 'Socket error, host is unreacheable'}), 500

if __name__ == '__main__':
  app.run(debug=True)
