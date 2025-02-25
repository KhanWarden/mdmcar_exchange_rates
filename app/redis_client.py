import redis
from redis.exceptions import DataError

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def save_exchange_rate(key: str, value: float) -> None:
    try:
        redis_client.set(key, value)
    except DataError as e:
        print(e)
