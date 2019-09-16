import redis
import rq
import logging
from Config import Config
from music.utils.RedisQueue import RedisQueue

logger = logging.getLogger("rq.worker")
#logger.addHandler(logging.StreamHandler())

def main():
    with rq.Connection(redis.from_url(Config().get_redis_url())):
        worker = rq.Worker(["default"])
        print("now worker started")
        worker.work()

if __name__ == "__main__":
    main()