import redis
import json


def pub():
    payload = {"message": "hello", "from": 123}

    redis_client = redis.Redis(charset="utf-8", decode_responses=True)

    redis_client.publish("message-broadcast", json.dumps(payload))


if __name__ == "__main__":
    pub()
