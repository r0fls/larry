import logging
from sanic import Sanic
from sanic.response import text
from larry.backends import Redis
from larry import Cache

cache = Cache()
app = Sanic()

log = logging.getLogger()

# We set the cache to start at 1
# because the request object is not hashable
@app.route("/<param>")
@cache.cache(start=1, backend=Redis())
def hello(request, param):
    s = [i**2 for i in range(int(param))]
    log.info("hits: " + str(cache.funcs['hello'].hits))
    log.info("misses: " + str(cache.funcs['hello'].misses))
    return text(s[-1])

app.run(port=8000, debug=True)
