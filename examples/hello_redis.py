from larry.backends import Redis
from larry import Cache
from time import sleep

cache = Cache()

# because the request object is not hashable
@cache.cache(backend=Redis(host='localhost', port=6379), expires=3)
def hello(param):
    s = [i**2 for i in range(int(param))]
    print("hits: " + str(cache.funcs['hello'].hits))
    print("misses: " + str(cache.funcs['hello'].misses))
    return text(s[-1])
# miss
hello(100000)
# hit
hello(100000)
# expire cache
sleep(3)
# miss
hello(100000)
