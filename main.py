# import config
from config import Config
import database
import schedule

if __name__ == '__main__':
    config = Config()
    print(config.configs)
    print('task', config.task)
    db = database.DataBase(config.db, config.task)
    print(type(db))
    schedule = schedule.Schedule(config.task, db)
