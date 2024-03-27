#!/usr/bin/env python3

"""MongoDB module"""

from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """changes all topics of a doc"""
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
