import threadpool
import time
import random

class Schedule(object):
    def __init__(self, l_task, db):
        self.db = db
        task_pool = threadpool.ThreadPool(4)

        request_list = []
        for task in l_task:
            t = ((task, self.db), dict())
            print(type(t))
            request_list.extend(threadpool.makeRequests(self.ThreadFun, [([task, self.db], {})], self.Callback))

        print(request_list)
        for request in request_list:
            task_pool.putRequest(request)
            print('work request %s added.' % request.requestID)
        task_pool.poll()

        data = [random.randint(1,10) for i in range(20)]
        requests = threadpool.makeRequests(self.do_something, data, self.print_result, self.handle_exception)
        data = [((random.randint(1,10),), {}) for i in range(20)]
        requests.extend(
            threadpool.makeRequests(self.do_something, data, self.print_result, self.handle_exception)
        )

        print("Creating thread pool with 3 worker threads.")
        main = threadpool.ThreadPool(3)

        for req in requests:
            main.putRequest(req)
            print("Work request #%s added." % req.requestID)

        i = 0
        while True:
            try:
                time.sleep(0.5)
                main.poll()
                print("Main thread working...")
                print("(active worker threads: %i)" % (threadpool.threading.activeCount()-1, ))
                if i == 10:
                    print("**** Adding 3 more worker threads...")
                    main.createWorkers(3)
                if i == 20:
                    print("**** Dismissing 2 worker threads...")
                    main.dismissWorkers(2)
                i += 1
            except KeyboardInterrupt:
                print("**** Interrupted!")
                break
            except threadpool.NoResultsPending:
                print("**** No pending results.")
                break
        if main.dismissedWorkers:
            print("Joining all dismissed worker threads...")
            main.joinAllDismissedWorkers()

    def add_task(self, task):
        pass

    def Callback(self, request, result):
        print('Callback %s:%d' % (request.requestID, result))

    def print_result(self, request, result):
        print("**** Result from request #%s: %r" % (request.requestID, result))

    def ThreadFun(self, *arg1, **arg2):
        print('ThreadFun', arg1, arg2)
        print('arg1', type(arg1), arg1)
        print('arg2', type(arg2), arg2)
        return int(arg1[0])

    def do_something(self, data):
        time.sleep(random.randint(1,5))
        result = round(random.random() * data, 5)
        # just to show off, we throw an exception once in a while
        if result > 5:
            raise RuntimeError("Something extraordinary happened!")
        return result

    def handle_exception(self, request, exc_info):
        if not isinstance(exc_info, tuple):
            # Something is seriously wrong...
            print(request)
            print(exc_info)
            raise SystemExit
        print("**** Exception occured in request #%s: %s" % \
              (request.requestID, exc_info))



if __name__ == '__main__':
    a = Schedule(['1', '2'], {'db': 'root'})
