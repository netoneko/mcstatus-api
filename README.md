# mcstatus-api

Provides HTTP API for mcstatus ([https://github.com/Dinnerbone/mcstatus](https://github.com/Dinnerbone/mcstatus)).

`GET /api/status?host=HOSTNAME&port=PORT` will return you a convenient JSON object.

## Configuration options

Environment variable `REDIS_URL` points to your Redis installation which is used for cache.

