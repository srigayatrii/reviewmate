from redis import Redis
from rq import Queue

from app.core.config import settings


redis_connection = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=False,
)

queue = Queue(
    "reviewmate",
    connection=redis_connection,
)