# import config
from config import Config
import database

if __name__ == '__main__':
    config = Config()
    db = database.DataBase(config.db, config.task)

    # print(config.configs)
    # print('task', config.task)

