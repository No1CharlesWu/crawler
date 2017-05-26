import re


# configs 中如果出现了不符合函数命名规则的字符，则删去。例如：okcoin.cn' 变为 'okcoincn'
# Config类读取 config_default.py 和 config_override.py 对配置文件内容读入，
# 把task变成一个list，其中存放需要进行的任务函数名称，db 是配置数据库的信息。


class Config(object):
    def __init__(self):
        try:
            from frame import config_default
            self.configs = config_default.configs
        except ImportError:
            print('Error: %s' % ImportError)
            print('can not find config_default.py')

        try:
            from frame import config_override
            self.configs = self.merge(self.configs, config_override.configs)
        except ImportError:
            pass

        self.db = self.configs['db']
        self.task = self.split_joint(self.configs['task'])

    def merge(self, defaults, override):
        r = {}
        for k, v in defaults.items():
            if k in override:
                if isinstance(v, dict):
                    r[k] = self.merge(v, override[k])
                else:
                    r[k] = override[k]
            else:
                r[k] = v
        return r

    def split_joint(self, d):
        r_list = list()
        if isinstance(d, set):
            for i in d:
                r_list.append(re.sub(r'[^0-9a-zA-Z_]', '', i))
            return r_list
        elif isinstance(d, dict):
            for k, v in d.items():
                temp = self.split_joint(v)
                for i in temp:
                    t = re.sub(r'[^0-9a-zA-Z_]', '', k) + '_' + re.sub(r'[^0-9a-zA-Z_]', '', i)
                    r_list.append(t)
            return r_list
        else:
            return []
