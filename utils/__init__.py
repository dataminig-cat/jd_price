from importlib import import_module
import json
def load_object(path):
    '''根据路径导入类'''
    try:
        dot = path.rindex('.')  #这里取最后一个点的索引
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj
def load_setting():
    with open('setting.json','r') as f:
        setting = json.load(f)
    return setting
