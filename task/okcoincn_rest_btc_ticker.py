import taskbase


class Task(taskbase.TaskBase):
    def do(self):
        print('okcoincn_rest_btc_ticker')
        self.set_interval(1)

if __name__ == '__main__':
    task = Task()
