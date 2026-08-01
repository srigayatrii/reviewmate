from fastapi import APIRouter

from app.workers.redis_queue import queue

router = APIRouter(
    prefix="/worker",
    tags=["Worker"]
)


@router.get("/stats")
def worker_stats():

    return {
        "queue_name": queue.name,
        "queued_jobs": len(queue),
    }