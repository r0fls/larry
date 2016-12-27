import redis

class Redis:
    def __init__(self, host='localhost', port=6379, db=0, driver=None):
        self.host = host
        self.port = port
        self.db = db
        if driver is None:
            self.conn = redis.StrictRedis(host=host, port=port, db=db)
        else:
            self.conn = driver()
        self.backend = 'redis'
