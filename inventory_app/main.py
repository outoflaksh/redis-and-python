import random
import redis
import logging

from pprint import pprint

random.seed(42)
logging.basicConfig()

inventory_db = [
    {"name": "milk", "type": "dairy", "quantity": 120, "price": 20, "npurchased": 0},
    {"name": "butter", "type": "dairy", "quantity": 78, "price": 55, "npurchased": 0},
    {"name": "pen", "type": "office", "quantity": 340, "price": 10, "npurchased": 0},
]

inventory_db = {f"item:{random.getrandbits(20)}": i for i in inventory_db}

# pprint(inventory_db)

redis_client = redis.Redis(db=1)

# Redis pipelining to reduce the round-trip transactions from the db
with redis_client.pipeline() as pipe:
    for item_id, item_details in inventory_db.items():
        # .hmset() is deprecated. when using hset() instead, provide the dict as "mapping"
        pipe.hset(item_id, mapping=item_details)
    pipe.execute()

redis_client.bgsave()

# print(redis_client.keys())


# simulate a "purchase" request.
# we need to check if the item is in stock,
# then decrease quantity and increase npurchased,
# and lastly be mindful if anything affects
# inventory in between the first two steps (i.e. race condition)


class OutOfStockError(Exception):
    """
    Error when item is out of stock
    """


def purchase_item(redis_client: redis.Redis, item_id: str) -> None:
    with redis_client.pipeline() as pipe:
        error_count = 0

        # we are going to apply optimistic locking on the db for transaction using .watch()
        # this will allow redis server to immediately raise an error if in the time step 1 and step 2
        # happen, there arises a conflict for write -> eliminating race condition
        while True:
            try:
                # Get the available inventorty while also watching it for changes
                pipe.watch(item_id)
                nleft: int = int(redis_client.hget(item_id, "quantity"))
                if nleft > 0:
                    pipe.multi()
                    pipe.hincrby(item_id, "quantity", -1)
                    pipe.hincrby(item_id, "npurchased", 1)
                    pipe.execute()
                    break
                else:
                    # in case of no stock -> unwatch the pipe and raise the error
                    pipe.unwatch()
                    raise OutOfStockError(
                        f"Sorry! Item with id {item_id} is unavailable at the moment!"
                    )
            except:
                # confict occurred during watch and so repeat with while loop & log it
                error_count += 1
                logging.warning(
                    f"Watch error #{error_count} for id {item_id}; retrying..."
                )

    return None
