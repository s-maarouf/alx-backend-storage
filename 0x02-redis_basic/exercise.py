#!/usr/bin/env python3

"""Redis Module"""

import redis
import uuid
from typing import Union


class Cache:
    """Cache class"""

    def __init__(self) -> None:
        """stores an instance of redis"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, int, bytes, float]) -> str:
        """returns generated key"""
        data_key = str(uuid.uuid1())
        self._redis.set(data_key, data)
        return data_key
