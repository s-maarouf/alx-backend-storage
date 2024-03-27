#!/usr/bin/env python3

"""MongoDB module"""

from pymongo import MongoClient


def list_all(mongo_collection):
  """Lists all documents in a collection"""
  for doc in mongo_collection:
    mongo_collection.find()
    
  return doc
