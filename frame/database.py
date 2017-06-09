from pymongo import MongoClient
import pymongo


class DataBase(object):
    def __init__(self, d_db, l_task):
        # print('DataBase init test, although nothing now')
        self.client = MongoClient(host=d_db['host'], port=d_db['port'])
        self.database = self.client[d_db['database']]
        # print(self.client, self.database)

    def get_db(self):
        return self.database

    def get_collection(self, collection_name):
        return self.database[collection_name]

    def find(self, collection_name):
        coll = self.database[collection_name]
        return coll.find()

    def find_last_one(self, collection_name):
        coll = self.database[collection_name]
        # return coll.find().sort({'time': -1}).limit(1)
        return coll.find().sort('timestamp', -1).limit(1)

    def insert(self, collection_name, data):
        # print('DataBase insert')
        coll = self.database[collection_name]
        if isinstance(data, dict):
            result = coll.insert_one(data)
        elif isinstance(data, list):
            result = coll.insert_many(data)
        else:
            print('data error')
            pass
            # print(result.inserted_id)

    # list [('timestamp','ASCENDING')] [('timestamp','DESCENDING')]
    def create_index(self, collection_name, data):
        l = list()
        for i in data:
            t = tuple()
            if i[1] == 'ASCENDING':
                t = (i[0], pymongo.ASCENDING)
            elif i[1] == 'DESCENDING':
                t = (i[0], pymongo.DESCENDING)
            l.append(t)
        coll = self.database[collection_name]
        coll.create_index(l)

    def update(self):
        pass

    def remove(self):
        pass


if __name__ == '__main__':
    configs = {
        'db': {
            'host': '127.0.0.1',
            'port': 27017,
            'user': 'root',
            'password': "'",
            'database': 'crawler'
        }
    }
    s = 'okcoincn_rest_btc_ticker'
    a = DataBase(configs['db'], ['okcoincn_rest_btc_ticker'])
    # c = a.find_one(s)
    col = a.get_collection(s)
    print(col)
    c = a.find(s)
    c = a.find_last_one(s)
    print(c)
    for i in c:
        print(i)

    # for i in range(10000):
    #     data = {'time': i, 'buy': 100, 'sell': 200}
    #     a.create_index('okcoincn_rest_btc_ticker', [('timestamp', 'DESCENDING')])
    #     a.insert('okcoincn_rest_btc_ticker', data)
