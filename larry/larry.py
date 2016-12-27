import functools
from .backends import Redis

class Cache:

    def __init__(self):
        self.funcs = dict()

    def cache(self, start=0, keys=[], backend=None):
        '''
        Decorate a function to make it cacheable.
        :param start: start cache key after argument number.
        :param exclude: exclude argument positions or names. Note that numeric
            args will exlude both the position in args and any kwargs with the
            numeric key. (NOT CURRENTLY IMPLEMENTED)
        :param keys: string list of extra keys that are not defined at function
            execution, e.g. `request.body` is typically  something that should
            be in cache key, but isn't an explicit function argument.
        :param backend: redis, mongo, file, custom, etc.. (NOT CURRENTLY IMPLEMENTED)
        '''

        # TODO
        # Fix the eval situation
        def _cache(func):
            self.funcs[func.__name__] = func_cache = FunctionKey(func,
                                                                 backend)
            @functools.wraps(func)
            def new_func(*args, **kwargs):
                key = (
                       hash(args[start:] + tuple(eval(i) for i in keys)),
                       hash(tuple(sorted(kwargs.items())))
                      )
                if not func_cache.store.get(key):
                    func_cache.misses += 1
                    func_cache.store[key] = func(*args, **kwargs)
                else:
                    func_cache.hits += 1
                return func_cache.store[key]
            return new_func

        return _cache


class FunctionKey:
    def __init__(self, func, backend=None, keys=None):
        self.func = func
        self.hits = 0
        self.misses = 0
        self.keys = None
        self.store = CacheStore(backend)


class CacheStore:

    def __init__(self, backend=None):
        if backend is None:
            self.backend = dict()


    def __getitem__(self, key):
        if isinstance(self.backend, dict):
            return self.backend.get(key)


    def __setitem__(self, key, value):
        if isinstance(self.backend, Redis):
            self.backend.set(key, value)
        elif isinstance(self.backend, dict):
            self.backend[key] = value

    def get(self, key):
        try:
            return self.backend[key]
        except:
            return None
