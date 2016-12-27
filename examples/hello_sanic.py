from sanic import Sanic
from sanic.response import text
import logging

log = logging.getLogger()

app = Sanic()

from larry import Cache
cache = Cache()

# We set the cache to start at 1
# because the request object is not hashable
@app.route("/<param>")
@cache.cache(start=1)
def hello(request, param):
    s = [i**2 for i in range(int(param))]
    log.info("hits: "+ str(cache.hits))
    log.info("misses: "+ str(cache.misses))
    log.info(cache.store)
    return text(s[-1])

app.run(port=8000, debug=True)
