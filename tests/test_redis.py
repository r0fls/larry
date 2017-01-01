import fakeredis
from larry.backends import Redis
from larry import Cache
from time import sleep

cache = Cache()


def test_cache():

    @cache.cache(backend=Redis(driver=fakeredis.FakeStrictRedis))
    def hello():
        return "hello"

    hello()
    r = hello()
    assert r == "hello"
    assert cache.funcs['hello'].hits == 1
    assert cache.funcs['hello'].misses == 1

def test_cache():

    @cache.cache(backend=Redis(driver=fakeredis.FakeStrictRedis),
                 expires=0.1)
    def hello_expires():
        return "hello"

    hello_expires()
    assert cache.funcs['hello_expires'].misses == 1
    sleep(0.2)
    hello_expires()
    assert cache.funcs['hello_expires'].misses == 2
