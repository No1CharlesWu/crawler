# import config
from frame import schedule
from frame import config
from frame import database

if __name__ == '__main__':
    con = config.Config()
    print(con.configs)
    print('task', con.task)
    db = database.DataBase(con.db, con.task)
    print(type(db))
    schedule = schedule.Schedule(con.task, db)
