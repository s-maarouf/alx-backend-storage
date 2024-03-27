#!/usr/bin/env python3

"""Redis Module"""

import redis
import uuid
from typing import Union, Callable


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

    def get(self,
            key: str,
            fn: Callable = None) -> Union[str, int, bytes, float]:
        """retrieves key from stored data"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage"""
        return self.get(key, lambda x: int(x))
