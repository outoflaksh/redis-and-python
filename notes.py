import redis

# Redis is the central class of the package
redis_client = redis.Redis()

# setting multiple keys by passing a dict
redis_client.mset({"name": "foo", "age": 20})


# single key setting
redis_client.set("name2", "bar")


# by default the value is returned as bytes
print(redis_client.get("name"))

# to receive the value as string add the decode method
print(redis_client.get("name").decode("utf-8"))

# pipelining in Redis can help reduce multiple round-trip transactions
with redis_client.pipeline() as pipe:
    for i in range(3):
        pipe.set(i, f"value {i}")
    pipe.execute()  # execute all commands in buffer in one go as a single transaction -> atomic


# we can set an expiration time for keys using setex method
from datetime import timedelta
from time import sleep

# r.setex(key, time, value) -> for string:string pair
redis_client.setex("key1", timedelta(minutes=1), value="some value")

# another way is to use the .expire() method
redis_client.set("key2", "some value 2")
redis_client.expire("key2", timedelta(minutes=1))

print("before expiry", redis_client.get("key2"))
sleep(60)
print("after expiry", redis_client.get("key2"))
