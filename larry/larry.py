import functools
from .backends import Redis
import dill

class Cache:

    def __init__(self):
        self.funcs = dict()

    def cache(self, start=0, backend=None):
        '''
        Decorate a function to make it cacheable.
        :param start: start cache key after argument number.
        :param exclude: exclude argument positions or names. Note that numeric
            args will exlude both the position in args and any kwargs with the
            numeric key. (NOT CURRENTLY IMPLEMENTED)
        :param backend: redis, mongo, file, custom, etc.. (NOT CURRENTLY IMPLEMENTED)
        '''

        def _cache(func):
            self.funcs[func.__name__] = func_cache = FunctionKey(func,
                                                                 backend)
            @functools.wraps(func)
            def new_func(*args, **kwargs):
                key = (
                       hash(args[start:]),
                       hash(tuple(sorted(kwargs.items())))
                      )
                if self.funcs[func.__name__].keys is not None:
                    key += (hash(tuple(dill.dumps(i) for i
                                       in self.funcs[func.__name__].keys)), )
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
        else:
            self.backend = backend


    def __getitem__(self, key):
        if isinstance(self.backend, dict):
            return self.backend.get(key)
        elif isinstance(self.backend, Redis):
            try:
                return dill.loads(self.backend.conn.get(key))
            except:
                return None

    def __setitem__(self, key, value):
        if isinstance(self.backend, Redis):
            self.backend.conn.set(key, dill.dumps(value))
        elif isinstance(self.backend, dict):
            self.backend[key] = value

    def get(self, key):
        if isinstance(self.backend, Redis):
            try:
                return dill.loads(self.backend.conn.get(key))
            except:
                return None
        try:
            return self.backend[key]
        except:
            return None
