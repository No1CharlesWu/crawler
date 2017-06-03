class TaskBase(object):
    def __init__(self, module_name, db):
        print('TaskBase init', db)
        self.db = db
        self.module_name = module_name
        self.result = dict()

        self.do_before()
        self.do()
        self.do_after()

    def do_before(self, module_name, db):
        pass

    def do(self):
        pass

    def data_filter(self, data):
        pass

    def data_insert(self):
        pass

    def do_after(self):
        pass

    def set_interval(self, interval=-1):
        if interval >= 0:
            self.loop = True
        else:
            self.loop = False
        self.interval = interval

    def get_result(self):
        r = dict()
        r['module_name'] = self.module_name
        r['loop'] = self.loop
        r['interval'] = self.interval
        r['result'] = self.result
        return r
