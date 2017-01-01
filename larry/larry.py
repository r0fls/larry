import functools
from .backends import Redis
import dill

class Cache:

    def __init__(self): self.funcs = Funcs()

    def cache(self, start=0, backend=None, expires=None):
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
                       args[start:],
                       tuple(sorted(kwargs.items()))
                      )
                if self.funcs[func.__name__].keys is not None:
                    key += tuple(dill.dumps(i) for i
                                       in self.funcs[func.__name__].keys)
                key = hash(key)
                if not func_cache.store.get(key):
                    func_cache.misses += 1
                    if expires is None:
                        func_cache.store[key] = func(*args, **kwargs)
                    else:
                        func_cache.store.set(key, func(*args, **kwargs),
                                             expires=expires)
                else:
                    func_cache.hits += 1
                return func_cache.store[key]
            return new_func

        return _cache


class Funcs:
    def __init__(self):
        self.funcs = dict()

    def __getitem__(self, key):
        if callable(key):
            key = key.__name__
        return self.funcs[key]

    def __setitem__(self, key, value):
        self.funcs[key] = value

    def get(self, key, default=None):
        try:
            return self[key]
        except:
            return default


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


    def set(self, key, value, expires=None):
        if expires is None:
            self.backend.conn.setex(key, dill.dumps(value))
        else:
            self.backend.conn.set(key, dill.dumps(value), expires)


    def get(self, key, default=None):
        try:
            if isinstance(self.backend, Redis):
                return dill.loads(self.backend.conn.get(key))
            else:
                return self.backend[key]
        except:
            return default
