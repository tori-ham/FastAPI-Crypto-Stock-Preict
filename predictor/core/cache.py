import os
import json 

import redis 
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")

redis = redis.Redis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    db = REDIS_DB,
    decode_responses = True
)

def getCachedPrices( symbol : str ) -> list[float] | None:
    key = f"prices:{symbol}"
    data = redis.get(key)
    return json.loads(data) if data else None

def setCachedPrices( symbol : str, prices : list[float], ttl : int = 60 ):
    key = f"prices:{symbol}"
    redis.set(key, json.dumps(prices), ex = ttl)

