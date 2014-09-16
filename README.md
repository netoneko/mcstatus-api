# mcstatus-api

Provides HTTP API for mcstatus ([https://github.com/Dinnerbone/mcstatus](https://github.com/Dinnerbone/mcstatus)).

`GET /api/status?host=HOSTNAME&port=PORT` will return you a convenient JSON object.

## Configuration options

* `-v` or `--verbose` enables debug mode
* `-r` or `--redis-url` allows to pass custom Redis URL
* `-s` or `--simple` disables connection to Redis

