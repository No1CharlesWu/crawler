class TaskBase(object):

    def __init__(self, module_name):
        self.do_before(module_name)
        self.do()
        self.do_after()

    def get_result(self):
        return {'module_name': self.module_name, 'interval': self.interval}

    def set_interval(self, interval):
        self.interval = interval

    def do_before(self, module_name):
        print('TaskBase init')
        self.module_name = module_name


    def do(self):
        pass

    def do_after(self):
        pass
