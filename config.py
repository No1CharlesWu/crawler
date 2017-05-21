import re
import config_default


class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r


def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

def tolist(d):
    r_list = list()
    if isinstance(d, set):
        for i in d:
            r_list.append(re.sub(r'[^0-9a-zA-Z_]', '', i))
        return r_list
    elif isinstance(d, dict):
        for k, v in d.items():
            temp = tolist(v)
            for i in temp:
                t = re.sub(r'[^0-9a-zA-Z_]', '', k) + '_' + re.sub(r'[^0-9a-zA-Z_]', '', i)
                r_list.append(t)
        return r_list
    else:
        return []

configs = config_default.configs

try:
    import config_override

    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
task = tolist(configs.task)
print('task', task)
# print(configs.db, configs.task)

# configs 中如果出现了不符合函数命名规则的字符，则删去。例如：okcoin.cn' 变为 'okcoincn'
