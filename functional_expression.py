import zope.interface

from expression import Expression
from function import Functions, UserDefineFunction
from value import Value
from variables import Variables


class FunctionalExpression(object):
    zope.interface.implements(Expression)

    name = ""
    arguments = list()
    pos = 0

    def __init__(self, name, arguments=[]):
        self.name = name
        self.arguments = arguments
        self.pos = len(self.arguments)

    def add_argument(self, Expression):
        temp = self.arguments
        self.arguments = Expression
        print self.arguments.eval()

    def eval(self):
        values = []
        func = Functions()
        # for i in range(len(self.arguments)):
        values.append(Value(self.arguments.eval()))
        temp_func = Functions()
        func = temp_func.get(self.name)
        if isinstance(func, UserDefineFunction):
            user_func = func
            # print values[0].as_string()
            # exit()
            if len(values) != user_func.get_args_count() - 1:
                raise RuntimeError("Args count mismatch")
            for i in range(len(values)):
                var = Variables()
                var.set_var(user_func.get_arg_name_by_index(i), values[i])

        return func.execute(values)

    def __str__(self):
        return "{}({})".format(self.name, self.arguments)
