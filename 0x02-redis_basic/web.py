#!/usr/bin/env python3

"""Redis Module"""

import requests
import redis
from functools import wraps
from typing import Callable


def data_cacher(method: Callable) -> Callable:
    """Caches the output of fetched data"""
    @wraps(method)
    def invoker(url) -> str:
        """The wrapper function for caching the output"""
        redis.Redis().incr(f'count:{url}')
        result = redis.Redis().get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis.Redis().set(f'count:{url}', 0)
        redis.Redis().setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request"""
    return requests.get(url).text
