#!/usr/bin/env python3

"""Redis Module"""

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts how many times Cache was called"""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs/outputs"""
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output"""
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method"""
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fcn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fcn_name)
    out_key = '{}:outputs'.format(fcn_name)
    fcn_call_count = 0
    if redis_store.exists(fcn_name) != 0:
        fcn_call_count = int(redis_store.get(fcn_name))
    print('{} was called {} times:'.format(fcn_name, fcn_call_count))
    fcn_inputs = redis_store.lrange(in_key, 0, -1)
    fcn_outputs = redis_store.lrange(out_key, 0, -1)
    for fcn_input, fcn_output in zip(fcn_inputs, fcn_outputs):
        print('{}(*{}) -> {}'.format(
            fcn_name,
            fcn_input.decode("utf-8"),
            fcn_output,
        ))


class Cache:
    """Cache class"""

    def __init__(self) -> None:
        """stores an instance of redis"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
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
