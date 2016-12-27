from larry import Cache

def test_cache():
    cache = Cache()

    @cache.cache()
    def hello():
        return "hello"

    hello()
    hello()
    assert cache.hits == 1
    assert cache.misses == 1

def test_cache_params():
    cache = Cache()

    @cache.cache()
    def hello2(name):
        return "hello, {}".format(name)

    hello2('raphael')
    hello2('luke')
    hello2('raphael')
    print(cache.store)
    assert cache.hits == 1
    assert cache.misses == 2
