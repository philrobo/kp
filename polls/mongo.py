import pymongo
from pymongo import MongoClient


class parseMango(object):

    # self.response(chat_msg)
    # def __init__(self):
    #     return self.response()

    def mongo_response(self):
        return self.response()
        # return self.response(self.input)

    def response(self):
        client = MongoClient('localhost', 27017)
        db = client.local
        collection = db['errorCollection']
        cursor = collection.find({})
        for document in cursor:
            print(document['event']['timeStamp'])
            print(document['event']['message'])
        return "success"
