class TaskBase(object):
    def __init__(self, module_name, db):
        self.do_before(module_name, db)
        self.do()
        self.do_after()

    def do_before(self, module_name, db):
        print('TaskBase init', db)
        self.db = db
        self.module_name = module_name
        self.loop = False
        self.interval = -1
        self.result = dict()

    def do(self):
        pass

    def do_after(self):
        pass

    def get_result(self):
        r = dict()
        r['module_name'] = self.module_name
        r['loop'] = self.loop
        r['interval'] = self.interval
        r['result'] = self.result
        return r

    def set_interval(self, interval):
        self.loop = True
        self.interval = interval

    def data_filter(self, data):
        pass
