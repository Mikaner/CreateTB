from Config import Config
import redis
from rq import Queue


class RedisQueue(Queue):
    def __init__(self):
        super().__init__(connection=redis.from_url(Config().get_redis_url()), default_timeout=10800)