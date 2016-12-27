from larry import Cache

def test_cache():
    cache = Cache()

    @cache.cache()
    def hello():
        return "hello"

    hello()
    hello()
    assert cache.funcs['hello'].hits == 1
    assert cache.funcs['hello'].misses == 1

def test_cache_params():
    cache = Cache()

    @cache.cache()
    def hello2(name):
        return "hello, {}".format(name)

    hello2('raphael')
    hello2('luke')
    hello2('raphael')
    hello2('luke')
    hello2('bob')
    assert cache.funcs['hello2'].hits == 2
    assert cache.funcs['hello2'].misses == 3
