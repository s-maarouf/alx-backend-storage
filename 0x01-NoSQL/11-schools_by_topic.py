#!/usr/bin/env python3

"""MongoDB module"""

from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """Returns a  list of school having a specefic topic"""
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
