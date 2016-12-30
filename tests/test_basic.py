from larry import Cache

cache = Cache()

def test_cache():

    @cache.cache()
    def hello():
        return "hello"

    hello()
    hello()
    assert cache.funcs[hello].hits == 1
    assert cache.funcs['hello'].misses == 1


def test_keys():

    r = {'value': 1764}
    @cache.cache()
    def keys():
        cache.funcs['keys'].keys = r
        return int(r['value']**0.5)

    answer = keys()
    r['value'] = 16
    keys()
    four = keys()
    assert cache.funcs['keys'].hits == 1
    assert cache.funcs['keys'].misses == 2
    assert answer == 42
    assert four == 4


def test_cache_params():

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


def test_cache_objects():

    class FancyThing:
        def __init__(self, answer):
            self.answer = answer

    @cache.cache()
    def hello(fancy_thing):
        return "hello {}".format(fancy_thing.answer)

    my_fancy_thing = FancyThing(42)
    my_other_fancy_thing = FancyThing(9000)
    hello(my_fancy_thing)
    hello(my_fancy_thing)
    hello(my_other_fancy_thing)
    hello(my_other_fancy_thing)
    assert cache.funcs['hello'].hits == 2
    assert cache.funcs['hello'].misses == 2
