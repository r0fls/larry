import redis

class Redis:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.conn = redis.StrictRedis(host=host, port=port, db=db)
        self.backend = 'redis'
