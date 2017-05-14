import zope.interface

from expression import Expression
from variables import Variables


class VariableExpression(object):
    zope.interface.implements(Expression)
    key = None

    def __init__(self, key):
        self.key = key

    def eval(self):
        if not Variables.variables.has_key(self.key):
            Exception("Not found Constant")
        return Variables.variables.get(self.key)

    def __str__(self):
        return "{}".format(self.key)
