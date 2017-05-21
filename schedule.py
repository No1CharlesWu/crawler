import threadpool


class Schedule(object):
    def __init__(self, l_task, db):
        self.db = db
        task_pool = threadpool.ThreadPool(1)

        request_list = []
        for task in l_task:
            t = ((task,self.db),dict())
            print(type(t))
            request_list.append(threadpool.makeRequests(self.ThreadFun,([task,self.db],{}), callback=self.Callback()))

        for request in request_list:
            task_pool.putRequest(*request)
        task_pool.wait()


    def add_task(self, task):
        pass

    def Callback(self):
        print('Callback')

    def ThreadFun(self, *arg1,**arg2):
        print('ThreadFun', arg1, arg2)
        print('arg1',type(arg1), arg1)
        print('arg2',type(arg2), arg2)

if __name__ == '__main__':
    a = Schedule(['1','2'], {'db':'root'})

