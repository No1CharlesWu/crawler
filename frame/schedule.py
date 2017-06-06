import threadpool
import time
import importlib
import datetime

from frame import config
from frame import database


class Schedule(object):
    TASK = 'task'
    THREADPOOL_COUNT = 4

    def __init__(self):
        print("Creating thread pool with 4 worker threads.")
        self.thread_pool = threadpool.ThreadPool(self.THREADPOOL_COUNT)

        self.l_task = list()
        self.time_task_list = list()

        con = config.Config()
        self.db = database.DataBase(con.db, con.task)

        while True:
            con = config.Config()
            self.l_add_task = con.added_task(self.l_task)
            self.l_task = con.task

            for task in self.l_add_task:
                self.add_task(task, self.db)

            current = datetime.datetime.now().timestamp()
            for d in self.time_task_list[:]:
                if d['time'] <= current:
                    if d['module_name'] in self.l_task:
                        self.add_task(d['module_name'], self.db)
                    self.time_task_list.remove(d)

            try:
                time.sleep(0.1)
                print("thread pool thread working...")
                print("(active worker threads: %i)" % (threadpool.threading.activeCount() - 1,))
                self.thread_pool.poll()
            except KeyboardInterrupt:
                print("**** Interrupted!")
                break
            except threadpool.NoResultsPending:
                print("**** No pending results.")

        if self.thread_pool.dismissedWorkers:
            print("Joining all dismissed worker threads...")
            self.thread_pool.joinAllDismissedWorkers()

    def add_task(self, task, db):
        data = [((task,), {'db': db})]
        requests = threadpool.makeRequests(self.thread_fun, data, self.callback, self.handle_exception)
        for req in requests:
            self.thread_pool.putRequest(req)
            print("callback Work request #%s added." % (req.requestID,))

    def callback(self, request, result):
        print("**** Result from request #%s: %r" % (request.requestID, result))
        if result['loop'] and result['interval'] >= 0:
            result['time'] = datetime.datetime.now().timestamp() + result['interval']
            self.time_task_list.append(result)

    def thread_fun(self, *args, **kwargs):
        # args[0]是模块名
        # print('ThreadFun', self, args, kwargs)
        try:
            task_module = importlib.import_module(self.TASK + '.' + args[0])
            print(task_module)
        except ModuleNotFoundError:
            raise
        except Exception:
            raise
        result = task_module.Task(args[0], kwargs['db'])
        # result 应该 args[0]也就是task任务文件名。interval间隔时间 dict形式
        # print(result.get_result())
        return result.get_result()

    def handle_exception(self, request, exc_info):
        if not isinstance(exc_info, tuple):
            # Something is seriously wrong...
            print(self, request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % (request.requestID, exc_info))


if __name__ == '__main__':
    # a = Schedule(['okcoincn_rest_btc_ticker', 'okcoincn_rest_ltc_ticker', '3', '4', '5'], 'db')
    pass
