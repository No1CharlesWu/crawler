from pymongo import MongoClient

class DataBase(object):
    def __init__(self, d_db, l_task):
        print('DataBase init test, although nothing now')
        self.client = MongoClient(host=d_db['host'], port=d_db['port'])
        self.database = self.client[d_db['database']]
        print(self.client, self.database)


    def connect(self):
        pass

    def query(self):
        pass

    def insert(self, collection_name, data):
        print('DataBase insert')
        coll = self.database[collection_name]
        result = coll.insert_one(data)
        print(result.inserted_id)

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
        a.insert('okcoincn_rest_btc_ticker', data)