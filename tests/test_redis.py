import fakeredis
from larry.backends import Redis
from larry import Cache

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


