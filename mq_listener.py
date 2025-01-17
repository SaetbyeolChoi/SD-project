import asyncio
import redis
import json

cache = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

TQ = "transformer_queue"
LQ = "load_queue"

def add_to_transform_queue(data):
    cache.rpush("transformer_queue", data)

def add_to_load_queue(data):
    cache.rpush("load_queue",data)


async def queue_listener(queue):
    while True:
        print("current Queue", queue)
        if cache.llen(queue) == 0:
            print("empty", cache.lrange(queue,0,-1))
        else:
            data = cache.lpop(queue)
            print("look at",data)
        await asyncio.sleep(1)
async def main():
    t1 = asyncio.create_task(queue_listener(TQ))
    t2 = asyncio.create_task(queue_listener(LQ))

    await asyncio.gather(t1,t2)


asyncio.run(main())