import redis
import json

from multiprocessing import Process


def sub():
    redis_client = redis.Redis(charset="utf-8", decode_responses=True)

    pubsub = redis_client.pubsub()
    pubsub.subscribe("message-broadcast")

    for message in pubsub.listen():
        if message.get("type") == "message":
            payload = json.loads(message.get("data"))
            print("Message picked up from the channel", payload)


if __name__ == "__main__":
    sub()
