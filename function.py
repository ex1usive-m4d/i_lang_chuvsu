import math

import zope.interface

from value import NumberValue


class Function(zope.interface.Interface):
    def execute(self, *args):
        pass


class sin():
    zope.interface.implements(Function)
    count = 0

    def execute(self, args):
        if (len(args) != 1):
            raise RuntimeError("One args expected")
        return NumberValue(math.sin(args[0].as_double()))


class cos():
    zope.interface.implements(Function)
    count = 0

    def execute(self, args):
        if (len(args) != 1):
            raise RuntimeError("One args expected")
        return NumberValue(math.cos(args[0].as_double()))


class echo():
    zope.interface.implements(Function)
    count = 0

    def execute(self, args):
        for arg in args:
            print arg.as_string()
        return NumberValue(0)


class Functions():
    functions = dict()
    functions.update({"sin": sin()})
    functions.update({"cos": cos()})
    functions.update({"echo": echo()})

    def is_exist(self, key):
        return self.functions.has_key(key)

    def set(self, key, func):
        self.functions[key] = func

    def get(self, key):
        if self.is_exist(key):
            return self.functions[key]
        else:
            raise RuntimeError("Unknow function {}".format(self.key))


class UserDefineFunction():
    zope.interface.implements(Function)

    arg_names = []
    body = None

    def __init__(self, arg_names, body):
        self.arg_names = arg_names
        self.body = body

    def get_args_count(self):
        return len(self.arg_names)

    def get_arg_name_by_index(self, index):
        if index < 0 or index >= self.get_args_count():
            return ""
        return self.arg_names[index]

    def execute(self, *args):
        self.body.execute()
        return NumberValue(0)
