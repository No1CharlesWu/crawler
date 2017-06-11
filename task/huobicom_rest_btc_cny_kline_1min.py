import time
from frame import taskbase

class Task(taskbase.TaskBase):
    def do(self):
        pass



if __name__ == '__main__':
    import time

    task = Task('a', 'b')
    j = 1
    for i in range(360):
        time.sleep(10)
        print(j)
        j += 1
        task.do()
