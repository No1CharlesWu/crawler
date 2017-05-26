import threadpool
import time
import random
import importlib
import datetime
# data = [((i,),{}) for i in range(10)]


class Schedule(object):
    TASK = 'task'

    def __init__(self, l_task, db):
        requests = list()
        self.db = db
        for task in l_task:
            data = [((task,), {'db': self.db})]
            requests.extend(threadpool.makeRequests(self.thread_fun, data, self.callback, self.handle_exception))

        print("Creating thread pool with 4 worker threads.")
        self.main = threadpool.ThreadPool(4)

        i = 0
        for req in requests:
            i += 1
            self.main.putRequest(req)
            print("%d Work request #%s added." % (i, req.requestID))

        self.time_task_list = list()
        while True:
            current = datetime.datetime.now().timestamp()
            for d in self.time_task_list[:]:
                if d['time'] <= current:
                    self.add_task(d['module_name'])
                    self.time_task_list.remove(d)
            try:
                time.sleep(0.1)
                self.main.poll()
                print("Main thread working...")
                print("(active worker threads: %i)" % (threadpool.threading.activeCount()-1, ))
            except KeyboardInterrupt:
                print("**** Interrupted!")
                break
            except threadpool.NoResultsPending:
                print("**** No pending results.")
        if self.main.dismissedWorkers:
            print("Joining all dismissed worker threads...")
            self.main.joinAllDismissedWorkers()

    def add_task(self, task):
        data = [((task,), {'db': self.db})]
        temp = threadpool.makeRequests(self.thread_fun, data, self.callback, self.handle_exception)
        for req in temp:
            self.main.putRequest(req)
            print("callback Work request #%s added." % (req.requestID,))

    def callback(self, request, result):
        print("**** Result from request #%s: %r" % (request.requestID, result))
        c = datetime.datetime.now().timestamp()
        time = c + result['interval']
        result['time'] = time
        self.time_task_list.append(result)

    def thread_fun(self, *args, **kwargs):
        # args[0]是模块名
        print('ThreadFun', self, args, kwargs)
        try:
            task_module = importlib.import_module(self.TASK + '.' + args[0])
            print(task_module)
        except ModuleNotFoundError:
            raise
        except Exception:
            raise
        result = task_module.Task(args[0])
        # result 应该 args[0]也就是task任务文件名。interval间隔时间 dict形式
        print(result.get_result())
        return result.get_result()

    def handle_exception(self, request, exc_info):
        if not isinstance(exc_info, tuple):
            # Something is seriously wrong...
            print(self, request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % (request.requestID, exc_info))


if __name__ == '__main__':
    a = Schedule(['okcoincn_rest_btc_ticker', 'okcoincn_rest_ltc_ticker', '3', '4', '5'], 'db')
