from frame import taskbase


class Task(taskbase.TaskBase):
    def do(self):
        print('okcoincn_rest_ltc_ticker')
        self.set_interval(2)

if __name__ == '__main__':
    task = Task()
