import threadpool
import time
import random
# data = [((i,),{}) for i in range(10)]


class Schedule(object):
    def __init__(self, l_task, db):
        requests = list()
        self.db = db
        for task in l_task:
            data = [((task, self.db), {'a': 'b'})]
            requests.extend(threadpool.makeRequests(self.thread_fun, data, self.callback, self.handle_exception))

        print("Creating thread pool with 4 worker threads.")
        self.main = threadpool.ThreadPool(4)

        i = 0
        for req in requests:
            i += 1
            self.main.putRequest(req)
            print("%d Work request #%s added." % (i, req.requestID))

        while True:
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
        data = [((task,), {})]
        temp = threadpool.makeRequests(self.thread_fun, data, self.callback, self.handle_exception)
        for req in temp:
            self.main.putRequest(req)
            print("callback Work request #%s added." % (req.requestID,))

    def callback(self, request, result):
        print("**** Result from request #%s: %r" % (request.requestID, result))
        self.add_task(result)

    def thread_fun(self, *args, **kwargs):
        print('ThreadFun', self, args, kwargs)
        time.sleep(0.5)
        result = round(random.random() * 1, 5)
        if result > 5:
            raise RuntimeError("Something extraordinary happened!")
        return result

    def handle_exception(self, request, exc_info):
        if not isinstance(exc_info, tuple):
            # Something is seriously wrong...
            print(self, request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % (request.requestID, exc_info))


if __name__ == '__main__':
    a = Schedule(['1', '2', '3', '4', '5'], 'db')
