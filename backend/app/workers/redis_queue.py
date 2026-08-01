from redis import Redis
from rq import Queue


redis_connection = Redis(
    host="redis",
    port=6379,
    decode_responses=False
)

queue = Queue(
    "reviewmate",
    connection=redis_connection
)