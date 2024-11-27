from datetime import timedelta

from app.db.database import redis_client

RESERVED_TIME = 15

def reserved_seat_create_key(movie_id, seat_number) -> str:
    return f"movie:{movie_id}:seat:{seat_number}"

def seat_ttl(key):
    return redis_client.ttl(key)

def is_seat_exists(key):
    return redis_client.exists(key)

def reserve_seat(key):
    redis_client.setex(
        name=key,
        time=timedelta(minutes=RESERVED_TIME),
        value="reserved"
    )