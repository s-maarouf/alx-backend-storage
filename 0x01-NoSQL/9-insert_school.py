#!/usr/bin/env python3

"""MongoDB module"""

from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """A script that inserts a new doc in a collection"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
