from pymongo import MongoClient
import pymongo
class DataBase(object):
    def __init__(self, d_db, l_task):
        # print('DataBase init test, although nothing now')
        self.client = MongoClient(host=d_db['host'], port=d_db['port'])
        self.database = self.client[d_db['database']]
        # print(self.client, self.database)

    def connect(self):
        pass

    def query(self):
        pass

    def insert(self, collection_name, data):
        print('DataBase insert')
        coll = self.database[collection_name]
        result = coll.insert_one(data)
        # print(result.inserted_id)

    # list [('timestamp','ASCENDING')] [('timestamp','DESCENDING')]
    def create_index(self, collection_name, data):
        print(data)
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
    a = DataBase(configs['db'], ['okcoincn_rest_btc_ticker'])
    for i in range(10):
        data = {'time': i,'buy':100,'sell':200}
        a.create_index('okcoincn_rest_btc_ticker',[('timestamp','DESCENDING')])
        a.insert('okcoincn_rest_btc_ticker', data)