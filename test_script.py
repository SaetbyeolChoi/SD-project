import json
import redis


cache = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

TQ = "transformer_queue"
LQ = "load_queue"

def add_to_transform_queue(data):
    cache.rpush(TQ, data)

    print("data added")
    print("look at data", cache.lrange(TQ,0,-1))

def add_to_load_queue(data):
    cache.rpush(LQ,data)
    print("data added")

add_to_load_queue(json.dumps({"test":"data"}))
add_to_transform_queue(json.dumps({"test":"data"}))